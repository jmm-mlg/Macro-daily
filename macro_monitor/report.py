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


KB_FILES = {"^GSPC": "GSPC", "^VIX": "VIX", "DX-Y.NYB": "DXY", "CL=F": "CL", "HG=F": "HG", "GC=F": "GC", "^TNX": "DGS10", "NEWORDER": "DGORDER"}
KB_URL = ""


def kb_link(sid: str, name: str) -> str:
    """Nombre de la serie enlazado a su entrada en la base de conocimiento, si hay URL base."""
    if not KB_URL:
        return name
    f = KB_FILES.get(sid, sid)
    return f"<a href='{KB_URL}/indicadores/{f}.md' style='color:#222;text-decoration:none;border-bottom:1px dotted #999'>{name}</a>"


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

    if extra_html:
        h.append(extra_html)

    # Tabla por bloques
    h.append("<h3>Panel de series</h3>")
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
            h.append(f"<tr{style}><td>{kb_link(r['id'], r['name'])} <span style='color:#999'>({r['unit']})</span></td>"
                     f"<td align='right'><b>{_fmt(r['value'])}</b></td>"
                     f"<td align='right'>{_arrow(r['chg'])} {_fmt(r['chg'])} <span style='color:#999'>{r['chg_label']}</span></td>"
                     f"<td align='right' style='color:{pcol}'>{pct:.0f}%</td>"
                     f"<td style='color:#666'>{r['date']}</td></tr>")
        h.append("</table>")

    # Calendario
    if calendar:
        h.append("<h3>Próximas publicaciones (7 días)</h3><ul>")
        for c in calendar:
            h.append(f"<li>{c['date']}: {c['release']}</li>")
        h.append("</ul>")

    kb = f" · <a href='{KB_URL}/README.md'>Base de conocimiento</a> · <a href='{KB_URL}/BIBLIOTECA.md'>Biblioteca</a>" if KB_URL else ""
    h.append("<p style='color:#999;font-size:12px'>Fuentes: FRED (St. Louis Fed), Yahoo Finance. "
             f"Percentil = posición del valor actual dentro de los últimos 10 años.{kb}</p></body></html>")
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


# ---------------------------------------------------------------- bloque de análisis (motor de reglas)
def _score_color(s):
    return "#b00" if s <= -2 else "#c60" if s == -1 else "#222" if s == 0 else "#07a"


def analysis_html(res: dict) -> str:
    sc, rg = res["scores"], res["regime"]
    h = ["<h3>Scores y régimen</h3>"]
    h.append("<table cellpadding='6' style='border-collapse:collapse'><tr>")
    for k in ("crecimiento", "inflacion", "liquidez", "riesgo"):
        s = sc.get(k)
        if not s:
            continue
        h.append(f"<td style='border:1px solid #ddd;min-width:120px'><div style='color:#666;font-size:12px'>{s['label']}</div>"
                 f"<div style='font-size:24px;font-weight:bold;color:{_score_color(s['score'])}'>{s['score']:+d}</div>"
                 f"<div style='font-size:12px;color:#666'>{s['trend_label']} · cobertura {s['coverage']}</div></td>")
    h.append(f"<td style='border:1px solid #ddd;min-width:160px;background:#f7f7f7'><div style='color:#666;font-size:12px'>Tensión del cuadro</div>"
             f"<div style='font-size:24px;font-weight:bold'>{res['tension']}</div><div style='font-size:12px;color:#666'>liquidez vs riesgo</div></td>")
    h.append("</tr></table>")
    h.append(f"<p><b>{rg['label']}</b> — {rg['desc']}</p>")

    # Sectores
    h.append("<h3>Sesgo por sector</h3>")
    h.append("<table cellpadding='6' style='border-collapse:collapse;width:100%'>"
             "<tr style='background:#f0f0f0'><th align='left'>Sector</th><th align='right'>Sesgo</th><th align='left'>Por qué</th><th align='left'>Qué esperar</th></tr>")
    for s in res["sectors"]:
        drv = ", ".join(f"{d['label']} ({d['effect']:+.1f})" for d in s["drivers"]) or "sin factores activos"
        h.append(f"<tr><td><b>{s['label']}</b></td><td align='right' style='font-size:18px;font-weight:bold;color:{_score_color(s['bias'])}'>{s['bias']:+d}</td>"
                 f"<td style='font-size:12px;color:#555'>{drv}</td><td style='font-size:12px'>{s['behaviour']}</td></tr>")
    h.append("</table>")

    # Divergencias
    if res["divergences"]:
        h.append("<h3>Señales cruzadas</h3><ul>")
        for d in res["divergences"]:
            h.append(f"<li><b>{d['a']}</b> p{d['pct_a']:.0f} vs <b>{d['b']}</b> p{d['pct_b']:.0f}: {d['text']}</li>")
        h.append("</ul>")

    # Disparadores
    h.append("<h3>Qué vigilar · disparadores</h3><table cellpadding='5' style='border-collapse:collapse;width:100%'>")
    for t in res["triggers"]:
        d = abs(t["distance"])
        dist = f"{d:,.0f}".replace(",", ".") if d >= 1000 else f"{d:.2f}".replace(".", ",")
        flag = "<span style='color:#b00;font-weight:bold'>ACTIVADO</span>" if t["hit"] else f"a {dist}"
        h.append(f"<tr><td style='font-family:monospace;white-space:nowrap'>{kb_link(t['series'], t['series'])}</td><td style='white-space:nowrap'>{_fmt(t['value'])} / {_fmt(t['threshold'])}</td>"
                 f"<td style='white-space:nowrap'>{flag}</td><td style='font-size:12px'>{t['text']}</td></tr>")
    h.append("</table>")
    return "\n".join(h)
