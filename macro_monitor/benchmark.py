"""Benchmarks de industria (kb/benchmarks/benchmarks.yaml, de Damodaran) y comparación de una empresa con su industria."""
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH = ROOT / "kb" / "benchmarks" / "benchmarks.yaml"
_cache = None

# métrica nuestra -> (campo de yfinance info, transformación, sentido: 1 = más alto es mejor, -1 = más bajo es mejor (valoración))
FIELDS = {
    "per_adelantado": ("forwardPE", 1, -1), "per_trailing": ("trailingPE", 1, -1), "ev_ebitda": ("enterpriseToEbitda", 1, -1),
    "margen_bruto": ("grossMargins", 100, 1), "margen_operativo": ("operatingMargins", 100, 1), "margen_neto": ("profitMargins", 100, 1),
    "roe": ("returnOnEquity", 100, 1), "rentabilidad_dividendo": ("dividendYield", 1, 0), "beta": ("beta", 1, 0),
}
LABEL = {"per_adelantado": "PER adel.", "per_trailing": "PER", "ev_ebitda": "EV/EBITDA", "margen_bruto": "margen bruto", "margen_operativo": "margen op.",
         "margen_neto": "margen neto", "roe": "ROE", "deuda_ebitda": "deuda/EBITDA", "rentabilidad_dividendo": "dividendo", "beta": "beta"}


def load() -> dict:
    global _cache
    if _cache is None:
        _cache = yaml.safe_load(PATH.read_text(encoding="utf-8")) if PATH.exists() else {}
    return _cache


def industry_bench(region: str, sector: str, industry: str) -> dict | None:
    b = load().get("regiones", {}).get(region, {}).get(sector, {})
    return b.get(industry)


def company_metrics(info: dict) -> dict:
    """Extrae de yfinance.info las métricas comparables, en las mismas unidades que el benchmark."""
    out = {}
    for metric, (field, scale, _) in FIELDS.items():
        v = info.get(field)
        if v is not None and v == v:
            v = float(v) * scale
            if metric == "rentabilidad_dividendo" and v < 0.5:   # yfinance a veces lo da en tanto por uno
                v *= 100
            out[metric] = v
    debt, cash, ebitda = info.get("totalDebt"), info.get("totalCash"), info.get("ebitda")
    if debt is not None and ebitda:
        out["deuda_ebitda"] = (debt - (cash or 0)) / ebitda
    if info.get("freeCashflow") and info.get("marketCap"):
        out["fcf_yield"] = info["freeCashflow"] / info["marketCap"] * 100
    return out


def compare(metrics: dict, bench: dict) -> dict:
    """Para cada métrica: valor, mediana de la industria, rango 10a y posición (muy_bajo / bajo / medio / alto / muy_alto)."""
    out = {}
    for metric, v in metrics.items():
        ref = bench.get(metric) if bench else None
        if not ref:
            out[metric] = {"valor": round(v, 2)}
            continue
        med, p25, p75 = ref.get("actual"), ref.get("p25"), ref.get("p75")
        if not med:
            out[metric] = {"valor": round(v, 2), "industria": med}
            continue
        r = v / med if med > 0 else None
        pos = ("muy_bajo" if r is not None and r < 0.65 else "bajo" if r is not None and r < 0.85 else
               "alto" if r is not None and r > 1.35 else "medio_alto" if r is not None and r > 1.15 else "medio")
        # dónde está la mediana actual de la industria respecto a su propia década
        hist = None
        if p25 is not None and p75 is not None:
            hist = "industria cara vs su década" if med > p75 else "industria barata vs su década" if med < p25 else "industria en su rango"
        out[metric] = {"valor": round(v, 2), "industria": med, "p25": p25, "p75": p75, "posicion": pos, "industria_vs_decada": hist}
    return out


def read(comp: dict) -> str:
    """Lectura breve: valoración frente a la industria y calidad."""
    val, qual = [], []
    for m in ("per_adelantado", "ev_ebitda"):
        c = comp.get(m)
        if c and "posicion" in c:
            val.append(f"{LABEL[m]} {c['valor']:.1f} vs {c['industria']:.1f}")
    ratios = [comp[m]["valor"] / comp[m]["industria"] for m in ("per_adelantado", "ev_ebitda") if comp.get(m, {}).get("industria") and comp[m]["valor"] > 0]
    r = sum(ratios) / len(ratios) if ratios else None
    v_txt = ("sin múltiplos comparables" if r is None else "claramente barata frente a su industria" if r < 0.7 else "barata frente a su industria" if r < 0.85 else
             "claramente cara frente a su industria" if r > 1.4 else "cara frente a su industria" if r > 1.15 else "en línea con su industria")
    for m in ("margen_operativo", "roe"):
        c = comp.get(m)
        if c and "posicion" in c:
            qual.append(f"{LABEL[m]} {c['valor']:.0f} % vs {c['industria']:.0f} % ({c['posicion'].replace('_', ' ')})")
    d = comp.get("deuda_ebitda")
    if d and "posicion" in d:
        qual.append(f"deuda/EBITDA {d['valor']:.1f} vs {d['industria']:.1f}")
    dec = comp.get("per_adelantado", {}).get("industria_vs_decada") or comp.get("ev_ebitda", {}).get("industria_vs_decada")
    return v_txt + ("; " + ", ".join(val) if val else "") + (f" ({dec})" if dec else "") + (". Calidad: " + "; ".join(qual) if qual else "")
