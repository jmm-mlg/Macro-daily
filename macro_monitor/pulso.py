"""Pulso de mercado: variaciones a 1d/1s/1m/3m por bloque y medidas de régimen.

Bloques: Mercado, VIX, Treasuries, Crédito, Liquidez, Mercado-vs-liquidez.
Medidas: estructura temporal del VIX, VIX vs volatilidad realizada, descomposición del 10 años,
tipo de empinamiento, HY-IG, CCC-HY, liquidez neta (balance Fed − TGA − RRP), z-score mercado − liquidez,
prima de riesgo (earnings yield − tipo real), correlación acciones-bonos a 60 días.
Todo con FRED y yfinance; sin clave FRED las filas FRED salen vacías pero el módulo no falla.
"""
import json
import datetime as dt
import pathlib

import numpy as np
import pandas as pd

from . import fetch

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HORIZONS = {"1d": 1, "1s": 5, "1m": 21, "3m": 63}


# ---------------------------------------------------------------- utilidades
def _chg(s: pd.Series, n: int, mode: str):
    """Variación a n observaciones (días hábiles): % o diferencia absoluta."""
    if s is None or len(s) <= n:
        return None
    a, b = float(s.iloc[-1]), float(s.iloc[-1 - n])
    if mode == "pct":
        return (a / b - 1) * 100 if b else None
    return a - b


def _row(name, s, mode, unit, scale=1.0):
    if s is None or s.empty:
        return {"name": name, "value": None, "unit": unit, "chg": {k: None for k in HORIZONS}}
    return {"name": name, "value": float(s.iloc[-1]), "unit": unit, "date": s.index[-1].strftime("%Y-%m-%d"),
            "chg": {k: (None if _chg(s, n, mode) is None else _chg(s, n, mode) * scale) for k, n in HORIZONS.items()}}


def _safe(fn, *a, **kw):
    try:
        s = fn(*a, **kw)
        return s if s is not None and len(s) else None
    except Exception as e:  # noqa: BLE001
        print(f"(pulso {a[0] if a else ''}: {e})")
        return None


def _z(x: pd.Series, window: int):
    """z-score del último valor frente a la distribución de la serie en la ventana."""
    w = x.dropna().iloc[-window:]
    if len(w) < window // 2 or w.std() == 0:
        return None
    return float((w.iloc[-1] - w.mean()) / w.std())


# ---------------------------------------------------------------- bloques
def build(years: int = 3) -> dict:
    today = dt.date.today().isoformat()
    out = {"date": today, "blocks": {}, "medidas": {}, "senales": []}

    # ---------- Mercado
    spx = _safe(fetch.market_series, "^GSPC", years)
    ndx = _safe(fetch.market_series, "^IXIC", years)
    rsp = _safe(fetch.market_series, "RSP", years)
    iwm = _safe(fetch.market_series, "IWM", years)
    rows = [_row("S&P 500", spx, "pct", "%"), _row("Nasdaq", ndx, "pct", "%"),
            _row("S&P equiponderado (RSP)", rsp, "pct", "%"), _row("Russell 2000 (IWM)", iwm, "pct", "%")]
    if spx is not None and rsp is not None:
        d = {k: (_chg(spx, n, "pct") or 0) - (_chg(rsp, n, "pct") or 0) for k, n in HORIZONS.items()}
        rows.append({"name": "Amplitud: S&P − equiponderado", "value": None, "unit": "pp", "chg": d})
        if (d["3m"] or 0) > 5:
            out["senales"].append({"tipo": "amplitud", "texto": f"Subida estrecha: el S&P 500 bate al equiponderado en {d['3m']:.1f} pp a 3 meses (pocos valores sostienen el índice)."})
    if spx is not None and iwm is not None:
        d = {k: (_chg(spx, n, "pct") or 0) - (_chg(iwm, n, "pct") or 0) for k, n in HORIZONS.items()}
        rows.append({"name": "S&P − Russell 2000", "value": None, "unit": "pp", "chg": d})
    out["blocks"]["Mercado"] = rows

    # ---------- VIX
    vix = _safe(fetch.market_series, "^VIX", years)
    vix3 = _safe(fetch.market_series, "^VIX3M", years)
    rows = [_row("VIX", vix, "abs", "pts"), _row("VIX 3 meses", vix3, "abs", "pts")]
    if vix is not None and vix3 is not None:
        ratio = float(vix.iloc[-1] / vix3.iloc[-1])
        out["medidas"]["vix_estructura"] = {"ratio": ratio, "lectura": "backwardation (pánico agudo)" if ratio > 1.0 else "contango (normal)" if ratio < 0.95 else "plana"}
        if ratio > 1.0:
            out["senales"].append({"tipo": "vix", "texto": f"Curva del VIX en backwardation ({ratio:.2f}): miedo inmediato; históricamente suelos de corto plazo en días."})
    if vix is not None and spx is not None:
        rv = float(np.log(spx).diff().dropna().iloc[-20:].std() * np.sqrt(252) * 100)
        prem = float(vix.iloc[-1]) - rv
        out["medidas"]["vix_vs_realizada"] = {"vix": float(vix.iloc[-1]), "realizada_20d": rv, "prima": prem,
                                             "lectura": "seguro barato (VIX por debajo de la realizada): complacencia" if prem < 0 else "normal" if prem < 6 else "seguro caro"}
        if prem < 0:
            out["senales"].append({"tipo": "vix", "texto": f"VIX ({vix.iloc[-1]:.1f}) por debajo de la volatilidad realizada ({rv:.1f}): el mercado infravalora el riesgo."})
    out["blocks"]["VIX"] = rows

    # ---------- Treasuries
    t = {k: _safe(fetch.fred_series, k, years) for k in ("DGS2", "DGS10", "DGS30", "DFII10", "T10YIE", "T10Y2Y")}
    rows = [_row("2 años", t["DGS2"], "abs", "pb", 100), _row("10 años", t["DGS10"], "abs", "pb", 100),
            _row("30 años", t["DGS30"], "abs", "pb", 100), _row("Tipo real 10a", t["DFII10"], "abs", "pb", 100),
            _row("Breakeven 10a", t["T10YIE"], "abs", "pb", 100), _row("Curva 10−2", t["T10Y2Y"], "abs", "pb", 100)]
    if t["DGS10"] is not None and t["DFII10"] is not None and t["T10YIE"] is not None:
        dec = {}
        for k, n in HORIZONS.items():
            dn, dr, db = _chg(t["DGS10"], n, "abs"), _chg(t["DFII10"], n, "abs"), _chg(t["T10YIE"], n, "abs")
            if None not in (dn, dr, db):
                dec[k] = {"nominal": dn * 100, "real": dr * 100, "breakeven": db * 100}
        out["medidas"]["descomposicion_10a"] = dec
        m = dec.get("1m")
        if m and abs(m["nominal"]) >= 25:
            quien = "tipo real" if abs(m["real"]) > abs(m["breakeven"]) else "inflación esperada"
            out["senales"].append({"tipo": "tipos", "texto": f"El 10 años se ha movido {m['nominal']:+.0f} pb en un mes, sobre todo por {quien} ({m['real']:+.0f} real, {m['breakeven']:+.0f} breakeven)."})
    if t["DGS2"] is not None and t["DGS10"] is not None:
        d2, d10 = _chg(t["DGS2"], 21, "abs"), _chg(t["DGS10"], 21, "abs")
        if d2 is not None and d10 is not None and abs(d10 - d2) >= 0.10:
            tipo = ("bear steepening (el 10 sube más: prima de plazo o inflación)" if d10 > d2 and d10 > 0 else
                    "bull steepening (el 2 cae más: recortes descontados)" if d10 > d2 else
                    "bear flattening (el 2 sube más: Fed endureciendo)" if d2 > 0 else
                    "bull flattening (el 10 cae más: refugio)")
            out["medidas"]["empinamiento_1m"] = {"d2": d2 * 100, "d10": d10 * 100, "tipo": tipo}
    out["blocks"]["Treasuries"] = rows

    # ---------- Crédito
    c = {k: _safe(fetch.fred_series, k, years) for k in ("BAMLH0A0HYM2", "BAMLC0A0CM", "BAMLH0A3HYC")}
    hyg, lqd = _safe(fetch.market_series, "HYG", years), _safe(fetch.market_series, "LQD", years)
    rows = [_row("HY (OAS)", c["BAMLH0A0HYM2"], "abs", "pb", 100), _row("IG (OAS)", c["BAMLC0A0CM"], "abs", "pb", 100),
            _row("CCC (OAS)", c["BAMLH0A3HYC"], "abs", "pb", 100), _row("HYG (precio)", hyg, "pct", "%"), _row("LQD (precio)", lqd, "pct", "%")]
    if c["BAMLH0A0HYM2"] is not None and c["BAMLC0A0CM"] is not None:
        hy, ig = c["BAMLH0A0HYM2"], c["BAMLC0A0CM"]
        idx = hy.index.intersection(ig.index)
        rows.append(_row("HY − IG (calidad)", (hy.loc[idx] - ig.loc[idx]), "abs", "pb", 100))
    if c["BAMLH0A3HYC"] is not None and c["BAMLH0A0HYM2"] is not None:
        ccc, hy = c["BAMLH0A3HYC"], c["BAMLH0A0HYM2"]
        idx = ccc.index.intersection(hy.index)
        rows.append(_row("CCC − HY (tramo débil)", (ccc.loc[idx] - hy.loc[idx]), "abs", "pb", 100))
    out["blocks"]["Crédito"] = rows

    # ---------- Liquidez
    l = {k: _safe(fetch.fred_series, k, years) for k in ("WALCL", "WTREGEN", "RRPONTSYD", "WRESBAL", "NFCI")}
    rows = []
    neta = None
    if l["WALCL"] is not None and l["WTREGEN"] is not None and l["RRPONTSYD"] is not None:
        # a miles de millones: WALCL y WTREGEN en millones; RRPONTSYD en miles de millones
        df = pd.concat({"bal": l["WALCL"] / 1000, "tga": l["WTREGEN"] / 1000, "rrp": l["RRPONTSYD"]}, axis=1).sort_index().ffill().dropna()
        neta = (df["bal"] - df["tga"] - df["rrp"]).resample("W-WED").last().dropna()
        wk = {"1d": 0, "1s": 1, "1m": 4, "3m": 13}
        rows.append({"name": "Liquidez neta (balance − TGA − RRP)", "value": float(neta.iloc[-1]), "unit": "mM$", "date": neta.index[-1].strftime("%Y-%m-%d"),
                     "chg": {k: (None if n == 0 or len(neta) <= n else float(neta.iloc[-1] - neta.iloc[-1 - n])) for k, n in wk.items()}})
        for name, key in (("Balance de la Fed", "bal"), ("Cuenta del Tesoro (TGA)", "tga"), ("Repo inverso (RRP)", "rrp")):
            w = df[key].resample("W-WED").last().dropna()
            rows.append({"name": name, "value": float(w.iloc[-1]), "unit": "mM$", "date": w.index[-1].strftime("%Y-%m-%d"),
                         "chg": {k: (None if n == 0 or len(w) <= n else float(w.iloc[-1] - w.iloc[-1 - n])) for k, n in wk.items()}})
    if l["WRESBAL"] is not None:
        w = (l["WRESBAL"] / 1000).resample("W-WED").last().dropna()
        rows.append({"name": "Reservas bancarias", "value": float(w.iloc[-1]), "unit": "mM$", "date": w.index[-1].strftime("%Y-%m-%d"),
                     "chg": {k: (None if n == 0 or len(w) <= n else float(w.iloc[-1] - w.iloc[-1 - n])) for k, n in {"1d": 0, "1s": 1, "1m": 4, "3m": 13}.items()}})
    if l["NFCI"] is not None:
        w = l["NFCI"].dropna()
        rows.append({"name": "NFCI", "value": float(w.iloc[-1]), "unit": "índice", "date": w.index[-1].strftime("%Y-%m-%d"),
                     "chg": {k: (None if n == 0 or len(w) <= n else float(w.iloc[-1] - w.iloc[-1 - n])) for k, n in {"1d": 0, "1s": 1, "1m": 4, "3m": 13}.items()}})
    out["blocks"]["Liquidez"] = rows

    # ---------- Mercado vs liquidez
    if spx is not None and neta is not None and len(neta) > 60:
        spx_w = spx.resample("W-WED").last().dropna()
        idx = spx_w.index.intersection(neta.index)
        s3 = spx_w.loc[idx].pct_change(13).dropna() * 100     # variación a 13 semanas
        n3 = neta.loc[idx].pct_change(13).dropna() * 100
        zs, zn = _z(s3, 104), _z(n3, 104)                      # frente a 2 años de variaciones trimestrales
        if zs is not None and zn is not None:
            diff = zs - zn
            lectura = ("la bolsa sube muy por encima de lo que acompaña la liquidez: sostenida por flujos y narrativa" if diff > 1.5 else
                       "la liquidez empuja más que la bolsa: viento a favor" if diff < -1.5 else "coherentes")
            out["medidas"]["mercado_vs_liquidez"] = {"z_bolsa_3m": zs, "z_liquidez_3m": zn, "diferencia": diff,
                                                     "bolsa_3m_pct": float(s3.iloc[-1]), "liquidez_3m_pct": float(n3.iloc[-1]), "lectura": lectura}
            if abs(diff) > 1.5:
                out["senales"].append({"tipo": "mercado-liquidez", "texto": f"Mercado − liquidez: {diff:+.1f} desviaciones (bolsa {s3.iloc[-1]:+.1f} % a 3 meses, liquidez neta {n3.iloc[-1]:+.1f} %): {lectura}."})

    # ---------- Prima de riesgo (earnings yield − tipo real)
    try:
        import yfinance as yf
        info = yf.Ticker("SPY").info
        pe = info.get("forwardPE") or info.get("trailingPE")
        kind = "adelantado" if info.get("forwardPE") else "trailing"
        if pe and t["DFII10"] is not None:
            ey = 100 / float(pe)
            erp = ey - float(t["DFII10"].iloc[-1])
            out["medidas"]["prima_de_riesgo"] = {"per": float(pe), "tipo_per": kind, "earnings_yield": ey, "tipo_real": float(t["DFII10"].iloc[-1]), "prima": erp,
                                                 "lectura": "comprimida (< 1,5 %): poco pagado por el riesgo" if erp < 1.5 else "normal" if erp < 3.5 else "amplia"}
            if erp < 1.5:
                out["senales"].append({"tipo": "valoracion", "texto": f"Prima de riesgo de la renta variable {erp:.1f} % (earnings yield {ey:.1f} % − tipo real {t['DFII10'].iloc[-1]:.2f} %): comprimida."})
    except Exception as e:  # noqa: BLE001
        print(f"(pulso prima de riesgo: {e})")

    # ---------- Correlación acciones-bonos (60 días)
    tlt = _safe(fetch.market_series, "TLT", years)
    if spx is not None and tlt is not None:
        r = pd.concat({"spx": spx.pct_change(), "tlt": tlt.pct_change()}, axis=1).dropna().iloc[-60:]
        corr = float(r.corr().iloc[0, 1])
        out["medidas"]["correlacion_acciones_bonos_60d"] = {"corr": corr, "lectura": "positiva: régimen de inflación, los bonos no cubren la bolsa" if corr > 0.2 else "negativa: régimen normal, los bonos diversifican" if corr < -0.2 else "sin relación clara"}
        if corr > 0.2:
            out["senales"].append({"tipo": "correlacion", "texto": f"Correlación acciones-bonos a 60 días {corr:+.2f}: los Treasuries no protegen la cartera en este régimen."})

    return out


def save(p: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "pulso.json").write_text(json.dumps(p, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    # histórico compacto de medidas
    hist = DATA / "pulso.csv"
    m = p["medidas"]
    line = [p["date"],
            m.get("vix_estructura", {}).get("ratio"), m.get("vix_vs_realizada", {}).get("prima"),
            (m.get("descomposicion_10a", {}).get("1m") or {}).get("real"), (m.get("descomposicion_10a", {}).get("1m") or {}).get("breakeven"),
            m.get("mercado_vs_liquidez", {}).get("diferencia"), m.get("prima_de_riesgo", {}).get("prima"), m.get("correlacion_acciones_bonos_60d", {}).get("corr")]
    new = not hist.exists()
    with hist.open("a", encoding="utf-8") as f:
        if new:
            f.write("date,vix_ratio,vix_prima,d10_real_1m,d10_be_1m,mercado_liquidez_z,prima_riesgo,corr_acc_bonos\n")
        f.write(",".join("" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v)) for v in line) + "\n")


# ---------------------------------------------------------------- email
def _f(v, unit):
    if v is None:
        return "—"
    if unit in ("pb", "pts", "pp"):
        return f"{v:+.0f}" if unit == "pb" else f"{v:+.1f}"
    if unit == "mM$":
        return f"{v:+,.0f}".replace(",", ".")
    return f"{v:+.1f}"


def to_html(p: dict) -> str:
    h = ["<h3>Pulso de mercado · variaciones a 1 día / 1 semana / 1 mes / 3 meses</h3>"]
    if p["senales"]:
        h.append("<ul style='margin:4px 0 10px'>")
        for s in p["senales"]:
            h.append(f"<li><b>{s['tipo']}</b>: {s['texto']}</li>")
        h.append("</ul>")
    for block, rows in p["blocks"].items():
        if not rows:
            continue
        h.append(f"<h4 style='margin:10px 0 4px'>{block}</h4><table cellpadding='4' style='border-collapse:collapse;width:100%'>"
                 "<tr style='background:#f0f0f0'><th align='left'>Serie</th><th align='right'>Último</th>"
                 "<th align='right'>1d</th><th align='right'>1s</th><th align='right'>1m</th><th align='right'>3m</th></tr>")
        for r in rows:
            val = "—" if r.get("value") is None else (f"{r['value']:,.0f}".replace(",", ".") if r["unit"] == "mM$" else f"{r['value']:.2f}")
            cells = []
            for k in ("1d", "1s", "1m", "3m"):
                v = r["chg"].get(k)
                col = "#222" if v is None else ("#b00" if (v < 0 and r["unit"] in ("%", "mM$")) or (v > 0 and r["unit"] in ("pb", "pts")) else "#07a")
                cells.append(f"<td align='right' style='color:{col}'>{_f(v, r['unit'])}</td>")
            h.append(f"<tr><td>{r['name']} <span style='color:#999'>({r['unit']})</span></td><td align='right'><b>{val}</b></td>{''.join(cells)}</tr>")
        h.append("</table>")
    m = p["medidas"]
    h.append("<h4 style='margin:10px 0 4px'>Medidas de régimen</h4><table cellpadding='4' style='border-collapse:collapse;width:100%'>")
    if "vix_estructura" in m:
        h.append(f"<tr><td>Estructura del VIX (VIX / VIX3M)</td><td><b>{m['vix_estructura']['ratio']:.2f}</b></td><td style='color:#555'>{m['vix_estructura']['lectura']}</td></tr>")
    if "vix_vs_realizada" in m:
        x = m["vix_vs_realizada"]
        h.append(f"<tr><td>VIX frente a volatilidad realizada 20d</td><td><b>{x['vix']:.1f} vs {x['realizada_20d']:.1f}</b></td><td style='color:#555'>{x['lectura']}</td></tr>")
    if "empinamiento_1m" in m:
        x = m["empinamiento_1m"]
        h.append(f"<tr><td>Movimiento de la curva en el mes</td><td><b>2a {x['d2']:+.0f} / 10a {x['d10']:+.0f} pb</b></td><td style='color:#555'>{x['tipo']}</td></tr>")
    if "mercado_vs_liquidez" in m:
        x = m["mercado_vs_liquidez"]
        h.append(f"<tr><td>Mercado − liquidez (z-scores a 3 meses)</td><td><b>{x['diferencia']:+.1f}</b></td><td style='color:#555'>bolsa {x['bolsa_3m_pct']:+.1f} %, liquidez neta {x['liquidez_3m_pct']:+.1f} %: {x['lectura']}</td></tr>")
    if "prima_de_riesgo" in m:
        x = m["prima_de_riesgo"]
        h.append(f"<tr><td>Prima de riesgo (earnings yield − tipo real)</td><td><b>{x['prima']:.1f} %</b></td><td style='color:#555'>PER {x['tipo_per']} {x['per']:.1f} → EY {x['earnings_yield']:.1f} %; tipo real {x['tipo_real']:.2f} %: {x['lectura']}</td></tr>")
    if "correlacion_acciones_bonos_60d" in m:
        x = m["correlacion_acciones_bonos_60d"]
        h.append(f"<tr><td>Correlación acciones-bonos (60 días)</td><td><b>{x['corr']:+.2f}</b></td><td style='color:#555'>{x['lectura']}</td></tr>")
    h.append("</table>")
    return "\n".join(h)


def summary_for_llm(p: dict) -> dict:
    """Versión compacta para la narrativa."""
    comp = {}
    for block, rows in p["blocks"].items():
        comp[block] = [{"serie": r["name"], "ultimo": None if r.get("value") is None else round(r["value"], 2), "unidad": r["unit"],
                        "var": {k: (None if v is None else round(v, 1)) for k, v in r["chg"].items()}} for r in rows]
    return {"variaciones": comp, "medidas": p["medidas"], "senales": [s["texto"] for s in p["senales"]]}
