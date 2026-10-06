"""Descarga de datos: FRED (API) y mercado (yfinance)."""
import os
import datetime as dt
import requests
import pandas as pd

FRED_URL = "https://api.stlouisfed.org/fred"


def _key():
    k = os.environ.get("FRED_API_KEY")
    if not k:
        raise RuntimeError("Falta FRED_API_KEY en el entorno")
    return k


def fred_series(series_id: str, years: int = 10) -> pd.Series:
    """Serie FRED como pd.Series indexada por fecha (float, sin NaN)."""
    start = (dt.date.today() - dt.timedelta(days=365 * years + 30)).isoformat()
    r = requests.get(
        f"{FRED_URL}/series/observations",
        params={"series_id": series_id, "api_key": _key(), "file_type": "json",
                "observation_start": start},
        timeout=30,
    )
    r.raise_for_status()
    obs = r.json()["observations"]
    s = pd.Series({o["date"]: o["value"] for o in obs}, name=series_id)
    s.index = pd.to_datetime(s.index)
    return pd.to_numeric(s, errors="coerce").dropna()


def fred_meta(series_id: str) -> dict:
    """Metadatos: title, frequency, last_updated (fecha de última publicación)."""
    r = requests.get(
        f"{FRED_URL}/series",
        params={"series_id": series_id, "api_key": _key(), "file_type": "json"},
        timeout=30,
    )
    r.raise_for_status()
    s = r.json()["seriess"][0]
    return {"title": s["title"], "frequency": s["frequency_short"],
            "last_updated": s["last_updated"][:10]}


def fred_calendar(days_ahead: int = 7) -> list:
    """Publicaciones FRED (releases) de los próximos N días."""
    today = dt.date.today()
    end = today + dt.timedelta(days=days_ahead)
    r = requests.get(
        f"{FRED_URL}/releases/dates",
        params={"api_key": _key(), "file_type": "json",
                "realtime_start": today.isoformat(), "realtime_end": end.isoformat(),
                "include_release_dates_with_no_data": "true", "limit": 1000},
        timeout=30,
    )
    r.raise_for_status()
    out = [{"date": d["date"], "release": d["release_name"]}
           for d in r.json().get("release_dates", [])
           if today.isoformat() <= d["date"] <= end.isoformat()]
    return sorted(out, key=lambda x: x["date"])


def market_series(ticker: str, years: int = 10) -> pd.Series:
    import yfinance as yf
    df = yf.download(ticker, period=f"{years}y", interval="1d", progress=False, auto_adjust=True)
    if df.empty:
        return pd.Series(dtype=float, name=ticker)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):  # multiindex en versiones recientes de yfinance
        close = close.iloc[:, 0]
    close.name = ticker
    return close.dropna()
