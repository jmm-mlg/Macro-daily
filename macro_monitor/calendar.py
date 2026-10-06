"""Genera un .ics con publicaciones macro (FRED) y reuniones FOMC/BCE para suscribirse desde Google Calendar."""
import datetime as dt
import hashlib
import pathlib
from zoneinfo import ZoneInfo

import yaml

from . import fetch

ET = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Madrid")
UTC = ZoneInfo("UTC")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def _uid(*parts):
    return hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest() + "@macro-monitor"


def _ics_dt(d: dt.datetime) -> str:
    return d.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def _event(uid, start, minutes, summary, description, alarm_min=15):
    """Evento con hora. Si start es un date (sin hora) se crea evento de día completo."""
    now = _ics_dt(dt.datetime.now(UTC))
    if isinstance(start, dt.date) and not isinstance(start, dt.datetime):
        dates = [f"DTSTART;VALUE=DATE:{start.strftime('%Y%m%d')}",
                 f"DTEND;VALUE=DATE:{(start + dt.timedelta(days=1)).strftime('%Y%m%d')}"]
    else:
        dates = [f"DTSTART:{_ics_dt(start)}", f"DTEND:{_ics_dt(start + dt.timedelta(minutes=minutes))}"]
    lines = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{now}", *dates,
             f"SUMMARY:{_esc(summary)}", f"DESCRIPTION:{_esc(description)}"]
    if alarm_min:
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{_esc(summary)}",
                  f"TRIGGER:-PT{alarm_min}M", "END:VALARM"]
    lines.append("END:VEVENT")
    return "\n".join(lines)


def fred_release_events(cfg: dict, latest: dict | None = None) -> list:
    """Eventos de publicaciones FRED de los próximos N días, filtrados por config.calendar.releases."""
    cal = cfg.get("calendar", {})
    days = cal.get("days_ahead", 60)
    rules = cal.get("releases", [])
    names = {s["id"]: s["name"] for s in cfg["fred"]}
    events, seen = [], set()

    for rel in fetch.fred_calendar(days):
        for rule in rules:
            if rule["match"].lower() not in rel["release"].lower():
                continue
            key = (rel["date"], rule["label"])
            if key in seen:
                continue
            seen.add(key)
            hh, mm = map(int, rule["time_et"].split(":"))
            d = dt.date.fromisoformat(rel["date"])
            start = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=ET)
            local = start.astimezone(CET).strftime("%H:%M")
            icon = {"alta": "🔴", "media": "🟠", "baja": "⚪"}.get(rule.get("importance"), "")
            lines = [f"Release FRED: {rel['release']}", f"Hora: {rule['time_et']} ET / {local} España",
                     f"Importancia: {rule.get('importance', '-')}", "", "Series afectadas:"]
            for sid in rule.get("series", []):
                line = f"  - {names.get(sid, sid)} [{sid}]"
                if latest and sid in latest and "value" in latest[sid]:
                    r = latest[sid]
                    line += f": último {r['value']:.2f} ({r['date']})"
                lines.append(line)
            events.append(_event(_uid("fred", rel["date"], rule["label"]), start, 30,
                                 f"{icon} {rule['label']}", "\n".join(lines)))
    return events


def central_bank_events() -> list:
    cb = yaml.safe_load((ROOT / "central_banks.yaml").read_text(encoding="utf-8"))
    events = []
    for m in cb.get("fomc", []):
        d = m["date"] if isinstance(m["date"], dt.date) else dt.date.fromisoformat(m["date"])
        start = dt.datetime(d.year, d.month, d.day, 14, 0, tzinfo=ET)
        extra = " + proyecciones y dot plot" if m.get("sep") else ""
        desc = (f"Decisión de tipos de la Reserva Federal a las 14:00 ET "
                f"({start.astimezone(CET).strftime('%H:%M')} España); rueda de prensa 14:30 ET.{extra}\n"
                "Series: DFF, DGS2, DGS10, DFII10")
        events.append(_event(_uid("fomc", d), start, 60, f"🏛️ FOMC: decisión de tipos{extra}", desc, 30))
    for m in cb.get("ecb", []):
        d = m["date"] if isinstance(m["date"], dt.date) else dt.date.fromisoformat(m["date"])
        start = dt.datetime(d.year, d.month, d.day, 14, 15, tzinfo=CET)
        extra = " + proyecciones del staff" if m.get("proj") else ""
        desc = f"Decisión del Consejo de Gobierno del BCE a las 14:15; rueda de prensa 14:45.{extra}\nSeries: ECBDFR"
        events.append(_event(_uid("ecb", d), start, 60, f"🏛️ BCE: decisión de tipos{extra}", desc, 30))
    return events


def build_ics(cfg: dict, latest: dict | None = None) -> str:
    return render("Macro Monitor", fred_release_events(cfg, latest) + central_bank_events())


def render(name: str, events: list) -> str:
    """Envuelve una lista de VEVENT en un VCALENDAR válido (RFC 5545)."""
    body = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//macro-monitor//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{name}",
        "X-WR-TIMEZONE:Europe/Madrid",
        "X-PUBLISHED-TTL:PT12H",
        *events,
        "END:VCALENDAR",
    ]
    # Plegado de líneas a 75 octetos según RFC 5545
    out = []
    for line in "\n".join(body).split("\n"):
        enc = line.encode("utf-8")
        while len(enc) > 73:
            cut = 73
            while cut > 0 and (enc[cut] & 0xC0) == 0x80:  # no partir un carácter UTF-8
                cut -= 1
            out.append(enc[:cut].decode("utf-8"))
            enc = b" " + enc[cut:]
        out.append(enc.decode("utf-8"))
    return "\r\n".join(out) + "\r\n"
