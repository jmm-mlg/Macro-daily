"""Capa LLM: nota del comité redactada por Groq a partir del JSON del día.

Reglas de diseño:
- El modelo solo ve el payload que le pasamos (scores, régimen, sectores, divergencias, disparadores,
  series clave, cambio vs. ayer y agenda). Nunca busca ni inventa datos: si falta algo, lo dice.
- Estructura fija de salida. Longitud acotada.
- Si no hay GROQ_API_KEY o falla, el informe sale sin narrativa (nunca bloquea el envío).
"""
import os
import csv
import json
import datetime as dt
import pathlib
import html as _html

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]

SYSTEM = """Eres el analista senior de un comité de inversión personal. Redactas la nota diaria en español para un inversor
a medio plazo (meses) en acciones de EE.UU. y Europa. El motor ya ha CALCULADO la decisión (clave "decision" del JSON):
banda de exposición, si se abre hoy, sectores donde buscar y vetados, candidatas y lo que les falta, casuísticas activas
con su "qué hacer", sensibilidad de los disparadores y de los datos de la semana, cambios frente a ayer, historial del
régimen y acciones pendientes en cartera. TU TRABAJO NO ES CALCULAR NADA: es explicar esa decisión, argumentarla con los
datos y convertirla en un plan. Cada frase termina en una acción o en una condición.

REGLAS ESTRICTAS:
1. Usa ÚNICAMENTE el JSON. No cites cifras, fechas ni hechos que no estén en él. Si falta algo, di "no disponible".
2. No contradigas la decisión del motor: si "abrir_hoy" es "no", la nota no propone abrir. Puedes matizarla (por qué, qué
   la cambiaría), nunca invertirla. Las candidatas se citan como candidatas, con lo que les falta; nunca como compras.
3. Habla de la ECONOMÍA y de la CARTERA, no del sistema. PROHIBIDAS: score, scores, percentil, umbral, disparador,
   cobertura, JSON, payload, activado, "sesgo +1". Traduce: "tipo real en máximos de la década", "a 22 pb del 5,50 %
   que haría al bono competir con la bolsa", "nóminas +29k frente a +133k".
4. COMPRUEBA EL SIGNO de cada comparación. Un error de signo invalida la nota.
5. Apóyate en las casuísticas activas: su "qué hacer" es la doctrina de la casa; cítalas por su título.
6. Usa la sensibilidad calculada para el plan de la semana: "si el IPC subyacente sube 0,2 pp, la inflación pasa a
   +2 y el régimen a Estanflación; entonces X". No inventes escenarios que el JSON no trae.
7. Sobrio, concreto, sin adjetivos vacíos. Entre 320 y 480 palabras. Escribe las SEIS secciones completas.

FORMATO (Markdown, exactamente estas seis secciones, con estos títulos):
## Decisión del día
(Exposición objetivo, si se abre algo hoy y por qué, dónde buscar y qué está vetado. 3-4 frases, la primera es la decisión.)
## Las tres cosas que importan
(3 viñetas: dato + mecanismo + consecuencia para la cartera. Ordenadas por impacto, no por novedad. Usa "cambios" para
destacar lo que ha cambiado frente a ayer solo si altera una decisión.)
## Candidatas y lo que les falta
(Las que pasan el filtro 3 con su stop y tamaño, y el disparador concreto que las convertiría en orden; las que no pasan,
en una línea con el motivo. Si no hay sectores donde buscar, dilo y explica qué tendría que cambiar.)
## Plan de la semana
(Tabla o lista evento → fecha → si sale X, hago Y / si sale Z, hago W, con la sensibilidad calculada y los resultados de
bellwethers de la semana. Incluye qué NO hacer antes de cada dato.)
## Cartera
(Si hay posiciones: una línea por posición con avisos: mantener / mover stop / reducir / cerrar y el motivo. Si no hay:
"Sin posiciones" y una frase sobre la exposición objetivo.)
## Qué me haría cambiar de opinión
(2-3 condiciones concretas con fecha y la acción asociada, tomadas de la sensibilidad y de "qué la resuelve" de las casuísticas.)"""


KEY_SERIES_SHORT = ["DGS10", "DFII10", "T10Y2Y", "CPIAUCSL", "CPILFESL", "PCEPILFE", "PPIFIS", "CES0500000003", "PAYEMS", "ICSA",
                    "RSAFS", "NEWORDER", "BAMLH0A0HYM2", "^GSPC", "^VIX", "CL=F", "HG=F", "EURUSD=X", "JPY=X"]


def _yesterday_scores() -> dict | None:
    p = DATA / "scores.csv"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    today = dt.date.today().isoformat()
    prev = [r for r in rows if r["date"] < today]
    if not prev:
        return None
    r = prev[-1]
    return {"date": r["date"], "regime": r["regime"], "crecimiento": int(r["crecimiento"]), "inflacion": int(r["inflacion"]),
            "liquidez": int(r["liquidez"]), "riesgo": int(r["riesgo"]), "tension": r["tension"],
            "sectors": json.loads(r["sectors_json"])}


def build_payload(rows: dict, res: dict, week_events: list, calendar: list) -> dict:
    """Payload compacto y explícito: lo único que verá el modelo."""
    key_series = ["DGS10", "DFII10", "T10Y2Y", "CPIAUCSL", "CPILFESL", "PCEPILFE", "PPIFIS", "CES0500000003",
                  "PAYEMS", "UNRATE", "ICSA", "CCSA", "JTSQUR", "RSAFS", "RSCCAS", "NEWORDER", "TCU", "PSAVERT", "DRCCLACBS", "CUSR0000SASL2RS", "UMCSENT", "MORTGAGE30US", "BAMLH0A0HYM2", "NFCI", "CU_AU", "TTF=F",
                  "ECBDFR", "CP0000EZ19M086NEST", "^GSPC", "^VIX", "DX-Y.NYB", "EURUSD=X", "JPY=X", "CNY=X", "CL=F", "HG=F", "GC=F"]
    series = {}
    for sid in key_series:
        r = rows.get(sid)
        if r and "value" in r:
            series[sid] = {"nombre": r.get("name"), "valor": round(r["value"], 2), "unidad": r.get("unit"),
                           "variacion": None if r.get("chg") is None else round(r["chg"], 2),
                           "variacion_vs": r.get("chg_label"), "percentil_10a": None if r.get("pct") is None else round(r["pct"]),
                           "fecha_dato": r.get("date")}
    return {
        "fecha": res["date"],
        "regimen": {"nombre": res["regime"]["label"], "descripcion": res["regime"]["desc"]},
        "tension_del_cuadro": res["tension"],
        "scores": {k: {"score": v["score"], "tendencia": v["trend_label"], "cobertura": v["coverage"]} for k, v in res["scores"].items()},
        "ayer": _yesterday_scores(),
        "sectores": [{"sector": s["label"], "sesgo": s["bias"], "por_que": [d["label"] for d in s["drivers"]], "que_esperar": s["behaviour"]}
                     for s in res["sectors"]],
        "divergencias": [{"series": f"{d['a']} (p{d['pct_a']:.0f}) vs {d['b']} (p{d['pct_b']:.0f})", "lectura": d["text"]} for d in res["divergences"]],
        "disparadores": [{"serie": t["series"], "valor": t["value"], "umbral": t["threshold"], "activado": t["hit"],
                          "distancia": t["distance"], "texto": t["text"]} for t in res["triggers"][:6]],
        "series_clave": series,
        "agenda_macro_7d": [{"fecha": c["date"], "publicacion": c["release"]} for c in calendar][:12],
        "resultados_7d": [{"fecha": str(e["date"]), "empresa": e.get("name"), "ticker": e.get("t"), "rol": e.get("role"),
                           "sector": e.get("sector"), "tipo": e.get("kind"), "bpa_esperado": e.get("eps_estimate")}
                          for e in week_events if e.get("kind") in ("resultados", "mercado")][:20],
    }


def micro_summary(m: dict, confl: list) -> dict:
    """Resumen compacto de la capa micro para el modelo: solo hechos, con fuente."""
    hechos = []
    for co in m["companies"]:
        for e in co["eventos"]:
            if e["importancia"] >= 2:
                hechos.append({"fecha": e["fecha"], "empresa": co["name"], "sector": co["sector"], "hecho": e["descripcion"]})
        if co.get("compra_cluster"):
            hechos.append({"fecha": m["date"], "empresa": co["name"], "sector": co["sector"],
                           "hecho": f"compras de {co['n_compradores']} insiders en 30 días ({co['importe_compras']:,.0f} USD)"})
        a = (co.get("revisiones") or {}).get("anual")
        if a and abs(a["net30"]) >= 0.6 and (a["up30"] + a["down30"]) >= 3:
            hechos.append({"fecha": m["date"], "empresa": co["name"], "sector": co["sector"],
                           "hecho": f"analistas {'suben' if a['net30'] > 0 else 'recortan'} estimaciones anuales ({a['up30']} arriba / {a['down30']} abajo, 30 días)"})
    return {
        "pulso_sectorial": {k: {"amplitud_revisiones_30d": v["amplitud_revisiones"], "mejorando": v["mejorando"], "empeorando": v["empeorando"]}
                            for k, v in m["sector_pulse"].items()},
        "conflictos_macro_micro": [{"sector": c["sector"], "sesgo_macro": c["macro"], "senal_micro": c["micro"]} for c in confl],
        "hechos_relevantes": hechos[:15],
        "bancos_centrales": [{"banco": s["banco"], "fecha": s["fecha"], "titulo": s["titulo"], "postura": s.get("postura"), "resumen": s.get("resumen")}
                             for s in m["central_banks"] if s.get("postura") is not None][:8],
    }


MAX_PAYLOAD_BYTES = 12_000   # Groq gratuito ~8.000 tokens/min por modelo contando prompt + max_tokens   # Groq gratuito: ~8.000 tokens/minuto por modelo; 14 KB de JSON ≈ 4.500 tokens


def _compact(o):
    """Redondea floats, elimina nulos y claves vacías para reducir el tamaño del JSON."""
    if isinstance(o, dict):
        return {k: _compact(v) for k, v in o.items() if v is not None and v != [] and v != {}}
    if isinstance(o, list):
        return [_compact(v) for v in o if v is not None]
    if isinstance(o, float):
        return round(o, 2)
    return o


def fit_payload(payload: dict) -> dict:
    """Recorta por prioridad hasta caber en MAX_PAYLOAD_BYTES; siempre conserva lo esencial."""
    p = _compact(payload)
    size = lambda d: len(json.dumps(d, ensure_ascii=False, default=str).encode("utf-8"))  # noqa: E731
    def trim(d, key, n, sub=None):
        obj = d.get(sub, {}) if sub else d
        if isinstance(obj.get(key), list):
            obj[key] = obj[key][:n]

    steps = [
        lambda d: d.get("fichas", {}).pop("momentum_sectorial", None),
        lambda d: d.pop("fichas", None),
        lambda d: d.get("pulso", {}).pop("variaciones", None),
        lambda d: trim(d, "candidatas", 6, "decision"),
        lambda d: trim(d, "casuisticas_activas", 5, "decision"),
        lambda d: [c.update({"que_hacer": c.get("que_hacer", "")[:260], "que_la_resuelve": c.get("que_la_resuelve", "")[:140]}) for c in d.get("decision", {}).get("casuisticas_activas", [])],
        lambda d: trim(d, "disparadores", 6),
        lambda d: d.__setitem__("series_clave", {k: v for k, v in d.get("series_clave", {}).items() if k in KEY_SERIES_SHORT}) if "series_clave" in d else None,
        lambda d: trim(d, "disparadores", 4, "decision") if False else trim(d.get("decision", {}).get("sensibilidad", {}), "disparadores", 3),
        lambda d: d.get("pulso", {}).pop("variaciones", None),
        lambda d: trim(d, "candidatas_en_sectores_favorecidos", 5, "fichas"),
        lambda d: trim(d, "hechos_relevantes", 5, "micro"),
        lambda d: trim(d, "resultados_7d", 6),
        lambda d: trim(d, "agenda_macro_7d", 6),
        lambda d: trim(d, "bancos_centrales", 3, "micro"),
        lambda d: d.pop("fichas", None),
        lambda d: trim(d, "hechos_relevantes", 0, "micro"),
        lambda d: d.pop("resultados_7d", None),
        lambda d: d.pop("pulso", None),
        lambda d: d.pop("cartera", None),
    ]
    for step in steps:
        if size(p) <= MAX_PAYLOAD_BYTES:
            break
        step(p)
    print(f"(narrativa: payload {size(p):,} bytes)")
    return p


def generate(payload: dict) -> str | None:
    from . import llm
    if not (os.environ.get("GROQ_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        print("(narrativa: sin GROQ_API_KEY ni GEMINI_API_KEY, se omite)")
        return None
    payload = fit_payload(payload)
    user = ("Redacta la nota de hoy a partir de este JSON y de nada más:\n\n```json\n"
            + json.dumps(payload, ensure_ascii=False, default=str) + "\n```")
    import re
    prohibidas = re.compile(r"\b(score|scores|percentil|percentiles|umbral|umbrales|disparador|disparadores|cobertura|json|payload|activado)\b", re.I)
    for intento in (1, 2):
        txt = llm.chat(SYSTEM, user, max_tokens=2400, temperature=0.2, reasoning="medium")
        if not txt or txt.count("## ") < 6:
            print(f"(narrativa: salida incompleta o vacía en el intento {intento})")
            continue
        hits = sorted(set(m.lower() for m in prohibidas.findall(txt)))
        if hits and intento == 1:
            print(f"(narrativa: usa vocabulario del sistema {hits}; reintento)")
            user = user + "\n\nRECORDATORIO: la nota anterior usó las palabras prohibidas " + ", ".join(hits) + ". Reescríbela sin ellas, en lenguaje económico, y revisa el signo de cada comparación."
            continue
        return txt
    return None


def save(text: str, date: str):
    DATA.mkdir(exist_ok=True)
    p = DATA / "narrativas.md"
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n\n# {date}\n\n{text}\n")


def to_html(md: str) -> str:
    """Conversión mínima de Markdown (##, viñetas, negrita) a HTML para el email."""
    out, in_list = [], False
    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            continue
        esc = _html.escape(s)
        # negrita **x**
        while "**" in esc:
            esc = esc.replace("**", "<b>", 1).replace("**", "</b>", 1)
        if s.startswith("## "):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<h4 style='margin:14px 0 4px'>{esc[3:]}</h4>")
        elif s.lstrip().startswith(("- ", "* ", "• ")):
            if not in_list:
                out.append("<ul style='margin:4px 0'>"); in_list = True
            out.append(f"<li>{esc.lstrip()[2:]}</li>")
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<p style='margin:4px 0'>{esc}</p>")
    if in_list:
        out.append("</ul>")
    return ("<h3>Nota del comité</h3><div style='background:#fbfbf7;border:1px solid #e6e2d3;border-radius:8px;"
            "padding:12px 16px;font-size:14px;line-height:1.5'>" + "\n".join(out) +
            "<p style='margin-top:10px;font-size:11px;color:#888'>Redactada por el modelo a partir del JSON del día; "
            "ninguna cifra procede de fuera del panel.</p></div>")
