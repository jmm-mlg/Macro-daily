"""Cartera: lee cartera/operaciones.csv, valora las posiciones abiertas y comprueba los límites de la guía.

Por posición: precio actual, resultado en USD (acción y divisa por separado), resultado en R, distancia al stop,
stop alcanzado, +1R / +2R, días a resultados, sector con sesgo negativo, disparador en contra activado.
Por cartera: exposición total, por sector y región; riesgo abierto; límites del nivel 6.
"""
import json
import datetime as dt
import pathlib

import pandas as pd

from . import empresas, ficha

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CSV = ROOT / "cartera" / "operaciones.csv"


def load() -> pd.DataFrame:
    if not CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(CSV, dtype=str).fillna("")
    if df.empty:
        return df
    for c in ("acciones", "precio_entrada", "stop", "fx_entrada", "sesgo_sector", "amplitud_revisiones", "precio_cierre"):
        if c in df:
            df[c] = pd.to_numeric(df[c].replace("", None), errors="coerce")
    df["estado"] = df["estado"].str.strip().str.lower()
    return df


def build(cfg: dict, res: dict, week_events: list, px: pd.DataFrame | None = None) -> dict:
    df = load()
    f = cfg.get("ficha", {})
    capital = f.get("capital", 1_000_000)
    today = dt.date.today()
    out = {"date": today.isoformat(), "capital": capital, "posiciones": [], "cerradas": [], "resumen": {}, "avisos": []}
    if df.empty:
        return out

    wl = {c["t"]: c for c in empresas.load_watchlist()}
    bias = {s["label"]: s["bias"] for s in res["sectors"]}
    hits = {t["series"] for t in res["triggers"] if t["hit"]}
    earn = {e["t"]: e["date"] for e in week_events if e.get("kind") == "resultados"}
    abiertas = df[df["estado"] == "abierta"]
    tickers = list(abiertas["ticker"].unique()) + list(ficha.FX.values())
    if px is None and tickers:
        px = ficha.download(tickers, period="3mo")
    close = px["Close"] if px is not None else pd.DataFrame()

    def fx_now(ccy):
        if ccy == "USD":
            return 1.0
        s = close[ficha.FX[ccy]].dropna() if ficha.FX[ccy] in close else None
        return float(s.iloc[-1]) if s is not None and len(s) else 1.0

    total_exp, riesgo_abierto, por_sector, por_region, factores = 0.0, 0.0, {}, {}, {}
    for _, r in abiertas.iterrows():
        t = r["ticker"]
        if t not in close:
            out["avisos"].append(f"{t}: sin precio (ticker no reconocido).")
            continue
        s = close[t].dropna()
        ccy = ficha._ccy(t)
        price = float(s.iloc[-1]) / (100 if ccy == "GBP" else 1)
        fx0, fx1 = float(r["fx_entrada"] or 1.0), fx_now(ccy)
        n, e, stop = float(r["acciones"]), float(r["precio_entrada"]), float(r["stop"])
        lado = 1 if str(r["lado"]).strip().lower() != "corto" else -1
        pnl_local = (price - e) * n * lado
        pnl_usd = pnl_local * fx1
        pnl_accion_usd = pnl_local * fx0
        pnl_divisa_usd = pnl_usd - pnl_accion_usd
        riesgo_inicial_usd = abs(e - stop) * n * fx0
        R = pnl_usd / riesgo_inicial_usd if riesgo_inicial_usd else None
        dist_stop_pct = (price - stop) / price * 100 * lado
        stop_hit = (price <= stop) if lado == 1 else (price >= stop)
        valor_usd = price * n * fx1
        meta = wl.get(t, {})
        sector = meta.get("sector", "?")
        region = meta.get("region", "EU" if ccy != "USD" else "US")
        b = bias.get(sector, 0)
        ed = earn.get(t)
        dias = (ed - today).days if ed else None
        avisos = []
        if stop_hit:
            avisos.append("STOP ALCANZADO: cerrar")
        if R is not None and R >= 2:
            avisos.append("+2R: cerrar la mitad, stop a +1R")
        elif R is not None and R >= 1:
            avisos.append("+1R: stop a precio de entrada")
        if b <= -1:
            avisos.append(f"sector con sesgo {b:+d}: revisar")
        if dias is not None and dias <= 5:
            avisos.append(f"resultados en {dias} días")
        cierro = str(r.get("cierro_si", ""))
        for sid in hits:
            if sid in cierro:
                avisos.append(f"disparador {sid} activado (en tu frase de cierre)")
        pos = {"id": r["id"], "ticker": t, "name": meta.get("name", t), "sector": sector, "region": region, "lado": "largo" if lado == 1 else "corto",
               "acciones": int(n), "entrada": e, "precio": price, "moneda": ccy, "stop": stop, "dist_stop_pct": dist_stop_pct, "stop_hit": stop_hit,
               "valor_usd": valor_usd, "pnl_usd": pnl_usd, "pnl_accion_usd": pnl_accion_usd, "pnl_divisa_usd": pnl_divisa_usd,
               "pnl_pct": pnl_local / (e * n) * 100, "R": R, "riesgo_inicial_usd": riesgo_inicial_usd,
               "riesgo_actual_usd": max(0.0, (price - stop) * n * fx1 * lado), "sesgo_sector": b, "dias_a_resultados": dias,
               "disparador": r.get("disparador", ""), "cierro_si": cierro, "fecha_apertura": r.get("fecha_apertura", ""), "avisos": avisos}
        out["posiciones"].append(pos)
        total_exp += valor_usd
        riesgo_abierto += pos["riesgo_actual_usd"]
        por_sector[sector] = por_sector.get(sector, 0) + valor_usd
        por_region[region] = por_region.get(region, 0) + valor_usd

    # cerradas: estadísticas
    cerr = df[df["estado"] == "cerrada"]
    if not cerr.empty:
        rs = []
        for _, r in cerr.iterrows():
            e, stop, pc, n = float(r["precio_entrada"]), float(r["stop"]), float(r["precio_cierre"] or 0), float(r["acciones"])
            lado = 1 if str(r["lado"]).strip().lower() != "corto" else -1
            fx0 = float(r["fx_entrada"] or 1.0)
            pnl = (pc - e) * n * lado * fx0
            risk = abs(e - stop) * n * fx0
            rs.append({"id": r["id"], "ticker": r["ticker"], "pnl_usd": pnl, "R": pnl / risk if risk else None, "motivo": r.get("motivo_cierre", "")})
        out["cerradas"] = rs
        Rs = [x["R"] for x in rs if x["R"] is not None]
        if Rs:
            wins = [x for x in Rs if x > 0]
            out["resumen"]["cerradas"] = {"n": len(Rs), "esperanza_R": sum(Rs) / len(Rs), "acierto_pct": len(wins) / len(Rs) * 100,
                                         "R_medio_ganador": (sum(wins) / len(wins)) if wins else None,
                                         "R_medio_perdedor": (sum(x for x in Rs if x <= 0) / max(1, len(Rs) - len(wins))) if len(Rs) > len(wins) else None,
                                         "pnl_total_usd": sum(x["pnl_usd"] for x in rs)}

    # límites (nivel 6 de la guía)
    pos_max = out["capital"] * (f.get("posicion_max_pct_cautela", 5.0) if res["regime"]["key"] == "mixto" or res["tension"] == "alta" else f.get("posicion_max_pct", 10.0)) / 100
    limites = []
    for p in out["posiciones"]:
        if p["valor_usd"] > pos_max:
            limites.append(f"{p['ticker']}: posición {p['valor_usd']/capital*100:.1f} % > máximo {pos_max/capital*100:.0f} %")
    for sec, v in por_sector.items():
        if v > capital * 0.25:
            limites.append(f"Sector {sec}: {v/capital*100:.1f} % > 25 %")
    for reg, v in por_region.items():
        if v > capital * 0.70:
            limites.append(f"Región {reg}: {v/capital*100:.1f} % > 70 %")
    if riesgo_abierto > capital * 0.05:
        limites.append(f"Riesgo abierto {riesgo_abierto/capital*100:.1f} % > 5 %")
    n_pos = len(out["posiciones"])
    if n_pos > 12:
        limites.append(f"{n_pos} posiciones > 12")
    sec_count = {}
    for p in out["posiciones"]:
        sec_count[p["sector"]] = sec_count.get(p["sector"], 0) + 1
    for sec, c in sec_count.items():
        if c > 2:
            limites.append(f"{c} posiciones en {sec}: correlación (máximo 2 por factor)")
    out["resumen"].update({"n_posiciones": n_pos, "exposicion_usd": total_exp, "exposicion_pct": total_exp / capital * 100,
                           "riesgo_abierto_usd": riesgo_abierto, "riesgo_abierto_pct": riesgo_abierto / capital * 100,
                           "pnl_abierto_usd": sum(p["pnl_usd"] for p in out["posiciones"]),
                           "por_sector": {k: v / capital * 100 for k, v in por_sector.items()},
                           "por_region": {k: v / capital * 100 for k, v in por_region.items()}, "limites": limites})
    return out


def save(c: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "cartera_estado.json").write_text(json.dumps(c, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    if c["posiciones"]:
        pd.DataFrame(c["posiciones"]).drop(columns=["avisos"]).to_csv(DATA / "cartera_estado.csv", index=False)


def _m(v):
    return f"{v:,.0f}".replace(",", ".")


def to_html(c: dict) -> str:
    if not c["posiciones"] and not c["cerradas"]:
        return ("<h3>Cartera</h3><p style='color:#666'>Sin posiciones registradas. Añade filas a <code>cartera/operaciones.csv</code> "
                "(ver cartera/README.md) y aparecerán aquí al día siguiente.</p>")
    r = c["resumen"]
    h = [f"<h3>Cartera · {r.get('n_posiciones', 0)} posiciones · exposición {r.get('exposicion_pct', 0):.1f} % · riesgo abierto {r.get('riesgo_abierto_pct', 0):.2f} % · P&L abierto {_m(r.get('pnl_abierto_usd', 0))} $</h3>"]
    if r.get("limites"):
        h.append("<div style='background:#fff3f3;border:1px solid #d99;border-radius:6px;padding:8px 12px;margin-bottom:8px'><b>Límites incumplidos</b><ul style='margin:4px 0'>")
        h += [f"<li>{l}</li>" for l in r["limites"]]
        h.append("</ul></div>")
    if c["avisos"]:
        h.append("<p style='color:#b00'>" + " · ".join(c["avisos"]) + "</p>")
    if c["posiciones"]:
        h.append("<table cellpadding='4' style='border-collapse:collapse;width:100%;font-size:12px'><tr style='background:#f0f0f0'>"
                 "<th align='left'>Posición</th><th align='right'>Acc.</th><th align='right'>Entrada</th><th align='right'>Precio</th><th align='right'>Stop</th>"
                 "<th align='right'>Dist.</th><th align='right'>P&L $</th><th align='right'>acción / divisa</th><th align='right'>R</th><th align='right'>Sesgo</th><th align='left'>Avisos</th></tr>")
        for p in c["posiciones"]:
            col = "#07a" if p["pnl_usd"] >= 0 else "#b00"
            style = " style='background:#fff3f3'" if p["stop_hit"] or any("disparador" in a for a in p["avisos"]) else ""
            h.append(f"<tr{style}><td><b>{p['name']}</b> <span style='color:#999'>{p['ticker']} · {p['sector'][:14]} · {p['lado']}</span></td>"
                     f"<td align='right'>{p['acciones']}</td><td align='right'>{p['entrada']:.2f}</td><td align='right'>{p['precio']:.2f} <span style='color:#999'>{p['moneda']}</span></td>"
                     f"<td align='right'>{p['stop']:.2f}</td><td align='right'>{p['dist_stop_pct']:.1f}%</td>"
                     f"<td align='right' style='color:{col};font-weight:bold'>{_m(p['pnl_usd'])} ({p['pnl_pct']:+.1f}%)</td>"
                     f"<td align='right' style='color:#666'>{_m(p['pnl_accion_usd'])} / {_m(p['pnl_divisa_usd'])}</td>"
                     f"<td align='right'>{'—' if p['R'] is None else f'{p['R']:+.2f}'}</td><td align='right'>{p['sesgo_sector']:+d}</td>"
                     f"<td style='color:#b00'>{'; '.join(p['avisos'])}</td></tr>")
        h.append("</table>")
        if r.get("por_sector"):
            h.append("<p style='font-size:12px;color:#666'>Por sector: " + ", ".join(f"{k} {v:.1f} %" for k, v in r["por_sector"].items())
                     + " · Por región: " + ", ".join(f"{k} {v:.1f} %" for k, v in r["por_region"].items()) + "</p>")
    cz = r.get("cerradas")
    if cz:
        h.append(f"<p style='font-size:12px'><b>Cerradas:</b> {cz['n']} operaciones · esperanza {cz['esperanza_R']:+.2f} R · acierto {cz['acierto_pct']:.0f} % · "
                 f"P&L {_m(cz['pnl_total_usd'])} $" + (f" · ganadora media {cz['R_medio_ganador']:+.2f} R" if cz.get("R_medio_ganador") else "")
                 + (f" · perdedora media {cz['R_medio_perdedor']:+.2f} R" if cz.get("R_medio_perdedor") else "") + "</p>")
    return "\n".join(h)


def summary_for_llm(c: dict) -> dict:
    return {"resumen": {k: v for k, v in c["resumen"].items() if k != "por_sector"},
            "posiciones": [{"ticker": p["ticker"], "sector": p["sector"], "pnl_pct": round(p["pnl_pct"], 1), "R": None if p["R"] is None else round(p["R"], 2),
                            "dist_stop_pct": round(p["dist_stop_pct"], 1), "sesgo_sector": p["sesgo_sector"], "avisos": p["avisos"], "cierro_si": p["cierro_si"]}
                           for p in c["posiciones"]]}
