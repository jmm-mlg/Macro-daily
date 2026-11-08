"""Email breve (una pantalla) y resumen semanal.

breve_html(): decisión del día, nota reducida (tres secciones), cartera con avisos, órdenes posibles,
disparadores más cercanos, cambios frente a ayer y enlace al informe completo publicado en docs/informe/.
semanal_html(): resumen de la semana a partir de data/ (scores, disparadores, pulso, momentum, cartera) y agenda
de la semana siguiente.
"""
import re
import csv
import json
import html as _html
import datetime as dt
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INFORME = ROOT / "docs" / "informe"

SECCIONES_BREVE = ["Decisión del día", "Las tres cosas que importan", "Plan de la semana"]


# ---------------------------------------------------------------- nota reducida
def secciones(md: str, nombres: list) -> str:
    """Extrae del Markdown de la nota las secciones indicadas (por su título ##)."""
    if not md:
        return ""
    parts = re.split(r"^## ", md, flags=re.M)
    keep = []
    for p in parts:
        title = p.split("\n", 1)[0].strip()
        if any(title.lower().startswith(n.lower()) for n in nombres):
            keep.append("## " + p.strip())
    return "\n\n".join(keep)


def nota_motor(dec: dict, res: dict, cartera: dict | None) -> str:
    """Nota de respaldo escrita por el motor cuando el modelo no responde: misma estructura, solo hechos."""
    e = dec["exposicion"]
    lines = ["## Decisión del día",
             f"Exposición objetivo {e['banda_pct']} % ({e['motivo']}). Abrir hoy: {dec['abrir_hoy']['respuesta']}: {dec['abrir_hoy']['motivo']}. "
             f"Dónde buscar: {', '.join(dec['sectores_donde_buscar']) or 'ningún sector'}. "
             + ("Qué no hacer: " + "; ".join(dec["que_no_hacer"]) + "." if dec["que_no_hacer"] else ""),
             "## Las tres cosas que importan"]
    for c in dec["casuisticas_activas"][:3]:
        qh = (c.get("que_hacer") or "").replace("\n", " ").strip()
        if len(qh) > 260:   # cortar en el final de la última frase completa, no a mitad de palabra
            cut = qh[:260]
            qh = cut[:max(cut.rfind(". "), cut.rfind("; "), cut.rfind(", ")) + 1].rstrip() or cut.rsplit(" ", 1)[0] + "…"
        lines.append(f"- **{c['titulo']}** ({c['por_que']}). {qh}")
    lines.append("## Plan de la semana")
    for x in dec["sensibilidad"].get("datos_semana", [])[:4]:
        up = "; ".join(f"{k.replace('_', ' ')} {v}" for k, v in x["si_sube"].items() if k != "sin_cambios") or "sin cambios en régimen ni sesgos"
        dn = "; ".join(f"{k.replace('_', ' ')} {v}" for k, v in x["si_baja"].items() if k != "sin_cambios") or "sin cambios"
        lines.append(f"- **{x['publicacion']}**: si sube {x['paso']}, {up}; si baja, {dn}.")
    for t in dec["sensibilidad"].get("disparadores", [])[:3]:
        ch = "; ".join(f"{k.replace('_', ' ')} {v}" for k, v in t["si_se_cruza"].items() if k != "sin_cambios") or "solo cambia la lectura"
        lines.append(f"- Si {t['serie']} cruza {t['umbral']:g} (hoy {t['valor_actual']:g}): {ch}.")
    return "\n".join(lines)


# ---------------------------------------------------------------- email breve
def _md_html(md: str) -> str:
    from . import narrativa
    return narrativa.to_html(md) if md else ""


def subject(today: str, res: dict, dec: dict | None, cartera: dict | None, alerts: list) -> str:
    s = f"[Macro] {today} · {res['regime']['label']}"
    if dec:
        s += f" · exposición {dec['exposicion']['banda_pct']} % · abrir: {dec['abrir_hoy']['respuesta']}"
    n_av = sum(1 for p in (cartera or {}).get("posiciones", []) if p["avisos"])
    if n_av:
        s += f" · {n_av} aviso{'s' if n_av != 1 else ''} en cartera"
    if alerts:
        s += f" · {len(alerts)} alerta{'s' if len(alerts) != 1 else ''}"
    return s


def breve_html(today: str, res: dict, dec: dict | None, cartera: dict | None, nar_md: str | None, alerts: list, informe_url: str, prop: dict | None = None) -> str:
    h = [f"<div style='font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:720px;color:#222;font-size:14px;line-height:1.45'>",
         f"<h2 style='margin:0 0 2px'>Macro Monitor · {today}</h2>",
         f"<p style='margin:0 0 10px;color:#666'>{res['regime']['label']} · tensión {res['tension']} · crecimiento {res['scores']['crecimiento']['score']:+d}, inflación {res['scores']['inflacion']['score']:+d}, liquidez {res['scores']['liquidez']['score']:+d}, riesgo {res['scores']['riesgo']['score']:+d}</p>"]
    if alerts:
        h.append("<p style='color:#b00;margin:0 0 8px'><b>Alertas:</b> " + " · ".join(f"{a['name']}: {a['msg']} ({a['value']})" for a in alerts) + "</p>")
    # Decisión
    if dec:
        e = dec["exposicion"]
        abrir = dec["abrir_hoy"]
        col = "#07a" if abrir["respuesta"].startswith("sí") else "#222"
        h.append("<table cellpadding='6' style='border-collapse:collapse;width:100%;margin-bottom:6px'><tr>"
                 f"<td style='border:1px solid #ddd;width:25%'><span style='color:#888;font-size:11px'>EXPOSICIÓN</span><br><b style='font-size:18px'>{e['banda_pct']} %</b></td>"
                 f"<td style='border:1px solid #ddd;width:25%'><span style='color:#888;font-size:11px'>ABRIR HOY</span><br><b style='font-size:18px;color:{col}'>{abrir['respuesta']}</b></td>"
                 f"<td style='border:1px solid #ddd;width:50%'><span style='color:#888;font-size:11px'>DÓNDE BUSCAR</span><br><b>{', '.join(dec['sectores_donde_buscar']) or 'ningún sector'}</b><br><span style='color:#666;font-size:12px'>{e['nuevas_posiciones']}</span></td></tr></table>")
        h.append(f"<p style='margin:0 0 6px;font-size:13px;color:#555'>{abrir['motivo']}.</p>")
        if dec["que_no_hacer"]:
            qnh = dec["que_no_hacer"]
            h.append("<p style='margin:0 0 8px;font-size:13px'><b>Qué no hacer:</b> " + "; ".join(qnh[:3]) + (f" (+{len(qnh) - 3} más en el informe)" if len(qnh) > 3 else "") + ".</p>")
        ch = dec["cambios"]
        items = [f"{k.replace('_', ' ')}: {v}" for k, v in ch.get("vs_ayer", {}).items() if k != "fecha"]
        mv = ch.get("disparadores_que_se_mueven", [])
        if items or mv:
            h.append("<p style='margin:0 0 8px;font-size:12px;color:#555'><b>Cambios vs ayer:</b> " + ("; ".join(items) if items else "sin cambios de régimen ni sesgos")
                     + ("; disparadores: " + ", ".join(f"{m['serie']} {'↑ se acerca' if m['se_acerca'] else '↓ se aleja'}" for m in mv[:4]) if mv else "") + "</p>")
    # Nota (reducida o de respaldo)
    md = secciones(nar_md, SECCIONES_BREVE) if nar_md else ""
    if not md and dec:
        md = nota_motor(dec, res, cartera)
        h.append("<p style='font-size:11px;color:#999;margin:0'>Nota escrita por el motor (el modelo no ha respondido hoy).</p>")
    if md:
        h.append("<div style='border-left:3px solid #ddd;padding:2px 12px;margin:6px 0 10px'>" + _md_html(md) + "</div>")
    # Cartera: solo avisos
    pos = (cartera or {}).get("posiciones", [])
    av = [p for p in pos if p["avisos"]]
    if av:
        h.append("<h4 style='margin:10px 0 4px'>Cartera · acciones pendientes</h4><ul style='margin:0 0 8px'>")
        for p in av:
            h.append(f"<li><b>{p['name']}</b> ({p['ticker']}): {'; '.join(p['avisos'])} · P&L {p['pnl_usd']:+,.0f} $ ({p['pnl_pct']:+.1f} %), a {p['dist_stop_pct']:.1f} % del stop</li>".replace(",", "."))
        h.append("</ul>")
    elif pos:
        r = cartera["resumen"]
        h.append(f"<p style='margin:6px 0;font-size:13px'><b>Cartera:</b> {r['n_posiciones']} posiciones, exposición {r['exposicion_pct']:.1f} %, P&L abierto {r['pnl_abierto_usd']:+,.0f} $, sin avisos.</p>".replace(",", "."))
    else:
        h.append("<p style='margin:6px 0;font-size:13px;color:#666'><b>Cartera:</b> sin posiciones registradas.</p>")
    # Ledger externo: órdenes propuestas, candidatas técnicas y añadidos (sustituye a "Órdenes posibles")
    if prop:
        from . import ledger
        h.append(ledger.to_html(prop))
    # Órdenes posibles y disparadores más cercanos
    if dec:
        ordenes = [c for c in dec["candidatas"] if c.get("orden_posible")]
        if ordenes and not prop:
            h.append("<h4 style='margin:10px 0 4px'>Órdenes posibles</h4><ul style='margin:0 0 8px'>")
            for c in ordenes:
                t = c["disparador_activo"][0] if c.get("disparador_activo") else {"nombre": "", "detalle": ""}
                h.append(f"<li><b>{c['empresa']}</b> ({c['ticker']}): {t['nombre']}; {t['detalle']} · acuerdo {c['patas']['a_favor']}/3 · {c['acciones']} acc. ≈ {str(c['importe']).replace(',', '.')} $ · stop {c['stop']} ({c['stop_dist_pct']} %)</li>")
            h.append("</ul>")
        pend = [c for c in dec["candidatas"] if c.get("pasa_filtro_3") and not c.get("orden_posible")][:3]
        if pend:
            h.append("<p style='margin:0 0 8px;font-size:13px'><b>A la espera de disparador:</b> " + "; ".join(f"{c['empresa']} ({'; '.join(c['le_falta'])[:90]})" for c in pend) + ".</p>")
        near = [t for t in res["triggers"] if not t["hit"]]
        near.sort(key=lambda t: abs(t["distance"]) / (abs(t["threshold"]) or 1))
        hits = [t for t in res["triggers"] if t["hit"]]
        h.append("<p style='margin:0 0 8px;font-size:13px'><b>Disparadores:</b> " + ("activos: " + ", ".join(t["series"] for t in hits) + " · " if hits else "")
                 + "más cercanos: " + ", ".join(f"{t['series']} {t['value']:g} → {t['threshold']:g}" for t in near[:3]) + ".</p>")
    h.append(f"<p style='margin:12px 0 0;font-size:13px'><a href='{informe_url}/{today}.html'>Ver informe completo</a> · <a href='{informe_url}/'>Histórico</a></p></div>")
    return "\n".join(h)


# ---------------------------------------------------------------- publicación del informe completo
def publicar(today: str, html: str) -> pathlib.Path:
    INFORME.mkdir(parents=True, exist_ok=True)
    p = INFORME / f"{today}.html"
    doc = ("<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>Macro Monitor · {today}</title></head><body style='margin:0 auto;max-width:980px;padding:12px'>" + html + "</body></html>")
    p.write_text(doc, encoding="utf-8")
    (INFORME / "latest.html").write_text(doc, encoding="utf-8")
    dates = sorted((x.stem for x in INFORME.glob("20*.html")), reverse=True)
    idx = ["<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Macro Monitor · informes</title></head><body style='font-family:sans-serif;max-width:720px;margin:20px auto'>",
           "<h2>Macro Monitor · informes diarios</h2><ul>"] + [f"<li><a href='{d}.html'>{d}</a></li>" for d in dates[:120]] + ["</ul></body></html>"]
    (INFORME / "index.html").write_text("\n".join(idx), encoding="utf-8")
    return p


# ---------------------------------------------------------------- semanal
def _csv(name):
    p = DATA / name
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def semanal_html(today: str, res: dict, dec: dict | None, cartera: dict | None, fichas: dict | None, next_events: list, informe_url: str, kb_url: str) -> str:
    end = dt.date.fromisoformat(today)
    start = end - dt.timedelta(days=7)
    sc = [r for r in _csv("scores.csv") if start.isoformat() <= r["date"] <= today]
    h = [f"<div style='font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;max-width:760px;color:#222;font-size:14px;line-height:1.45'>",
         f"<h2 style='margin:0 0 6px'>Macro Monitor · resumen semanal · {start.strftime('%d/%m')} – {end.strftime('%d/%m/%Y')}</h2>"]
    # 1. Régimen y scores: inicio vs fin de semana
    if len(sc) >= 2:
        a, b = sc[0], sc[-1]
        chg = [f"{k}: {int(a[k]):+d} → {int(b[k]):+d}" for k in ("crecimiento", "inflacion", "liquidez", "riesgo") if a.get(k) not in ("", None) and int(a[k]) != int(b[k])]
        reg = f"{a['regime']} → {b['regime']}" if a["regime"] != b["regime"] else f"{b['regime']} toda la semana"
        h.append(f"<p><b>Régimen:</b> {reg}; tensión {b.get('tension', '')}. " + ("<b>Scores que cambian:</b> " + "; ".join(chg) + "." if chg else "Scores sin cambios.") + "</p>")
        try:
            sa, sb = json.loads(a["sectors_json"]), json.loads(b["sectors_json"])
            sch = [f"{k} {sa[k]:+d} → {sb[k]:+d}" for k in sb if k in sa and sa[k] != sb[k]]
            if sch:
                h.append("<p><b>Sesgos sectoriales que cambian:</b> " + "; ".join(sch) + ".</p>")
        except (json.JSONDecodeError, KeyError):
            pass
    # 2. Disparadores: distancia inicio vs fin
    tr = [r for r in _csv("triggers.csv") if start.isoformat() <= r["date"] <= today]
    if tr:
        first = {r["series"]: float(r["distance"]) for r in tr if r["date"] == tr[0]["date"]}
        last = {r["series"]: (float(r["distance"]), r["hit"] == "1", float(r["threshold"])) for r in tr if r["date"] == tr[-1]["date"]}
        mv = sorted(((s, first[s], d, hit, thr) for s, (d, hit, thr) in last.items() if s in first and abs(first[s] - d) > 1e-9),
                    key=lambda x: -abs(x[1] - x[2]) / (abs(x[4]) or 1))[:6]
        if mv:
            h.append("<p><b>Disparadores en la semana:</b> " + "; ".join(f"{s} {'ACTIVO' if hit else ('se acerca' if abs(d) < abs(f0) else 'se aleja')} ({f0:.2f} → {d:.2f})" for s, f0, d, hit, thr in mv) + ".</p>")
    # 3. Pulso de mercado: medidas de régimen inicio vs fin
    pu = [r for r in _csv("pulso.csv") if start.isoformat() <= r["date"] <= today]
    if len(pu) >= 2:
        a, b = pu[0], pu[-1]
        def f(r, k):
            try:
                return float(r[k])
            except (ValueError, KeyError, TypeError):
                return None
        items = []
        for k, lab in (("prima_riesgo", "prima de riesgo"), ("corr_acc_bonos", "correlación acciones-bonos"), ("mercado_liquidez_z", "mercado − liquidez"), ("vix_ratio", "estructura del VIX")):
            va, vb = f(a, k), f(b, k)
            if va is not None and vb is not None:
                items.append(f"{lab} {va:.2f} → {vb:.2f}")
        if items:
            h.append("<p><b>Pulso de mercado:</b> " + "; ".join(items) + ".</p>")
    # 4. Momentum sectorial y candidatas (estado del viernes)
    if fichas:
        mom = sorted(fichas["momentum"], key=lambda m: -m["rel"]["3m"])
        top = ", ".join(f"{m['sector']} {m['region']} {m['rel']['3m']:+.1f}" for m in mom[:4])
        bot = ", ".join(f"{m['sector']} {m['region']} {m['rel']['3m']:+.1f}" for m in mom[-3:])
        confl = [f"{m['sector']} ({m['region']})" for m in fichas["momentum"] if m["conflicto"]]
        h.append(f"<p><b>Momentum sectorial (3 meses vs índice):</b> líderes {top}; rezagados {bot}." + (f" <b>Conflictos con el motor:</b> {', '.join(confl)}." if confl else "") + "</p>")
    if dec:
        ordenes = [c for c in dec["candidatas"] if c.get("orden_posible")]
        pend = [c for c in dec["candidatas"] if c.get("pasa_filtro_3") and not c.get("orden_posible")]
        h.append("<p><b>Candidatas al cierre de la semana:</b> " + (("órdenes posibles: " + ", ".join(f"{c['empresa']} ({c['patas']['a_favor']}/3)" for c in ordenes) + "; ") if ordenes else "sin órdenes posibles; ")
                 + (("a la espera: " + ", ".join(c["empresa"] for c in pend[:6])) if pend else "nada a la espera") + ".</p>")
        if dec["casuisticas_activas"]:
            h.append("<p><b>Casuísticas activas:</b> " + " · ".join(f"<a href='{kb_url}/casuisticas/{c['id']}/'>{c['titulo']}</a>" for c in dec["casuisticas_activas"]) + ".</p>")
    # 5. Cartera
    pos = (cartera or {}).get("posiciones", [])
    if pos:
        r = cartera["resumen"]
        h.append(f"<p><b>Cartera:</b> {r['n_posiciones']} posiciones, exposición {r['exposicion_pct']:.1f} %, P&L abierto {r['pnl_abierto_usd']:+,.0f} $; "
                 + "; ".join(f"{p['ticker']} {p['pnl_pct']:+.1f} % ({'; '.join(p['avisos']) if p['avisos'] else 'sin avisos'})" for p in pos) + ".</p>".replace(",", "."))
        cz = r.get("cerradas")
        if cz:
            h.append(f"<p><b>Cerradas:</b> {cz['n']} · esperanza {cz['esperanza_R']:+.2f} R · acierto {cz['acierto_pct']:.0f} %.</p>")
    else:
        h.append("<p><b>Cartera:</b> sin posiciones registradas. Registra las operaciones en paper en cartera/operaciones.csv: sin registro no hay validación.</p>")
    # 6. Semana que viene
    if next_events:
        h.append("<h4 style='margin:10px 0 4px'>Semana que viene</h4><ul style='margin:0'>")
        for e in next_events[:14]:
            h.append(f"<li>{e}</li>")
        h.append("</ul>")
    h.append(f"<p style='margin-top:12px;font-size:13px'><a href='{informe_url}/'>Informes diarios</a> · <a href='{kb_url}/'>Base de conocimiento</a></p></div>")
    return "\n".join(h)
