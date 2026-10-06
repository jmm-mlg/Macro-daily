"""Cálculo de métricas por serie: valor, variación, percentil, alertas; y régimen macro."""
import numpy as np
import pandas as pd


def _at_or_before(s: pd.Series, when):
    sub = s[s.index <= when]
    return float(sub.iloc[-1]) if len(sub) else None


def compute(s: pd.Series, transform: str, cfg: dict) -> dict:
    if s.empty:
        return {"error": "sin datos"}
    if transform == "level":
        t = s
    elif transform == "diff":
        t = s.diff()
    elif transform == "mom":
        t = s.pct_change() * 100
    elif transform == "yoy":
        t = s.pct_change(12) * 100
    elif transform == "qoq_ann":
        t = ((s / s.shift(1)) ** 4 - 1) * 100
    else:
        raise ValueError(f"transform desconocido: {transform}")
    t = t.dropna()
    if len(t) < 2:
        return {"error": "serie demasiado corta"}

    last_date = t.index[-1]
    value = float(t.iloc[-1])
    prev = float(t.iloc[-2])

    # Para series diarias/semanales en nivel: variación vs hace 1 mes; si no, vs anterior
    month_ago = _at_or_before(t, last_date - pd.Timedelta(days=30))
    if transform == "level" and month_ago is not None and (last_date - t.index[-2]).days < 20:
        chg, chg_label = value - month_ago, "vs 1m"
    else:
        chg, chg_label = value - prev, "vs ant."

    out = {
        "date": last_date.strftime("%Y-%m-%d"),
        "value": value, "prev": prev, "chg": chg, "chg_label": chg_label,
        "pct": float((t < value).mean() * 100),  # percentil en la ventana cargada
        "alerts": [],
    }
    a = cfg.get("alert")
    if a:
        if "above" in a and value > a["above"]:
            out["alerts"].append(a["msg"])
        if "below" in a and value < a["below"]:
            out["alerts"].append(a["msg"])
    return out


def regime(rows: dict) -> dict:
    """Semáforo: cuadrante crecimiento x inflación, con avisos de tipos y crédito."""
    def v(sid):
        return (rows.get(sid) or {}).get("value")

    def c(sid):
        return (rows.get(sid) or {}).get("chg")

    growth, infl = [], []
    if v("PAYEMS") is not None:
        growth.append(1 if v("PAYEMS") > 100 else -1 if v("PAYEMS") < 0 else 0)
    if c("ICSA") is not None:
        growth.append(-1 if c("ICSA") > 20000 else 1 if c("ICSA") < -20000 else 0)
    if v("GDPC1") is not None:
        growth.append(1 if v("GDPC1") > 2 else -1 if v("GDPC1") < 1 else 0)
    if v("RSAFS") is not None:
        growth.append(1 if v("RSAFS") > 0.3 else -1 if v("RSAFS") < -0.3 else 0)
    for sid in ("CPILFESL", "PCEPILFE"):
        if v(sid) is not None:
            infl.append(1 if v(sid) > 3 else -1 if v(sid) < 2 else 0)
        if c(sid) is not None:
            infl.append(1 if c(sid) > 0.1 else -1 if c(sid) < -0.1 else 0)

    g = int(np.sign(sum(growth))) if growth else 0
    i = int(np.sign(sum(infl))) if infl else 0
    label = {
        (1, -1): "Goldilocks (crecimiento ↑, inflación ↓): favorable a renta variable, calidad y growth",
        (1, 1): "Reflación (crecimiento ↑, inflación ↑): cíclicos, energía, value; presión sobre duración",
        (-1, 1): "Estanflación (crecimiento ↓, inflación ↑): el peor cuadrante; defensivos y materias primas",
        (-1, -1): "Desinflación recesiva (crecimiento ↓, inflación ↓): bonos y defensivos; esperar al pivot",
    }.get((g, i), "Régimen mixto / sin señal clara")

    notes = []
    if v("T10Y2Y") is not None and v("T10Y2Y") < 0:
        notes.append("curva invertida")
    if v("DFII10") is not None and v("DFII10") > 2:
        notes.append("tipos reales exigentes")
    if v("BAMLH0A0HYM2") is not None and v("BAMLH0A0HYM2") > 5:
        notes.append("estrés en crédito HY")
    if v("^VIX") is not None and v("^VIX") > 25:
        notes.append("volatilidad elevada")
    return {"growth": g, "inflation": i, "label": label, "notes": notes}
