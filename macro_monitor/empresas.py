"""Eventos corporativos de la watchlist: resultados, ex-dividendo y fechas fijas de mercado.

Fuentes: Finnhub (calendario de resultados con hora bmo/amc, si hay FINNHUB_API_KEY) y
yfinance (fechas de resultados y ex-dividendo; respaldo y única fuente para Europa).
Genera dos calendarios: empresas.ics (bellwethers + extra, con aviso) y
empresas-todas.ics (toda la watchlist, sin aviso).
"""
import os
import datetime as dt
import pathlib
import time
from zoneinfo import ZoneInfo

import requests
import yaml

from . import calendar as cal

ROOT = pathlib.Path(__file__).resolve().parent.parent
ET, CET = cal.ET, cal.CET

EU_SUFFIXES = (".L", ".PA", ".DE", ".AS", ".SW", ".MC", ".MI", ".CO", ".ST", ".HE", ".OL", ".BR")


# ---------------------------------------------------------------- watchlist
def load_watchlist() -> list:
    """Lista plana de empresas: t, name, role, sector, industry, region, note."""
    d = yaml.safe_load((ROOT / "watchlist.yaml").read_text(encoding="utf-8"))
    out, seen = [], set()
    for s in d.get("sectors", []):
        for ind in s.get("industries", []):
            for region in ("us", "eu"):
                for c in ind.get(region, []):
                    if c["t"] in seen:
                        continue
                    seen.add(c["t"])
                    out.append({**c, "sector": s["name"], "industry": ind["name"], "region": region.upper()})
    for c in d.get("extra", []):
        if c["t"] not in seen:
            seen.add(c["t"])
            out.append({**c, "sector": "Extra", "industry": "Posiciones y análisis", "region": "EU" if c["t"].endswith(EU_SUFFIXES) else "US"})
    return out


def market_dates(days_ahead: int) -> list:
    """Fechas fijas de mercado: quad witching (3er viernes mar/jun/sep/dic) + las del YAML."""
    d = yaml.safe_load((ROOT / "watchlist.yaml").read_text(encoding="utf-8")).get("market_dates", {})
    today, end = dt.date.today(), dt.date.today() + dt.timedelta(days=days_ahead)
    evs = []
    if d.get("quad_witching", {}).get("enabled", True):
        for y in (today.year, today.year + 1):
            for m in (3, 6, 9, 12):
                first = dt.date(y, m, 1)
                third_fri = first + dt.timedelta(days=(4 - first.weekday()) % 7 + 14)
                if today <= third_fri <= end:
                    evs.append({"date": third_fri, "kind": "mercado", "name": "Quad witching (vencimiento trimestral de opciones y futuros)",
                                "desc": "Volumen y volatilidad elevados en la apertura y el cierre. También rebalanceo trimestral del S&P 500."})
    for r in d.get("index_rebalance", []) or []:
        rd = r["date"] if isinstance(r["date"], dt.date) else dt.date.fromisoformat(str(r["date"]))
        if today <= rd <= end:
            evs.append({"date": rd, "kind": "mercado", "name": r["name"], "desc": "Flujos pasivos al cierre."})
    return evs


# ---------------------------------------------------------------- fuentes
def finnhub_earnings(days_ahead: int) -> dict:
    """{symbol: {date, hour, eps_estimate, revenue_estimate}} para el rango. Vacío sin API key."""
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        return {}
    today = dt.date.today()
    out = {}
    # Finnhub limita el rango por llamada; pedimos en tramos de 30 días
    start = today
    while start <= today + dt.timedelta(days=days_ahead):
        stop = min(start + dt.timedelta(days=30), today + dt.timedelta(days=days_ahead))
        try:
            r = requests.get("https://finnhub.io/api/v1/calendar/earnings",
                             params={"from": start.isoformat(), "to": stop.isoformat(), "token": key}, timeout=30)
            r.raise_for_status()
            for e in r.json().get("earningsCalendar", []):
                sym = e.get("symbol")
                if sym and sym not in out:
                    out[sym] = {"date": dt.date.fromisoformat(e["date"]), "hour": e.get("hour") or "",
                                "eps_estimate": e.get("epsEstimate"), "revenue_estimate": e.get("revenueEstimate")}
        except Exception as ex:  # noqa: BLE001
            print(f"(finnhub {start}: {ex})")
        start = stop + dt.timedelta(days=1)
        time.sleep(1.1)  # 60 llamadas/min en el plan gratuito
    return out


def yf_events(ticker: str, days_ahead: int) -> dict:
    """{earnings: date|None, eps_estimate, ex_dividend: date|None} vía yfinance. Tolerante a fallos."""
    import pandas as pd
    import yfinance as yf

    today, end = dt.date.today(), dt.date.today() + dt.timedelta(days=days_ahead)
    res = {"earnings": None, "eps_estimate": None, "ex_dividend": None}
    try:
        tk = yf.Ticker(ticker)
        try:
            ed = tk.get_earnings_dates(limit=8)
        except Exception:  # noqa: BLE001
            ed = None
        if ed is not None and len(ed):
            fut = [(i.date() if hasattr(i, "date") else i, row) for i, row in ed.iterrows()
                   if today <= (i.date() if hasattr(i, "date") else i) <= end]
            if fut:
                fut.sort(key=lambda x: x[0])
                d0, row = fut[0]
                res["earnings"] = d0
                est = row.get("EPS Estimate") if hasattr(row, "get") else None
                res["eps_estimate"] = None if est is None or pd.isna(est) else float(est)
        if res["earnings"] is None:
            c = tk.calendar or {}
            dates = c.get("Earnings Date") or []
            dates = [d if isinstance(d, dt.date) else d.date() for d in dates]
            dates = [d for d in dates if today <= d <= end]
            if dates:
                res["earnings"] = min(dates)
        c = tk.calendar or {}
        xd = c.get("Ex-Dividend Date")
        if xd:
            xd = xd if isinstance(xd, dt.date) else xd.date()
            if today <= xd <= end:
                res["ex_dividend"] = xd
    except Exception as ex:  # noqa: BLE001
        print(f"(yfinance {ticker}: {ex})")
    return res


# ---------------------------------------------------------------- construcción
def collect(days_ahead: int = 60, use_yf: bool = True) -> list:
    """Lista de eventos corporativos normalizados."""
    wl = load_watchlist()
    fh = finnhub_earnings(days_ahead)
    events = []
    for c in wl:
        t = c["t"]
        e = fh.get(t)
        earn, hour, eps, src = None, "", None, ""
        if e:
            earn, hour, eps, src = e["date"], e["hour"], e["eps_estimate"], "finnhub"
        xd = None
        if use_yf:
            y = yf_events(t, days_ahead)
            if earn is None and y["earnings"]:
                earn, eps, src = y["earnings"], y["eps_estimate"], "yfinance (estimada)"
            xd = y["ex_dividend"]
        if earn:
            events.append({"t": t, "name": c["name"], "role": c["role"], "sector": c["sector"], "industry": c["industry"],
                           "region": c["region"], "note": c.get("note", ""), "kind": "resultados",
                           "date": earn, "hour": hour, "eps_estimate": eps, "source": src})
        if xd:
            events.append({"t": t, "name": c["name"], "role": c["role"], "sector": c["sector"], "industry": c["industry"],
                           "region": c["region"], "note": c.get("note", ""), "kind": "ex-dividendo",
                           "date": xd, "hour": "", "eps_estimate": None, "source": "yfinance"})
    events += market_dates(days_ahead)
    events.sort(key=lambda e: (e["date"], e.get("role") != "bellwether", e.get("t", "")))
    return events


def _start(e: dict):
    """Hora del evento: Finnhub bmo/amc; Europa 07:00 CET; desconocida -> día completo."""
    d = e["date"]
    if e.get("kind") != "resultados":
        return d
    h = (e.get("hour") or "").lower()
    if h == "bmo":
        return dt.datetime(d.year, d.month, d.day, 8, 0, tzinfo=ET)
    if h == "amc":
        return dt.datetime(d.year, d.month, d.day, 16, 5, tzinfo=ET)
    if e.get("region") == "EU":
        return dt.datetime(d.year, d.month, d.day, 7, 0, tzinfo=CET)
    return d


def to_vevents(events: list, roles: set, alarm_min: int) -> list:
    out = []
    for e in events:
        if e.get("kind") == "mercado":
            out.append(cal._event(cal._uid("mkt", e["date"], e["name"]), e["date"], 0, f"📅 {e['name']}", e["desc"], alarm_min))
            continue
        if e["role"] not in roles:
            continue
        icon = "🔴" if e["role"] == "bellwether" else "🟠"
        flag = "🇺🇸" if e["region"] == "US" else "🇪🇺"
        if e["kind"] == "resultados":
            when = {"bmo": "antes de la apertura", "amc": "tras el cierre"}.get((e.get("hour") or "").lower(),
                   "por la mañana (hora europea)" if e["region"] == "EU" else "hora no confirmada")
            est = "" if "estimada" not in e["source"] else " (fecha estimada)"
            summary = f"{icon} {e['name']} ({e['t']}) · resultados{est}"
            desc = [f"{flag} {e['sector']} › {e['industry']}", f"Publica {when}.",
                    f"BPA esperado: {e['eps_estimate']:.2f}" if e.get("eps_estimate") is not None else "BPA esperado: n/d",
                    f"Fuente: {e['source']}"]
            if e.get("note"):
                desc.append(f"Nota: {e['note']}")
            out.append(cal._event(cal._uid("earn", e["t"], e["date"]), _start(e), 30, summary, "\n".join(desc), alarm_min))
        else:
            out.append(cal._event(cal._uid("xdiv", e["t"], e["date"]), e["date"], 0,
                                  f"💰 {e['name']} ({e['t']}) · ex-dividendo",
                                  f"{flag} {e['sector']} › {e['industry']}\nEl precio se ajusta a la baja por el dividendo en la apertura.", 0))
    return out


def write_calendars(events: list, docs: pathlib.Path) -> dict:
    docs.mkdir(exist_ok=True)
    top = cal.render("Empresas · bellwethers", to_vevents(events, {"bellwether", "extra"}, alarm_min=24 * 60))
    allc = cal.render("Empresas · todas", to_vevents(events, {"bellwether", "rep", "extra"}, alarm_min=0))
    (docs / "empresas.ics").write_text(top, encoding="utf-8")
    (docs / "empresas-todas.ics").write_text(allc, encoding="utf-8")
    return {"empresas.ics": top.count("BEGIN:VEVENT"), "empresas-todas.ics": allc.count("BEGIN:VEVENT")}


_DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def _fd(d):
    return f"{_DIAS[d.weekday()]} {d.day:02d}"


def week_html(events: list, days: int = 7) -> str:
    """Sección 'Esta semana en tus empresas' para el email diario."""
    end = dt.date.today() + dt.timedelta(days=days)
    week = [e for e in events if e["date"] <= end]
    if not week:
        return "<h3>Esta semana en tus empresas</h3><p style='color:#666'>Sin resultados de la watchlist en los próximos 7 días.</p>"
    h = ["<h3>Esta semana en tus empresas</h3>", "<table cellpadding='5' style='border-collapse:collapse;width:100%'>",
         "<tr style='background:#f0f0f0'><th align='left'>Fecha</th><th align='left'>Empresa</th><th align='left'>Sector</th><th align='left'>Qué</th><th align='right'>BPA esp.</th></tr>"]
    for e in week:
        if e.get("kind") == "mercado":
            h.append(f"<tr><td>{_fd(e['date'])}</td><td colspan=4>📅 {e['name']}</td></tr>")
            continue
        icon = "🔴" if e["role"] == "bellwether" else "🟠"
        flag = "🇺🇸" if e["region"] == "US" else "🇪🇺"
        when = {"bmo": "pre-apertura", "amc": "post-cierre"}.get((e.get("hour") or "").lower(), "")
        est = "" if e.get("eps_estimate") is None else f"{e['eps_estimate']:.2f}"
        what = "ex-dividendo" if e["kind"] != "resultados" else f"resultados {when}".strip()
        if e["kind"] == "resultados" and "estimada" in e["source"]:
            what += " <span style='color:#999'>(fecha est.)</span>"
        bold = "font-weight:bold" if e["role"] == "bellwether" else ""
        h.append(f"<tr style='{bold}'><td>{_fd(e['date'])}</td><td>{icon} {flag} {e['name']} <span style='color:#999'>{e['t']}</span></td>"
                 f"<td style='color:#666'>{e['sector']}</td><td>{what}</td><td align='right'>{est}</td></tr>")
    h.append("</table>")
    return "\n".join(h)
