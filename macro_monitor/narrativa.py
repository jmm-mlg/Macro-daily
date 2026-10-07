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

SYSTEM = """Eres el analista macro de un comité de inversión personal. Redactas la nota diaria en español,
para un inversor a medio plazo (meses) que invierte en acciones de EE.UU. y Europa.

REGLAS ESTRICTAS:
1. Usa ÚNICAMENTE los datos del JSON que recibes. No cites cifras, fechas ni hechos que no estén en él.
   Si una conclusión necesita un dato que no está, di "no disponible" en vez de inventarlo.
2. No des recomendaciones de compra o venta de valores concretos. Habla de sesgos, riesgos y qué vigilar.
3. Sé concreto y cuantitativo: cada afirmación lleva el dato económico que la sostiene (nivel y variación).
   Habla de la ECONOMÍA, no del sistema: nunca menciones "score", "cobertura", "JSON", "sesgo +1" ni
   "percentil" como palabras; traduce: "tipo real en máximos de la década", "nóminas +29k frente a +133k",
   "el petróleo encarece el consumo discrecional". El lector no sabe ni debe saber cómo se calculan los scores.
4. Prioriza: primero lo que ha cambiado, luego lo que más importa, luego lo accesorio.
5. Tono sobrio, sin adjetivos vacíos, sin relleno. Entre 280 y 450 palabras en total. Escribe las SEIS
   secciones completas (seis); no te detengas antes de la última.

FORMATO DE SALIDA (Markdown, exactamente estas seis secciones, con estos títulos):
## Qué ha cambiado
(2-3 frases. Si no hay ayer con qué comparar, dilo en una frase.)
## Lectura del cuadro
(3 viñetas máximo. Cada una: tesis en negrita + dato que la sostiene + implicación.)
## Esta semana
(2-3 frases que conecten los eventos de la agenda con el cuadro macro: qué dato o resultado puede confirmar o romper la lectura.)
## Empresas y bancos centrales
(Solo si el JSON trae la clave "micro". 2-4 frases: hechos relevantes, revisiones de analistas por sector, postura de los
bancos centrales, y sobre todo los CONFLICTOS entre el cuadro macro y lo que dicen los analistas. Si no hay "micro", escribe "Sin datos micro hoy.")
## Para la cartera
(2-3 frases sobre sesgos sectoriales y su fragilidad. Nombra solo sectores, no valores.)
## Qué cambiaría la conclusión
(2-3 disparadores concretos del JSON, con su umbral y distancia.)"""


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
                  "PAYEMS", "UNRATE", "ICSA", "RSAFS", "DGORDER", "UMCSENT", "MORTGAGE30US", "BAMLH0A0HYM2", "NFCI",
                  "ECBDFR", "CP0000EZ19M086NEST", "^GSPC", "^VIX", "DX-Y.NYB", "CL=F", "HG=F", "GC=F"]
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


def generate(payload: dict) -> str | None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("(narrativa: sin GROQ_API_KEY, se omite)")
        return None
    user = ("Redacta la nota de hoy a partir de este JSON y de nada más:\n\n```json\n"
            + json.dumps(payload, ensure_ascii=False, default=str) + "\n```")
    for model in MODELS:
        try:
            r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                              json={"model": model, "temperature": 0.3, "max_tokens": 3000, "reasoning_effort": "low",
                                    "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]},
                              timeout=90)
            r.raise_for_status()
            txt = r.json()["choices"][0]["message"]["content"].strip()
            if txt and txt.count("## ") >= 6:
                print(f"(narrativa generada con {model})")
                return txt
            print(f"(narrativa {model}: salida incompleta, {txt.count('## ')} secciones)")
        except Exception as e:  # noqa: BLE001
            print(f"(narrativa {model}: {e})")
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
