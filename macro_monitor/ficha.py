"""Ficha técnica por empresa y momentum sectorial.

Ficha: precio, medias de 50 y 200, distancia a máximo de 52 semanas, ATR 14, stop estructural (mínimo de 20 sesiones)
y por ATR (2x), stop elegido y distancia, tamaño de posición para el capital y riesgo configurados (ajustado por
régimen y sesgo del sector), fuerza relativa a 1 y 3 meses frente al ETF de su sector, días hasta resultados.
Momentum sectorial: ETFs por sector (EE.UU. y Europa) frente a su índice a 1/3/6 meses y tendencia (media 200),
contrastado con el sesgo del motor (conflicto si discrepan).
Una sola descarga de yfinance para toda la watchlist.
"""
import json
import datetime as dt
import pathlib

import numpy as np
import pandas as pd

from . import empresas

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ETF_US = {"Tecnología de la información": "XLK", "Servicios de comunicación": "XLC", "Consumo discrecional": "XLY",
          "Salud": "XLV", "Financiero": "XLF", "Industriales": "XLI", "Materiales": "XLB", "Energía": "XLE",
          "Consumo básico": "XLP", "Utilities": "XLU", "Inmobiliario": "XLRE"}
ETF_EU = {"Tecnología de la información": "EXV3.DE", "Servicios de comunicación": "EXV2.DE", "Consumo discrecional": "EXH6.DE",
          "Salud": "EXV4.DE", "Financiero": "EXV1.DE", "Industriales": "EXH4.DE", "Materiales": "EXH7.DE", "Energía": "EXH1.DE",
          "Consumo básico": "EXH5.DE", "Utilities": "EXV6.DE", "Inmobiliario": "EXI5.DE"}
IDX = {"US": "SPY", "EU": "^STOXX"}
H = {"1m": 21, "3m": 63, "6m": 126}
# Moneda de cotización por sufijo; .L cotiza en peniques (GBp): se divide por 100
CCY = {".L": "GBP", ".PA": "EUR", ".DE": "EUR", ".AS": "EUR", ".MC": "EUR", ".MI": "EUR", ".BR": "EUR", ".HE": "EUR",
       ".SW": "CHF", ".CO": "DKK", ".ST": "SEK", ".OL": "NOK"}
FX = {"GBP": "GBPUSD=X", "EUR": "EURUSD=X", "CHF": "CHFUSD=X", "DKK": "DKKUSD=X", "SEK": "SEKUSD=X", "NOK": "NOKUSD=X"}


def _ccy(ticker: str) -> str:
    for suf, c in CCY.items():
        if ticker.endswith(suf):
            return c
    return "USD"


def _ret(s: pd.Series, n: int):
    s = s.dropna()
    return None if len(s) <= n else float((s.iloc[-1] / s.iloc[-1 - n] - 1) * 100)


def download(tickers: list, period="1y") -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(sorted(set(tickers)), period=period, interval="1d", progress=False, auto_adjust=True, group_by="column", threads=True)
    return df


# ---------------------------------------------------------------- momentum sectorial
def sector_momentum(px: pd.DataFrame, sectors_macro: list) -> list:
    close = px["Close"]
    bias = {s["label"]: s for s in sectors_macro}
    out = []
    for region, etfs in (("US", ETF_US), ("EU", ETF_EU)):
        idx = close[IDX[region]].dropna()
        for sector, etf in etfs.items():
            if etf not in close:
                continue
            s = close[etf].dropna()
            if len(s) < 130:
                continue
            rel = {k: (_ret(s, n) or 0) - (_ret(idx, n) or 0) for k, n in H.items()}
            ma200 = float(s.iloc[-200:].mean()) if len(s) >= 200 else float(s.mean())
            above = float(s.iloc[-1]) > ma200
            b = bias.get(sector, {}).get("bias", 0)
            mom = 1 if rel["3m"] > 3 else -1 if rel["3m"] < -3 else 0
            conflict = (b >= 1 and mom < 0) or (b <= -1 and mom > 0)
            out.append({"region": region, "sector": sector, "etf": etf, "precio": float(s.iloc[-1]), "rel": rel,
                        "abs": {k: _ret(s, n) for k, n in H.items()}, "sobre_ma200": above, "sesgo_motor": b,
                        "momentum": mom, "conflicto": conflict})
    out.sort(key=lambda x: (x["region"], -x["rel"]["3m"]))
    return out


# ---------------------------------------------------------------- fichas
def risk_pct(cfg: dict, regime_key: str, tension: str, sector_bias: int, conflict: bool) -> float:
    f = cfg.get("ficha", {})
    r = f.get("riesgo_base_pct", 0.5)
    if regime_key in ("goldilocks", "reflacion") and tension != "alta":
        r += f.get("riesgo_extra_regimen_pct", 0.25)
    if sector_bias >= 2 and not conflict:
        r += f.get("riesgo_extra_sector_pct", 0.25)
    return min(r, f.get("riesgo_max_pct", 1.0))


def build(cfg: dict, res: dict, week_events: list, confl: list, px: pd.DataFrame | None = None) -> dict:
    wl = empresas.load_watchlist()
    tickers = [c["t"] for c in wl] + list(ETF_US.values()) + list(ETF_EU.values()) + list(IDX.values()) + list(FX.values())
    if px is None:
        px = download(tickers)
    close, high, low = px["Close"], px["High"], px["Low"]
    f = cfg.get("ficha", {})
    capital = f.get("capital", 1_000_000)
    cap_ccy = f.get("moneda", "USD")
    # tipo de cambio de cada moneda a la del capital (vía USD)
    def rate(ccy):
        if ccy == cap_ccy:
            return 1.0
        to_usd = 1.0 if ccy == "USD" else float(close[FX[ccy]].dropna().iloc[-1])
        cap_to_usd = 1.0 if cap_ccy == "USD" else float(close[FX[cap_ccy]].dropna().iloc[-1])
        return to_usd / cap_to_usd
    stop_max = f.get("stop_max_pct", 8.0)
    pos_max = f.get("posicion_max_pct", 10.0)
    if res["regime"]["key"] == "mixto" or res["tension"] == "alta":
        pos_max = f.get("posicion_max_pct_cautela", 5.0)
    bias = {s["label"]: s["bias"] for s in res["sectors"]}
    conflict_sectors = {c["sector"] for c in confl}
    earn = {e["t"]: e["date"] for e in week_events if e.get("kind") == "resultados"}
    today = dt.date.today()

    fichas = []
    for c in wl:
        t = c["t"]
        if t not in close:
            continue
        s, h, l = close[t].dropna(), high[t].dropna(), low[t].dropna()
        if len(s) < 60:
            continue
        ccy = _ccy(t)
        if ccy == "GBP":  # peniques a libras
            s, h, l = s / 100, h / 100, l / 100
        fx = rate(ccy)
        price = float(s.iloc[-1])
        ma50 = float(s.iloc[-50:].mean())
        ma200 = float(s.iloc[-200:].mean()) if len(s) >= 200 else None
        hi52 = float(s.iloc[-252:].max())
        # ATR 14
        prev = s.shift(1)
        tr = pd.concat([h - l, (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1).dropna()
        atr = float(tr.iloc[-14:].mean())
        stop_struct = float(l.iloc[-20:].min())
        stop_atr = price - 2 * atr
        stop = max(stop_struct, stop_atr)  # el más cercano de los dos (menos distancia = menos riesgo por acción)
        dist_pct = (price - stop) / price * 100
        cabe = dist_pct <= stop_max and dist_pct > 0.5
        b = bias.get(c["sector"], 0)
        confl_s = c["sector"] in conflict_sectors
        rpct = risk_pct(cfg, res["regime"]["key"], res["tension"], b, confl_s)
        riesgo_eur = capital * rpct / 100                       # en la moneda del capital
        shares = int(riesgo_eur / ((price - stop) * fx)) if cabe and price > stop else 0
        notional = shares * price * fx                           # en la moneda del capital
        if notional > capital * pos_max / 100:
            shares = int(capital * pos_max / 100 / (price * fx))
            notional = shares * price * fx
        etf = (ETF_US if c["region"] == "US" else ETF_EU).get(c["sector"])
        rel = {}
        if etf and etf in close:
            e = close[etf].dropna()
            rel = {k: (_ret(s, n) or 0) - (_ret(e, n) or 0) for k, n in (("1m", 21), ("3m", 63))}
        ed = earn.get(t)
        days_to = (ed - today).days if ed else None
        fichas.append({
            "t": t, "name": c["name"], "sector": c["sector"], "region": c["region"], "role": c["role"],
            "moneda": ccy, "fx_a_capital": fx, "precio": price, "ma50": ma50, "ma200": ma200, "sobre_ma50": price > ma50, "sobre_ma200": (ma200 is not None and price > ma200),
            "dist_max52_pct": (price / hi52 - 1) * 100, "atr14": atr, "atr_pct": atr / price * 100,
            "stop_estructural": stop_struct, "stop_atr": stop_atr, "stop": stop, "stop_dist_pct": dist_pct, "cabe": cabe,
            "sesgo_sector": b, "conflicto": confl_s, "riesgo_pct": rpct, "riesgo_eur": riesgo_eur,
            "acciones": shares, "importe": notional, "importe_pct": notional / capital * 100,
            "rel_1m": rel.get("1m"), "rel_3m": rel.get("3m"), "etf": etf,
            "resultados": ed.isoformat() if ed else None, "dias_a_resultados": days_to,
            "ventana_resultados": (days_to is not None and days_to <= 5),
        })
    return {"date": today.isoformat(), "capital": capital, "moneda_capital": cap_ccy, "posicion_max_pct": pos_max, "fichas": fichas,
            "momentum": sector_momentum(px, res["sectors"])}


def save(d: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "fichas.json").write_text(json.dumps(d, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    pd.DataFrame(d["fichas"]).to_csv(DATA / "fichas.csv", index=False)
    pd.DataFrame([{**m, **{f"rel_{k}": v for k, v in m["rel"].items()}} for m in d["momentum"]]).drop(columns=["rel", "abs"]).to_csv(DATA / "momentum_sectorial.csv", index=False)


# ---------------------------------------------------------------- email
def _fmt(v, d=1, suf=""):
    return "—" if v is None else f"{v:,.{d}f}{suf}".replace(",", ".")


def to_html(d: dict, max_rows: int = 30) -> str:
    h = ["<h3>Momentum sectorial · ETFs frente a su índice</h3>"]
    confl = [m for m in d["momentum"] if m["conflicto"]]
    if confl:
        h.append("<div style='background:#fff3e0;border:1px solid #e0b060;border-radius:6px;padding:8px 12px;margin-bottom:8px'><b>Conflictos sesgo / momentum</b><ul style='margin:4px 0'>")
        for m in confl:
            h.append(f"<li><b>{m['sector']} ({m['region']})</b>: sesgo del motor {m['sesgo_motor']:+d} pero el ETF {m['etf']} va {m['rel']['3m']:+.1f} pp frente al índice a 3 meses.</li>")
        h.append("</ul></div>")
    h.append("<table cellpadding='4' style='border-collapse:collapse;width:100%'><tr style='background:#f0f0f0'>"
             "<th align='left'>Sector</th><th>ETF</th><th align='right'>rel 1m</th><th align='right'>rel 3m</th><th align='right'>rel 6m</th><th>MA200</th><th align='right'>Sesgo</th></tr>")
    for m in d["momentum"]:
        col = "#07a" if m["rel"]["3m"] > 3 else "#b00" if m["rel"]["3m"] < -3 else "#222"
        style = " style='background:#fff3f3'" if m["conflicto"] else ""
        h.append(f"<tr{style}><td>{m['sector']} <span style='color:#999'>{m['region']}</span></td><td>{m['etf']}</td>"
                 f"<td align='right'>{m['rel']['1m']:+.1f}</td><td align='right' style='color:{col};font-weight:bold'>{m['rel']['3m']:+.1f}</td>"
                 f"<td align='right'>{m['rel']['6m']:+.1f}</td><td align='center'>{'↑' if m['sobre_ma200'] else '↓'}</td><td align='right'>{m['sesgo_motor']:+d}</td></tr>")
    h.append("</table>")

    # Fichas: candidatas = sectores con sesgo >= +1 o bellwethers; ordenadas por fuerza relativa a 3 meses
    cand = [f for f in d["fichas"] if f["sesgo_sector"] >= 1 or f["role"] == "bellwether"]
    cand.sort(key=lambda f: -(f["rel_3m"] or -99))
    h.append(f"<h3>Fichas técnicas · capital {d['capital']:,.0f} {d.get('moneda_capital', 'USD')} · posición máxima {d['posicion_max_pct']:.0f} %</h3>".replace(",", "."))
    h.append("<p style='font-size:12px;color:#666'>Stop = el más cercano entre el mínimo de 20 sesiones y 2 ATR. Tamaño = capital × riesgo / (precio − stop), "
             "con riesgo 0,5-1 % según régimen y sesgo. Precio y stop en moneda local; importe en la moneda del capital. 'No cabe' = stop a más del 8 %. Fila sombreada = resultados en ≤ 5 días (no abrir).</p>")
    h.append("<table cellpadding='4' style='border-collapse:collapse;width:100%;font-size:12px'><tr style='background:#f0f0f0'>"
             "<th align='left'>Empresa</th><th align='right'>Precio</th><th>MA50/200</th><th align='right'>a máx. 52s</th><th align='right'>ATR %</th>"
             "<th align='right'>Stop</th><th align='right'>Dist.</th><th align='right'>Riesgo</th><th align='right'>Acciones</th><th align='right'>Importe</th><th align='right'>rel 3m</th><th align='right'>Result.</th></tr>")
    for f in cand[:max_rows]:
        style = " style='background:#fff3f3'" if f["ventana_resultados"] else ""
        ma = ("↑" if f["sobre_ma50"] else "↓") + ("↑" if f["sobre_ma200"] else "↓")
        stop = f"{f['stop']:.2f}" if f["cabe"] else f"<span style='color:#999'>{f['stop']:.2f} no cabe</span>"
        h.append(f"<tr{style}><td><b>{f['name']}</b> <span style='color:#999'>{f['t']} · {f['sector'][:14]} {f['sesgo_sector']:+d}</span></td>"
                 f"<td align='right'>{f['precio']:.2f} <span style='color:#999'>{f['moneda']}</span></td><td align='center'>{ma}</td><td align='right'>{f['dist_max52_pct']:+.1f}%</td>"
                 f"<td align='right'>{f['atr_pct']:.1f}</td><td align='right'>{stop}</td><td align='right'>{f['stop_dist_pct']:.1f}%</td>"
                 f"<td align='right'>{f['riesgo_pct']:.2f}%</td><td align='right'>{f['acciones'] if f['cabe'] else '—'}</td>"
                 f"<td align='right'>{_fmt(f['importe'], 0) if f['cabe'] else '—'} ({f['importe_pct']:.1f}%)</td>"
                 f"<td align='right'>{_fmt(f['rel_3m'], 1)}</td><td align='right'>{f['dias_a_resultados'] if f['dias_a_resultados'] is not None else '—'}</td></tr>")
    h.append("</table>")
    h.append("<p style='font-size:11px;color:#999'>Las 185 fichas completas están en data/fichas.csv.</p>")
    return "\n".join(h)


def summary_for_llm(d: dict) -> dict:
    cand = sorted([f for f in d["fichas"] if f["sesgo_sector"] >= 1], key=lambda f: -(f["rel_3m"] or -99))[:10]
    return {
        "momentum_sectorial": [{"sector": m["sector"], "region": m["region"], "rel_3m_pp": round(m["rel"]["3m"], 1), "sobre_ma200": m["sobre_ma200"],
                                "sesgo_motor": m["sesgo_motor"], "conflicto": m["conflicto"]} for m in d["momentum"]],
        "candidatas_en_sectores_favorecidos": [{"empresa": f["name"], "ticker": f["t"], "sector": f["sector"], "rel_3m_pp": None if f["rel_3m"] is None else round(f["rel_3m"], 1),
                                                "sobre_ma200": f["sobre_ma200"], "stop_dist_pct": round(f["stop_dist_pct"], 1), "cabe": f["cabe"],
                                                "dias_a_resultados": f["dias_a_resultados"]} for f in cand],
    }
