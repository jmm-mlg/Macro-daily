"""Render del informe (HTML + texto) y envío por email (SMTP)."""
import os
import smtplib
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _fmt(v, unit=""):
    if v is None:
        return "—"
    if abs(v) >= 1e6:
        return f"{v/1e6:,.2f}M"
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    return f"{v:,.2f}"


def _arrow(chg):
    if chg is None or abs(chg) < 1e-9:
        return "→"
    return "▲" if chg > 0 else "▼"


def render_html(rows: list, regime: dict, calendar: list, alerts: list, title: str, extra_html: str = "") -> str:
    today = dt.date.today().strftime("%d/%m/%Y")
    h = [f"<html><body style='font-family:Arial,sans-serif;font-size:14px;color:#222'>",
         f"<h2 style='margin-bottom:4px'>{title}</h2><div style='color:#666'>{today}</div>"]

    # Régimen
    h.append("<h3>Régimen macro</h3>")
    h.append(f"<p><b>{regime['label']}</b></p>")
    if regime["notes"]:
        h.append("<p>Avisos: " + ", ".join(regime["notes"]) + "</p>")

    # Alertas
    if alerts:
        h.append("<h3 style='color:#b00'>Alertas</h3><ul>")
        for a in alerts:
            h.append(f"<li><b>{a['name']}</b>: {a['msg']} (valor {_fmt(a['value'])})</li>")
        h.append("</ul>")

    # Tabla por bloques
    blocks = {}
    for r in rows:
        blocks.setdefault(r["block"], []).append(r)
    for block, items in blocks.items():
        h.append(f"<h3>{block}</h3>")
        h.append("<table cellpadding='6' style='border-collapse:collapse;width:100%'>"
                 "<tr style='background:#f0f0f0'><th align='left'>Serie</th><th align='right'>Último</th>"
                 "<th align='right'>Variación</th><th align='right'>Percentil 10a</th><th align='left'>Fecha</th></tr>")
        for r in items:
            if "error" in r:
                h.append(f"<tr><td>{r['name']}</td><td colspan=4 style='color:#999'>{r['error']}</td></tr>")
                continue
            pct = r["pct"]
            pcol = "#b00" if pct >= 90 else "#07a" if pct <= 10 else "#222"
            style = " style='background:#fff3f3'" if r["alerts"] else ""
            h.append(f"<tr{style}><td>{r['name']} <span style='color:#999'>({r['unit']})</span></td>"
                     f"<td align='right'><b>{_fmt(r['value'])}</b></td>"
                     f"<td align='right'>{_arrow(r['chg'])} {_fmt(r['chg'])} <span style='color:#999'>{r['chg_label']}</span></td>"
                     f"<td align='right' style='color:{pcol}'>{pct:.0f}%</td>"
                     f"<td style='color:#666'>{r['date']}</td></tr>")
        h.append("</table>")

    if extra_html:
        h.append(extra_html)

    # Calendario
    if calendar:
        h.append("<h3>Próximas publicaciones (7 días)</h3><ul>")
        for c in calendar:
            h.append(f"<li>{c['date']}: {c['release']}</li>")
        h.append("</ul>")

    h.append("<p style='color:#999;font-size:12px'>Fuentes: FRED (St. Louis Fed), Yahoo Finance. "
             "Percentil = posición del valor actual dentro de los últimos 10 años.</p></body></html>")
    return "\n".join(h)


def render_text(rows: list, regime: dict, alerts: list) -> str:
    lines = [f"RÉGIMEN: {regime['label']}"]
    if regime["notes"]:
        lines.append("Avisos: " + ", ".join(regime["notes"]))
    if alerts:
        lines.append("\nALERTAS:")
        for a in alerts:
            lines.append(f"  - {a['name']}: {a['msg']} ({_fmt(a['value'])})")
    lines.append("")
    for r in rows:
        if "error" in r:
            lines.append(f"{r['name']:<45} {r['error']}")
        else:
            lines.append(f"{r['name']:<45} {_fmt(r['value']):>12} {_arrow(r['chg'])}{_fmt(r['chg']):>10} "
                         f"{r['chg_label']:<8} p{r['pct']:.0f}  {r['date']}")
    return "\n".join(lines)


def send_email(subject: str, html: str, text: str):
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    pwd = os.environ["SMTP_PASS"]
    to = os.environ.get("EMAIL_TO", user)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP(host, port, timeout=30) as s:
        s.starttls()
        s.login(user, pwd)
        s.sendmail(user, [a.strip() for a in to.split(",")], msg.as_string())
