"""Decisión del día: todo lo que es regla se calcula aquí; el modelo solo redacta.

Bloques: banda de exposición (guía, nivel 5), sectores donde buscar y vetados, candidatas que pasan el embudo
(filtros 2 y 3) y lo que les falta, casuísticas activas con su "qué hacer" leído de la base de conocimiento,
sensibilidad de disparadores y de los datos de la semana (se vuelven a correr las reglas con el valor cruzado),
deltas frente a ayer y hace 5 días, historial del régimen y ficha de calidad de las candidatas.
"""
import re
import csv
import json
import copy
import datetime as dt
import pathlib

from . import rules

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
KB = ROOT / "kb"

EXPOSURE = {  # (régimen, tensión) -> (banda %, nuevas posiciones, factor de tamaño)
    ("goldilocks", "baja"): ("80-100", "sí, tamaño completo", 1.0), ("reflacion", "baja"): ("80-100", "sí, tamaño completo", 1.0),
    ("goldilocks", "media"): ("60-80", "sí: completo en sectores +2, mitad en +1", 0.75), ("reflacion", "media"): ("60-80", "sí: completo en sectores +2, mitad en +1", 0.75),
    ("mixto", "baja"): ("50-70", "solo con factores claros y micro a favor, mitad de tamaño", 0.5),
    ("mixto", "media"): ("50-70", "solo con factores claros y micro a favor, mitad de tamaño", 0.5),
    ("estanflacion", "baja"): ("30-50", "solo defensivos con pricing power y energía", 0.5), ("estanflacion", "media"): ("30-50", "solo defensivos con pricing power y energía", 0.5),
    ("desinflacion", "baja"): ("20-40", "solo calidad con caja neta; preparar lista para el pivot", 0.5), ("desinflacion", "media"): ("20-40", "solo calidad con caja neta; preparar lista para el pivot", 0.5),
}
BAD_8K = {"5.02", "4.02", "2.05", "2.06", "1.03", "2.04", "3.01", "5.01"}

# Detector -> casuística de la base (id de archivo en kb/casuisticas)
DIVERGENCE_KB = {("HG=F", "NEWORDER"): "cobre-sube-con-pedidos-cayendo", ("RSAFS", "UMCSENT"): "consumo-fuerte-con-confianza-baja",
                 ("^GSPC", "DFII10"): "bolsa-y-tipo-real-en-maximos", ("GC=F", "T10YIE"): "oro-cae-con-inflacion-alta",
                 ("PAYEMS", "ICSA"): "nominas-debiles-con-peticiones-bajas", ("BAMLH0A0HYM2", "^VIX"): "hy-sube-con-vix-bajo",
                 ("RSAFS", "RSCCAS"): "ventas-nominales-suben-por-gasolina", ("ICSA", "CCSA"): "continuadas-suben-con-iniciales-estables",
                 ("CU_AU", "DGS10"): "cobre-oro-y-10-anos"}
TRIGGER_KB = {"DGS10": "bono-supera-earnings-yield", "PAYEMS": "peticiones-superan-umbral", "ICSA": "peticiones-superan-umbral",
              "BAMLH0A0HYM2": "credito-avisa-antes-que-la-bolsa", "UNRATE": "regla-de-sahm-activada", "^VIX": "vix-sobre-25",
              "T10Y2Y": "curva-se-desinvierte", "JPY=X": "deshacer-del-carry", "PSAVERT": "consumo-financiado-con-credito",
              "DRCCLACBS": "consumo-financiado-con-credito", "PCEPILFE": "pce-por-encima-de-la-proyeccion-del-fomc", "CCSA": "continuadas-suben-con-iniciales-estables"}
PULSE_KB = {"valoracion": "bono-supera-earnings-yield", "tipos": "subida-rapida-del-10-anos", "mercado-liquidez": "liquidez-global-y-carry",
            "vix": "vix-sobre-25", "amplitud": "amplitud-estrecha-en-maximos"}
SIM_STEP = {"CPILFESL": 0.2, "CPIAUCSL": 0.3, "PCEPILFE": 0.2, "PAYEMS": 100, "UNRATE": 0.2, "RSAFS": 0.6, "GDPC1": 1.0, "ICSA": 30000, "PPIFIS": 0.5}


# ---------------------------------------------------------------- base de conocimiento
def kb_section(cid: str, section: str, limit: int = 650) -> str:
    p = KB / "casuisticas" / f"{cid}.md"
    if not p.exists():
        return ""
    t = p.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(section)}[^\n]*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if not m:
        return ""
    body = re.sub(r"\[\[([^\]]+)\]\]", r"\1", m.group(1)).strip()
    body = re.sub(r"\n{2,}", "\n", body)
    return body[:limit] + ("…" if len(body) > limit else "")


def kb_title(cid: str) -> str:
    p = KB / "casuisticas" / f"{cid}.md"
    if not p.exists():
        return cid
    m = re.search(r"^nombre:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else cid


def active_casuisticas(res: dict, pulso: dict | None, confl: list, momentum_conflicts: list) -> list:
    ids = []
    for d in res["divergences"]:
        cid = DIVERGENCE_KB.get((d["a"], d["b"])) or DIVERGENCE_KB.get((d["b"], d["a"]))
        if cid:
            ids.append((cid, f"señal cruzada {d['a']} vs {d['b']}"))
    for t in res["triggers"]:
        if t["hit"] and t["series"] in TRIGGER_KB:
            ids.append((TRIGGER_KB[t["series"]], f"disparador {t['series']} activado"))
    f = res["factors"]
    vix = (res.get("scores", {}).get("riesgo", {}).get("detail") or [])
    vix_val = next((x["value"] for x in vix if x["series"] == "^VIX"), None)
    if f.get("duracion", {}).get("signal") == 1 and vix_val is not None and vix_val < 16:
        ids.append(("vix-bajo-con-tipo-real-alto", "tipo real > 2 % con VIX < 16"))
    if f.get("dolar", {}).get("signal") == 1 and (f.get("petroleo", {}).get("signal") == 1 or f.get("cobre", {}).get("signal") == 1):
        ids.append(("dolar-fuerte-y-materias-primas", "dólar fuerte con materias primas caras"))
    if f.get("yen", {}).get("signal") == -1:
        ids.append(("deshacer-del-carry", "yen apreciándose > 4 en el mes"))
    for s in (pulso or {}).get("senales", []):
        cid = PULSE_KB.get(s["tipo"])
        if cid:
            ids.append((cid, s["texto"][:90]))
    if confl or momentum_conflicts:
        ids.append(("conflicto-macro-micro", "sesgo macro contra analistas o momentum"))
    if res["regime"]["key"] == "mixto" and not any(c == "nominas-debiles-con-peticiones-bajas" for c, _ in ids):
        ids.append(("nominas-debiles-con-peticiones-bajas", "régimen Mixto con crecimiento en disputa"))
    seen, out = set(), []
    for cid, why in ids:
        if cid in seen:
            continue
        seen.add(cid)
        out.append({"id": cid, "titulo": kb_title(cid), "por_que": why, "que_hacer": kb_section(cid, "Qué hacer"),
                    "que_la_resuelve": kb_section(cid, "Qué la resuelve", 350)})
    return out[:7]


# ---------------------------------------------------------------- sensibilidad
def _rerun(by_id: dict, sid: str, value: float, chg: float | None = None) -> dict:
    rows = copy.deepcopy(by_id)
    if sid not in rows or "value" not in rows[sid]:
        return None
    rows[sid]["value"] = value
    if chg is not None:
        rows[sid]["chg"] = chg
    return rules.run(rows)


def _diff(base: dict, alt: dict) -> dict:
    if alt is None:
        return {}
    out = {}
    if alt["regime"]["label"] != base["regime"]["label"]:
        out["regimen"] = f"{base['regime']['label']} → {alt['regime']['label']}"
    if alt["tension"] != base["tension"]:
        out["tension"] = f"{base['tension']} → {alt['tension']}"
    for k in base["scores"]:
        a, b = base["scores"][k]["score"], alt["scores"][k]["score"]
        if a != b:
            out[f"score_{k}"] = f"{a:+d} → {b:+d}"
    bb = {s["label"]: s["bias"] for s in base["sectors"]}
    for s in alt["sectors"]:
        if s["bias"] != bb.get(s["label"]):
            out[f"sector_{s['label']}"] = f"{bb.get(s['label']):+d} → {s['bias']:+d}"
    return out


def sensitivity(by_id: dict, res: dict, calendar: list, cfg: dict) -> dict:
    out = {"disparadores": [], "datos_semana": []}
    near = [t for t in res["triggers"] if not t["hit"]]
    near.sort(key=lambda t: abs(t["distance"]) / (abs(t["threshold"]) or 1))
    for t in near[:5]:
        thr = t["threshold"]
        eps = abs(thr) * 0.01 or 0.01
        val = thr + eps if (t["value"] < thr) else thr - eps
        d = _diff(res, _rerun(by_id, t["series"], val, chg=(val - t["value"])))
        out["disparadores"].append({"serie": t["series"], "umbral": thr, "valor_actual": t["value"], "si_se_cruza": d or {"sin_cambios": "no altera régimen ni sesgos; solo la lectura"}, "texto": t["text"]})
    # datos de la semana: ±1 paso en las series headline con publicación en 7 días
    rel_series = {}
    for r in cfg.get("calendar", {}).get("releases", []):
        for sid in r.get("series", []):
            rel_series[sid] = r["label"]
    upcoming = {c["release"] for c in calendar}
    for r in cfg.get("calendar", {}).get("releases", []):
        if not any(r["match"].lower() in u.lower() for u in upcoming):
            continue
        for sid in r.get("series", []):
            if sid not in SIM_STEP or sid not in by_id or "value" not in by_id[sid]:
                continue
            v, step = by_id[sid]["value"], SIM_STEP[sid]
            up, dn = _diff(res, _rerun(by_id, sid, v + step, step)), _diff(res, _rerun(by_id, sid, v - step, -step))
            out["datos_semana"].append({"publicacion": r["label"], "serie": sid, "valor_actual": v, "paso": step,
                                        "si_sube": up or {"sin_cambios": True}, "si_baja": dn or {"sin_cambios": True}})
    return out


# ---------------------------------------------------------------- historial y deltas
def _history():
    p = DATA / "scores.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def regime_history(res: dict) -> dict:
    h = _history()
    today = res["date"]
    prev = [r for r in h if r["date"] < today]
    if not prev:
        return {"dias_en_regimen": 1, "nota": "sin histórico anterior"}
    cur = res["regime"]["key"]
    days = 1
    for r in reversed(prev):
        if r["regime"] == cur:
            days += 1
        else:
            break
    last_change = next((r["date"] for r in reversed(prev) if r["regime"] != cur), None)
    seq = []
    for r in prev[-90:] + [{"date": today, "regime": cur}]:
        if not seq or seq[-1]["regimen"] != r["regime"]:
            seq.append({"desde": r["date"], "regimen": r["regime"]})
    traj = {}
    for k in ("crecimiento", "inflacion", "liquidez", "riesgo"):
        vals = [int(r[k]) for r in prev if r.get(k) not in (None, "")]
        now = res["scores"][k]["score"]
        traj[k] = {"hoy": now, "hace_5d": vals[-5] if len(vals) >= 5 else None, "hace_20d": vals[-20] if len(vals) >= 20 else None}
    return {"dias_en_regimen": days, "ultimo_cambio": last_change, "secuencia_90d": seq[-6:], "trayectoria_scores": traj}


def deltas(res: dict, cand_now: list) -> dict:
    h = _history()
    today = res["date"]
    prev = [r for r in h if r["date"] < today]
    out = {"vs_ayer": {}, "vs_5d": {}}
    for label, idx in (("vs_ayer", -1), ("vs_5d", -5)):
        if len(prev) < abs(idx):
            continue
        r = prev[idx]
        d = {"fecha": r["date"]}
        if r["regime"] != res["regime"]["key"]:
            d["regimen"] = f"{r['regime']} → {res['regime']['key']}"
        if r.get("tension") != res["tension"]:
            d["tension"] = f"{r.get('tension')} → {res['tension']}"
        for k in ("crecimiento", "inflacion", "liquidez", "riesgo"):
            try:
                if int(r[k]) != res["scores"][k]["score"]:
                    d[f"score_{k}"] = f"{int(r[k]):+d} → {res['scores'][k]['score']:+d}"
            except (ValueError, KeyError):
                pass
        try:
            old = json.loads(r["sectors_json"])
            for s in res["sectors"]:
                if old.get(s["sector"]) is not None and old[s["sector"]] != s["bias"]:
                    d[f"sector_{s['label']}"] = f"{old[s['sector']]:+d} → {s['bias']:+d}"
        except (json.JSONDecodeError, KeyError):
            pass
        out[label] = d
    # disparadores: distancia frente a ayer (data/triggers.csv, lo escribe rules.save_history desde hoy)
    p = DATA / "triggers.csv"
    if p.exists():
        with p.open(encoding="utf-8") as f:
            rows = [x for x in csv.DictReader(f) if x["date"] < today]
        if rows:
            last_date = rows[-1]["date"]
            old = {x["series"]: float(x["distance"]) for x in rows if x["date"] == last_date}
            mv = []
            for t in res["triggers"]:
                o = old.get(t["series"])
                if o is not None and abs(o - t["distance"]) > 1e-9:
                    rel = (t["distance"] - o) / (abs(t["threshold"]) or 1) * 100
                    if abs(rel) >= 1:
                        mv.append({"serie": t["series"], "distancia_antes": o, "distancia_hoy": t["distance"], "se_acerca": abs(t["distance"]) < abs(o)})
            out["disparadores_que_se_mueven"] = mv[:6]
    return out


# ---------------------------------------------------------------- candidatas
def _quality(tickers: list) -> dict:
    """PER adelantado/trailing, margen bruto, deuda neta/EBITDA para pocas empresas (yfinance info)."""
    import yfinance as yf
    out = {}
    for t in tickers[:8]:
        try:
            i = yf.Ticker(t).info
            debt, cash, ebitda = i.get("totalDebt"), i.get("totalCash"), i.get("ebitda")
            nd = None if not (debt is not None and cash is not None and ebitda) else (debt - cash) / ebitda
            out[t] = {"per_adelantado": i.get("forwardPE"), "per_trailing": i.get("trailingPE"), "margen_bruto_pct": None if i.get("grossMargins") is None else round(i["grossMargins"] * 100, 1),
                      "deuda_neta_ebitda": None if nd is None else round(nd, 2), "fcf_yield_pct": None if not (i.get("freeCashflow") and i.get("marketCap")) else round(i["freeCashflow"] / i["marketCap"] * 100, 1)}
        except Exception as e:  # noqa: BLE001
            print(f"(calidad {t}: {e})")
    return out


def candidates(res: dict, fichas: dict | None, micro: dict | None, allowed: set, vetoed: set, size_factor: float) -> list:
    if not fichas:
        return []
    rev = {c["t"]: c for c in (micro or {}).get("companies", [])}
    out = []
    for f in fichas["fichas"]:
        if f["sector"] not in allowed:
            continue
        checks, missing = [], []
        r = (rev.get(f["t"], {}).get("revisiones") or {}).get("anual")
        if r is None:
            checks.append("revisiones: sin dato")
        elif r["up30"] >= r["down30"] and (r["up30"] + r["down30"]) > 0:
            checks.append(f"revisiones {r['up30']}↑/{r['down30']}↓ ok")
        else:
            missing.append(f"revisiones {r['up30']}↑/{r['down30']}↓")
        bad = [e for e in rev.get(f["t"], {}).get("eventos", []) if set(e["codigos"]) & BAD_8K]
        if bad:
            missing.append(f"8-K negativo ({bad[0]['descripcion'][:30]})")
        if f["dias_a_resultados"] is not None and f["dias_a_resultados"] <= 5:
            missing.append(f"resultados en {f['dias_a_resultados']} días")
        if not f["sobre_ma200"]:
            missing.append("bajo la media de 200")
        if not f["cabe"]:
            missing.append(f"stop a {f['stop_dist_pct']:.1f} % (> 8 %)")
        if f["rel_3m"] is not None and f["rel_3m"] < -3:
            missing.append(f"fuerza relativa {f['rel_3m']:+.1f} pp")
        pasa = not missing
        out.append({"ticker": f["t"], "empresa": f["name"], "sector": f["sector"], "region": f["region"], "role": f["role"],
                    "pasa_filtro_3": pasa, "le_falta": missing if missing else ["disparador con fecha (filtro 4)"],
                    "precio": round(f["precio"], 2), "moneda": f["moneda"], "stop": round(f["stop"], 2), "stop_dist_pct": round(f["stop_dist_pct"], 1),
                    "acciones": int(f["acciones"] * size_factor) if f["cabe"] else 0, "importe": round(f["importe"] * size_factor) if f["cabe"] else 0,
                    "rel_3m": None if f["rel_3m"] is None else round(f["rel_3m"], 1), "dias_a_resultados": f["dias_a_resultados"]})
    out.sort(key=lambda c: (not c["pasa_filtro_3"], c["role"] != "bellwether", -(c["rel_3m"] or -99)))
    return out[:12]


# ---------------------------------------------------------------- orquestación
def build(cfg: dict, by_id: dict, res: dict, fichas: dict | None, micro: dict | None, confl: list, pulso: dict | None, calendar: list, cartera: dict | None) -> dict:
    tension = res["tension"] if res["tension"] in ("baja", "media") else "media"
    key = (res["regime"]["key"], tension)
    if res["tension"] == "alta":
        banda, nuevas, factor = "40-60", "solo en sectores +2 con micro a favor, mitad de tamaño", 0.5
    else:
        banda, nuevas, factor = EXPOSURE.get(key, ("50-70", "mitad de tamaño", 0.5))
    mom_confl = [m for m in (fichas or {}).get("momentum", []) if m["conflicto"]]
    confl_sectors = {c["sector"] for c in confl} | {m["sector"] for m in mom_confl if m["sesgo_motor"] >= 1}
    allowed = {s["label"] for s in res["sectors"] if s["bias"] >= 1 and s["label"] not in confl_sectors}
    vetoed = [{"sector": s["label"], "motivo": f"sesgo {s['bias']:+d}"} for s in res["sectors"] if s["bias"] <= -1]
    vetoed += [{"sector": sec, "motivo": "conflicto macro/micro o sesgo contra momentum"} for sec in confl_sectors if sec not in {v["sector"] for v in vetoed}]
    cands = candidates(res, fichas, micro, allowed, {v["sector"] for v in vetoed}, factor)
    quality = _quality([c["ticker"] for c in cands if c["pasa_filtro_3"]][:6]) if cands else {}
    for c in cands:
        c["calidad"] = quality.get(c["ticker"])
    cas = active_casuisticas(res, pulso, confl, mom_confl)
    sens = sensitivity(by_id, res, calendar, cfg)
    hist = regime_history(res)
    dl = deltas(res, cands)
    abre_hoy = bool([c for c in cands if c["pasa_filtro_3"]]) and res["regime"]["key"] != "mixto"
    acciones_cartera = []
    for p in (cartera or {}).get("posiciones", []):
        if p["avisos"]:
            acciones_cartera.append({"ticker": p["ticker"], "avisos": p["avisos"], "R": p["R"], "dist_stop_pct": round(p["dist_stop_pct"], 1)})
    return {
        "date": res["date"],
        "exposicion": {"banda_pct": banda, "nuevas_posiciones": nuevas, "factor_tamano": factor, "posicion_max_pct": (fichas or {}).get("posicion_max_pct"),
                       "motivo": f"régimen {res['regime']['label']} con tensión {res['tension']} (tabla del nivel 5 de la guía)"},
        "abrir_hoy": {"respuesta": "sí, si hay disparador" if abre_hoy else "no", "motivo": ("hay candidatas que pasan el filtro 3 en régimen con señal" if abre_hoy else
                      ("régimen Mixto: esperar o mitad de tamaño solo con disparador y micro a favor" if res["regime"]["key"] == "mixto" else "ninguna candidata pasa el filtro 3"))},
        "sectores_donde_buscar": sorted(allowed), "sectores_vetados": vetoed,
        "candidatas": cands, "casuisticas_activas": cas, "sensibilidad": sens, "historial_regimen": hist, "cambios": dl,
        "cartera_acciones": acciones_cartera,
        "que_no_hacer": [f"No abrir en {v['sector']} ({v['motivo']})" for v in vetoed[:4]] + (["No aumentar exposición agregada con la prima de riesgo comprimida"] if any(s["tipo"] == "valoracion" for s in (pulso or {}).get("senales", [])) else []),
    }


def save(d: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "decision.json").write_text(json.dumps(d, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


# ---------------------------------------------------------------- email
def to_html(d: dict, kb_url: str = "") -> str:
    def kb(cid):
        return f"<a href='{kb_url}/casuisticas/{cid}/'>{kb_title(cid)}</a>" if kb_url and "github.com" not in kb_url else kb_title(cid)
    e = d["exposicion"]
    h = ["<h3>Decisión del día <span style='font-size:12px;color:#999;font-weight:normal'>(calculada por el motor)</span></h3>"]
    h.append(f"<table cellpadding='5' style='border-collapse:collapse'><tr><td style='border:1px solid #ddd'><b>Exposición objetivo</b><br>{e['banda_pct']} %</td>"
             f"<td style='border:1px solid #ddd'><b>¿Abrir hoy?</b><br>{d['abrir_hoy']['respuesta']}</td>"
             f"<td style='border:1px solid #ddd'><b>Nuevas posiciones</b><br>{e['nuevas_posiciones']}</td>"
             f"<td style='border:1px solid #ddd'><b>Dónde buscar</b><br>{', '.join(d['sectores_donde_buscar']) or 'ningún sector'}</td></tr></table>")
    h.append(f"<p style='font-size:12px;color:#666'>{e['motivo']}. {d['abrir_hoy']['motivo'].capitalize()}.</p>")
    if d["que_no_hacer"]:
        h.append("<p><b>Qué no hacer:</b> " + "; ".join(d["que_no_hacer"]) + ".</p>")
    # cambios
    ch = d["cambios"]
    txt = []
    for lab, dd in (("vs ayer", ch.get("vs_ayer", {})), ("vs hace 5 días", ch.get("vs_5d", {}))):
        items = [f"{k.replace('_', ' ')}: {v}" for k, v in dd.items() if k != "fecha"]
        if items:
            txt.append(f"<b>{lab}</b>: " + "; ".join(items))
    mv = ch.get("disparadores_que_se_mueven", [])
    if mv:
        txt.append("<b>disparadores</b>: " + ", ".join(f"{m['serie']} {'se acerca' if m['se_acerca'] else 'se aleja'} ({m['distancia_antes']:.2f} → {m['distancia_hoy']:.2f})" for m in mv))
    h.append("<p style='font-size:12px'>" + ("<br>".join(txt) if txt else "Sin cambios de régimen, scores ni sesgos frente a ayer.") + "</p>")
    hr = d["historial_regimen"]
    if hr.get("ultimo_cambio"):
        h.append(f"<p style='font-size:12px;color:#666'>Régimen actual desde hace {hr['dias_en_regimen']} días (último cambio: {hr['ultimo_cambio']}).</p>")
    # candidatas
    if d["candidatas"]:
        h.append("<h4 style='margin:10px 0 4px'>Candidatas (embudo, filtros 2-3) y lo que les falta</h4><table cellpadding='4' style='border-collapse:collapse;width:100%;font-size:12px'>"
                 "<tr style='background:#f0f0f0'><th align='left'>Empresa</th><th>Pasa</th><th align='left'>Le falta</th><th align='right'>Precio</th><th align='right'>Stop</th><th align='right'>Acc.</th><th align='right'>Importe</th><th align='right'>PER adel.</th><th align='right'>Margen bruto</th><th align='right'>Deuda/EBITDA</th></tr>")
        for c in d["candidatas"]:
            q = c.get("calidad") or {}
            fmt = lambda v, s="": "—" if v is None else f"{v:.1f}{s}"  # noqa: E731
            style = " style='background:#f3fff3'" if c["pasa_filtro_3"] else ""
            h.append(f"<tr{style}><td><b>{c['empresa']}</b> <span style='color:#999'>{c['ticker']} · {c['sector'][:12]}</span></td><td align='center'>{'✔' if c['pasa_filtro_3'] else '✘'}</td>"
                     f"<td>{'; '.join(c['le_falta'])}</td><td align='right'>{c['precio']} {c['moneda']}</td><td align='right'>{c['stop']} ({c['stop_dist_pct']} %)</td>"
                     f"<td align='right'>{c['acciones'] or '—'}</td><td align='right'>{c['importe']:,} $</td><td align='right'>{fmt(q.get('per_adelantado'))}</td>"
                     f"<td align='right'>{fmt(q.get('margen_bruto_pct'), ' %')}</td><td align='right'>{fmt(q.get('deuda_neta_ebitda'))}</td></tr>".replace(",", "."))
        h.append("</table>")
    # casuísticas
    if d["casuisticas_activas"]:
        h.append("<h4 style='margin:10px 0 4px'>Casuísticas activas (base de conocimiento)</h4><ul style='font-size:12px'>")
        for c in d["casuisticas_activas"]:
            h.append(f"<li><b>{kb(c['id'])}</b> <span style='color:#999'>({c['por_que']})</span>" + (f"<br><span style='color:#555'>{c['que_hacer'][:260]}…</span>" if c["que_hacer"] else "") + "</li>")
        h.append("</ul>")
    # sensibilidad
    s = d["sensibilidad"]
    if s["disparadores"] or s["datos_semana"]:
        h.append("<h4 style='margin:10px 0 4px'>Si se cruza… (sensibilidad calculada)</h4><table cellpadding='4' style='border-collapse:collapse;width:100%;font-size:12px'>")
        for t in s["disparadores"]:
            cambios = "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in t["si_se_cruza"].items())
            h.append(f"<tr><td style='white-space:nowrap'><b>{t['serie']}</b> {t['valor_actual']:.2f} → {t['umbral']:.2f}</td><td>{cambios}</td></tr>")
        for x in s["datos_semana"]:
            up = "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in x["si_sube"].items() if k != "sin_cambios") or "sin cambios"
            dn = "; ".join(f"{k.replace('_', ' ')}: {v}" for k, v in x["si_baja"].items() if k != "sin_cambios") or "sin cambios"
            h.append(f"<tr><td style='white-space:nowrap'><b>{x['publicacion']}</b> ({x['serie']} ±{x['paso']})</td><td>↑ {up}<br>↓ {dn}</td></tr>")
        h.append("</table>")
    return "\n".join(h)


def summary_for_llm(d: dict) -> dict:
    return {
        "exposicion": d["exposicion"], "abrir_hoy": d["abrir_hoy"], "sectores_donde_buscar": d["sectores_donde_buscar"],
        "sectores_vetados": d["sectores_vetados"], "que_no_hacer": d["que_no_hacer"],
        "candidatas": [{k: c[k] for k in ("ticker", "empresa", "sector", "pasa_filtro_3", "le_falta", "stop_dist_pct", "acciones", "importe", "rel_3m", "dias_a_resultados", "calidad")} for c in d["candidatas"][:8]],
        "casuisticas_activas": [{"titulo": c["titulo"], "por_que": c["por_que"], "que_hacer": c["que_hacer"][:450], "que_la_resuelve": c["que_la_resuelve"][:250]} for c in d["casuisticas_activas"]],
        "sensibilidad": d["sensibilidad"], "historial_regimen": d["historial_regimen"], "cambios": d["cambios"], "cartera_acciones": d["cartera_acciones"],
    }
