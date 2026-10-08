"""Verifica las afirmaciones fechadas de la base de conocimiento contra FRED y yfinance.

Las afirmaciones están en kb/verificacion.yaml (una por línea: entrada, serie, fecha, valor afirmado,
tolerancia). El script descarga el dato real, compara y escribe un informe en kb/_verificacion.md
marcando OK, DESVIACIÓN (fuera de tolerancia) o SIN DATO.

Uso:  FRED_API_KEY=... python kb/verificar.py            (todas)
      python kb/verificar.py --entrada DFII10              (solo una entrada)
      python kb/verificar.py --solo-mercado                (sin FRED, solo yfinance)
"""
import os
import sys
import datetime as dt
import pathlib

import yaml
import requests
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
CLAIMS = ROOT / "verificacion.yaml"
REPORT = ROOT / "_verificacion.md"
FRED = "https://api.stlouisfed.org/fred/series/observations"
MARKET = ("^GSPC", "^VIX", "DX-Y.NYB", "CL=F", "HG=F", "GC=F", "^TNX")


def fred_series(sid, start, end):
    key = os.environ.get("FRED_API_KEY")
    if not key:
        return None
    r = requests.get(FRED, params={"series_id": sid, "api_key": key, "file_type": "json",
                                   "observation_start": start, "observation_end": end}, timeout=30)
    r.raise_for_status()
    s = pd.Series({o["date"]: o["value"] for o in r.json()["observations"]})
    s.index = pd.to_datetime(s.index)
    return pd.to_numeric(s, errors="coerce").dropna()


def yf_series(ticker, start, end):
    import yfinance as yf
    df = yf.download(ticker, start=start, end=end, interval="1d", progress=False, auto_adjust=False)
    if df.empty:
        return None
    s = df["Close"]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    return s.dropna()


def window(date, kind):
    d = pd.Timestamp(date)
    if kind in ("max_mes", "min_mes", "media_mes"):
        return d.replace(day=1), (d.replace(day=1) + pd.offsets.MonthEnd(1))
    if kind in ("max_anio", "min_anio"):
        return d.replace(month=1, day=1), d.replace(month=12, day=31)
    return d - pd.Timedelta(days=45), d + pd.Timedelta(days=45)


def evaluate(claim):
    sid, date, kind = claim["serie"], str(claim["fecha"]), claim.get("tipo", "valor")
    start, end = window(date, kind)
    try:
        s = yf_series(sid, start.date().isoformat(), (end + pd.Timedelta(days=1)).date().isoformat()) \
            if sid in MARKET else fred_series(sid, start.date().isoformat(), end.date().isoformat())
    except Exception as e:  # noqa: BLE001
        return {"estado": "ERROR", "real": None, "detalle": str(e)}
    if s is None or s.empty:
        return {"estado": "SIN DATO", "real": None, "detalle": "sin clave FRED o serie vacía"}

    transform = claim.get("transformacion")
    if transform == "yoy":
        # necesita 13 meses atrás: volver a pedir
        s2 = (yf_series if sid in MARKET else fred_series)(sid, (start - pd.Timedelta(days=400)).date().isoformat(), end.date().isoformat())
        s = (s2.pct_change(12) * 100).dropna()
    elif transform == "diff":
        s2 = (yf_series if sid in MARKET else fred_series)(sid, (start - pd.Timedelta(days=60)).date().isoformat(), end.date().isoformat())
        s = s2.diff().dropna()
    elif transform == "qoq_ann":
        s2 = (yf_series if sid in MARKET else fred_series)(sid, (start - pd.Timedelta(days=200)).date().isoformat(), end.date().isoformat())
        s = (((s2 / s2.shift(1)) ** 4 - 1) * 100).dropna()

    sub = s[(s.index >= start) & (s.index <= end)]
    if sub.empty:
        return {"estado": "SIN DATO", "real": None, "detalle": "sin observaciones en la ventana"}
    if kind in ("max_mes", "max_anio"):
        real, when = float(sub.max()), sub.idxmax()
    elif kind in ("min_mes", "min_anio"):
        real, when = float(sub.min()), sub.idxmin()
    elif kind == "media_mes":
        real, when = float(sub.mean()), sub.index[0]
    else:  # valor en la fecha (o la observación más cercana anterior)
        at = sub[sub.index <= pd.Timestamp(date)]
        real, when = (float(at.iloc[-1]), at.index[-1]) if len(at) else (float(sub.iloc[0]), sub.index[0])
    claimed, tol = float(claim["valor"]), float(claim.get("tolerancia", 0.1))
    ok = abs(real - claimed) <= tol
    return {"estado": "OK" if ok else "DESVIACIÓN", "real": real, "fecha_real": when.date().isoformat(),
            "detalle": f"afirmado {claimed} · real {real:.3f} ({when.date()}) · tol ±{tol}"}


def main():
    args = sys.argv[1:]
    only = args[args.index("--entrada") + 1] if "--entrada" in args else None
    solo_mercado = "--solo-mercado" in args
    claims = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))["afirmaciones"]
    rows = []
    for c in claims:
        if only and c["entrada"] != only:
            continue
        if solo_mercado and c["serie"] not in MARKET:
            continue
        r = evaluate(c)
        rows.append({**c, **r})
        print(f"[{r['estado']:<10}] {c['entrada']:<16} {c['serie']:<18} {c['fecha']}  {c['texto'][:60]}  ->  {r['detalle']}")

    today = dt.date.today().isoformat()
    n_ok = sum(r["estado"] == "OK" for r in rows)
    n_dev = sum(r["estado"] == "DESVIACIÓN" for r in rows)
    n_nd = len(rows) - n_ok - n_dev
    out = [f"# Verificación de la base de conocimiento · {today}", "",
           f"{len(rows)} afirmaciones: **{n_ok} OK**, **{n_dev} con desviación**, {n_nd} sin dato.", "",
           "| Estado | Entrada | Serie | Fecha | Afirmación | Afirmado | Real | Detalle |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(rows, key=lambda x: (x["estado"] != "DESVIACIÓN", x["entrada"])):
        real = "" if r["real"] is None else f"{r['real']:.2f} ({r.get('fecha_real', '')})"
        out.append(f"| {r['estado']} | {r['entrada']} | {r['serie']} | {r['fecha']} | {r['texto']} | {r['valor']} | {real} | {r['detalle']} |")
    out += ["", "Las desviaciones se corrigen en la entrada correspondiente (sección Episodios) y se actualiza `verificacion.yaml`.",
            "Tolerancias: décimas para tipos e inflación; unidades para índices; porcentaje para variaciones."]
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"\nInforme: {REPORT}  ({n_ok} OK, {n_dev} desviaciones, {n_nd} sin dato)")
    return 1 if n_dev else 0


if __name__ == "__main__":
    sys.exit(main())
