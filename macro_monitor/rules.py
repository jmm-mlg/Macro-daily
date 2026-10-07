"""Motor de reglas: scores, régimen, sesgo por sector, divergencias, disparadores e histórico.

Entrada: `rows` = {id: {value, chg, pct, date, ...}} que produce run.build_rows.
Todo umbral vive en rules.yaml; aquí solo hay mecánica.
"""
import csv
import json
import datetime as dt
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load_rules() -> dict:
    return yaml.safe_load((ROOT / "rules.yaml").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- señales
def _get(rows, sid):
    r = rows.get(sid) or {}
    return r if "value" in r else None


def _level_signal(r, lv: dict) -> int:
    v, p = r["value"], r.get("pct")
    if "above" in lv and v > lv["above"]:
        return 1
    if "below" in lv and v < lv["below"]:
        return -1
    if p is not None:
        if "pct_high" in lv and p >= lv["pct_high"]:
            return 1
        if "pct_low" in lv and p <= lv["pct_low"]:
            return -1
    return 0


def _trend_signal(r, tr: dict) -> int:
    c = r.get("chg")
    if c is None:
        return 0
    dead = tr.get("dead", 0)
    return 1 if c > dead else -1 if c < -dead else 0


def _clamp(x, lo=-2, hi=2):
    return max(lo, min(hi, x))


def compute_scores(rows: dict, rules: dict) -> dict:
    out = {}
    for key, sc in rules["scores"].items():
        total, wsum, detail = 0.0, 0.0, []
        for sg in sc["signals"]:
            r = _get(rows, sg["series"])
            if r is None:
                continue
            lvl = _level_signal(r, sg.get("level", {}))
            trd = _trend_signal(r, sg.get("trend", {}))
            s = lvl + trd
            if sg.get("invert"):
                s = -s
            w = sg.get("weight", 1)
            total += w * s
            wsum += w
            detail.append({"series": sg["series"], "level": lvl, "trend": trd, "signal": s, "weight": w,
                           "value": r["value"], "pct": r.get("pct")})
        raw = (total / (2 * wsum)) * 2 if wsum else 0.0  # cada señal vale como mucho ±2
        score = int(round(_clamp(raw)))
        # tendencia agregada: media de las señales de tendencia (ponderada)
        tsum = sum(d["weight"] * (-d["trend"] if next(s for s in sc["signals"] if s["series"] == d["series"]).get("invert") else d["trend"]) for d in detail)
        trend = tsum / wsum if wsum else 0
        up, down = ("subiendo", "bajando") if key == "inflacion" else ("mejorando", "empeorando")
        out[key] = {"label": sc["label"], "score": score, "raw": round(raw, 2), "trend": round(trend, 2),
                    "trend_label": up if trend > 0.15 else down if trend < -0.15 else "estable",
                    "coverage": f"{len(detail)}/{len(sc['signals'])}", "detail": detail}
    return out


def compute_regime(scores: dict, rules: dict) -> dict:
    g = scores.get("crecimiento", {}).get("score", 0)
    i = scores.get("inflacion", {}).get("score", 0)
    gs = 1 if g > 0 else -1 if g < 0 else 0
    is_ = 1 if i > 0 else -1 if i < 0 else 0
    for key, rg in rules["regimes"].items():
        if rg["growth"] == gs and rg["inflation"] == is_:
            return {"key": key, **rg, "g": g, "i": i}
    rg = rules["regimes"]["mixto"]
    return {"key": "mixto", **rg, "g": g, "i": i}


# ---------------------------------------------------------------- factores y sectores
def compute_factors(rows: dict, rules: dict) -> dict:
    out = {}
    for key, f in rules["factors"].items():
        r = _get(rows, f["series"])
        if r is None:
            out[key] = {"signal": 0, "label": f["label"], "value": None}
            continue
        sg, v, p, c = f["signal"], r["value"], r.get("pct"), r.get("chg")
        s = 0
        if "above" in sg and v > sg["above"]:
            s = 1
        elif "below" in sg and v < sg["below"]:
            s = -1
        elif "pct_high" in sg and p is not None and p >= sg["pct_high"]:
            s = 1
        elif "pct_low" in sg and p is not None and p <= sg["pct_low"]:
            s = -1
        if s == 0 and c is not None:
            if "chg_above" in sg and c > sg["chg_above"]:
                s = 1
            elif "chg_below" in sg and c < sg["chg_below"]:
                s = -1
        out[key] = {"signal": s, "label": f["label"], "value": v, "pct": p, "chg": c, "why": f.get("why", "")}
    return out


def compute_sectors(regime: dict, factors: dict, rules: dict) -> list:
    col = {"goldilocks": 0, "reflacion": 1, "estanflacion": 2, "desinflacion": 3}.get(regime["key"])
    out = []
    for sec, row in rules["sector_matrix"].items():
        base = row[col] if col is not None else 0
        adj, drivers = 0.0, []
        for fk, load in rules["sector_factor_loadings"].get(sec, {}).items():
            s = factors.get(fk, {}).get("signal", 0)
            if load and s:
                a = load * s
                adj += a
                drivers.append({"factor": fk, "label": factors[fk]["label"], "effect": a})
        bias = int(round(_clamp(base + adj)))
        if base:
            drivers.insert(0, {"factor": "regimen", "label": f"Régimen {regime['label']}", "effect": base})
        beh = rules.get("sector_behaviour", {}).get(sec, {}).get(regime["key"], "")
        out.append({"sector": sec, "label": rules["sector_labels"][sec], "bias": bias, "base": base,
                    "adjustment": round(adj, 1), "drivers": drivers, "behaviour": beh})
    out.sort(key=lambda x: (-x["bias"], x["label"]))
    return out


# ---------------------------------------------------------------- divergencias y disparadores
def compute_divergences(rows: dict, rules: dict) -> list:
    out = []
    for d in rules.get("divergences", []):
        a, b = _get(rows, d["a"]), _get(rows, d["b"])
        if a is None or b is None or a.get("pct") is None or b.get("pct") is None:
            continue
        pa, pb = a["pct"], b["pct"]
        pb_shown = pb
        if d.get("invert_b"):
            pb = 100 - pb
        if d.get("same_direction"):
            # aviso cuando AMBOS están en percentil extremo alto (gap negativo = umbral de proximidad)
            if pa >= 85 and pb >= 85:
                out.append({**d, "pct_a": pa, "pct_b": pb_shown, "kind": "coincidencia"})
        elif abs(pa - pb) > d["gap"]:
            out.append({**d, "pct_a": pa, "pct_b": pb_shown, "kind": "divergencia"})
    return out


def compute_triggers(rows: dict, rules: dict) -> list:
    out = []
    for t in rules.get("triggers", []):
        r = _get(rows, t["series"])
        if r is None:
            continue
        v = r["value"]
        if "above" in t:
            thr, hit, dist = t["above"], v > t["above"], t["above"] - v
        else:
            thr, hit, dist = t["below"], v < t["below"], v - t["below"]
        out.append({"series": t["series"], "threshold": thr, "value": v, "hit": hit,
                    "distance": round(dist, 2), "text": t["text"]})
    out.sort(key=lambda x: (not x["hit"], abs(x["distance"]) / (abs(x["threshold"]) or 1)))
    return out


# ---------------------------------------------------------------- orquestación
def run(rows: dict) -> dict:
    rules = load_rules()
    scores = compute_scores(rows, rules)
    regime = compute_regime(scores, rules)
    factors = compute_factors(rows, rules)
    sectors = compute_sectors(regime, factors, rules)
    liq = scores.get("liquidez", {}).get("score", 0)
    risk = scores.get("riesgo", {}).get("score", 0)
    tension = "alta" if (liq <= -1 and risk >= 1) else "media" if (liq <= -1 or risk >= 2) else "baja"
    return {
        "date": dt.date.today().isoformat(),
        "scores": scores,
        "regime": regime,
        "tension": tension,
        "factors": factors,
        "sectors": sectors,
        "divergences": compute_divergences(rows, rules),
        "triggers": compute_triggers(rows, rules),
    }


# ---------------------------------------------------------------- histórico
def save_history(rows: dict, result: dict):
    """Snapshots diarios: data/history.csv (series), data/scores.csv (scores+régimen+sectores), data/latest.json."""
    DATA.mkdir(exist_ok=True)
    today = result["date"]

    def _append(path, header, lines):
        new = not path.exists()
        existing = set()
        if not new:
            with path.open(encoding="utf-8") as f:
                existing = {tuple(l.split(",")[:2]) for l in f.read().splitlines()[1:]}
        with path.open("a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(header)
            for ln in lines:
                if (str(ln[0]), str(ln[1])) not in existing:
                    w.writerow(ln)

    _append(DATA / "history.csv", ["date", "id", "value", "chg", "pct", "obs_date"],
            [[today, sid, round(r["value"], 4), None if r.get("chg") is None else round(r["chg"], 4),
              None if r.get("pct") is None else round(r["pct"], 1), r.get("date")]
             for sid, r in rows.items() if "value" in r])

    sec = {s["sector"]: s["bias"] for s in result["sectors"]}
    _append(DATA / "scores.csv",
            ["date", "regime", "crecimiento", "inflacion", "liquidez", "riesgo", "tension", "sectors_json"],
            [[today, result["regime"]["key"], result["scores"]["crecimiento"]["score"], result["scores"]["inflacion"]["score"],
              result["scores"]["liquidez"]["score"], result["scores"]["riesgo"]["score"], result["tension"],
              json.dumps(sec, ensure_ascii=False)]])

    slim = {sid: {k: r.get(k) for k in ("value", "chg", "pct", "date", "name", "block", "unit")} for sid, r in rows.items() if "value" in r}
    (DATA / "latest.json").write_text(json.dumps({"series": slim, "analysis": result}, ensure_ascii=False, indent=1, default=str),
                                      encoding="utf-8")


def regime_history(n: int = 90) -> list:
    p = DATA / "scores.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[-n:]
