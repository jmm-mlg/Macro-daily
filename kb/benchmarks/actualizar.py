"""Benchmarks de valoración por industria a partir de los datos de Damodaran (NYU Stern), EE.UU. y Europa.

Descarga los archivos actuales (pc/datasets/<nombre>.xls, publicados cada enero) y el archivo histórico
(pc/archives/<nombre><aa>.xls, 2016-2024), agrega las industrias de Damodaran a las de la watchlist según
kb/benchmarks/correspondencia.yaml (ponderando por número de empresas), calcula mediana actual y rango
histórico (p25-p75, mínimo, máximo) y escribe:
  - kb/benchmarks/benchmarks.yaml      (lo lee el motor: score predictivo y ficha de calidad)
  - kb/benchmarks/<sector>.md          (11 entradas legibles de la base de conocimiento)
  - kb/benchmarks/_fuente_damodaran.csv (todas las industrias de Damodaran, por región y año, para auditoría)
Uso: python kb/benchmarks/actualizar.py [--sin-historico]
"""
import io
import re
import sys
import json
import datetime as dt
import pathlib
import unicodedata

import requests
import pandas as pd
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
HERE = ROOT / "kb" / "benchmarks"
BASE = "https://pages.stern.nyu.edu/~adamodar/pc/"
H = {"User-Agent": "Mozilla/5.0 (macro-monitor; benchmarks de industria)"}
REGIONS = {"US": "", "EU": "Europe"}
YEARS_HIST = list(range(2016, 2025))            # archivo disponible; 2025 no está publicado
CURRENT_YEAR = 2026

# archivo -> {columna Damodaran (texto a buscar en la cabecera): métrica nuestra}
DATASETS = {
    # PER trailing: agregado capitalización / beneficio de las empresas rentables (la media simple se dispara con PER de 500)
    "pedata": {"Aggregate Mkt Cap/ Trailing Net Income": "per_trailing", "Forward PE": "per_adelantado", "Expected growth - next 5 years": "crecimiento_esperado_5a", "PEG Ratio": "peg"},
    "margin": {"Gross Margin": "margen_bruto", "Pre-tax Unadjusted Operating Margin": "margen_operativo", "Net Margin": "margen_neto", "EBITDA/Sales": "ebitda_ventas"},
    # EV/EBITDA: la segunda aparición de la columna es "solo empresas con EBITDA positivo"
    "vebitda": {"EV/EBITDA #2": "ev_ebitda", "EV/EBIT #2": "ev_ebit"},
    "dbtfund": {"Debt to EBITDA": "deuda_ebitda", "Market D/E (unadjusted)": "deuda_capital_mercado", "Interest Coverage Ratio": "cobertura_intereses"},
    "pbvdata": {"PBV": "precio_valor_contable", "ROE": "roe", "ROIC": "roic"},
    "divfund": {"Dividend Yield": "rentabilidad_dividendo", "Dividend Payout": "payout"},
    "betas": {"Beta": "beta"},
}
EU_NAMES = {"pedata": "pe", "pbvdata": "pbv", "betas": "beta"}   # nombres distintos en la versión Europa
HIST_DATASETS = ["pedata", "margin", "vebitda", "dbtfund", "pbvdata"]
PCT = {"margen_bruto", "margen_operativo", "margen_neto", "ebitda_ventas", "roe", "roic", "rentabilidad_dividendo", "payout", "crecimiento_esperado_5a", "deuda_capital_mercado"}
LABEL = {"per_trailing": "PER trailing", "per_adelantado": "PER adelantado", "crecimiento_esperado_5a": "Crecimiento esperado BPA 5a", "peg": "PEG",
         "margen_bruto": "Margen bruto", "margen_operativo": "Margen operativo", "margen_neto": "Margen neto", "ebitda_ventas": "EBITDA/ventas",
         "ev_ebitda": "EV/EBITDA", "ev_ebit": "EV/EBIT", "deuda_ebitda": "Deuda/EBITDA", "deuda_capital_mercado": "Deuda/capital (mercado)",
         "cobertura_intereses": "Cobertura de intereses", "precio_valor_contable": "Precio/valor contable", "roe": "ROE", "roic": "ROIC",
         "rentabilidad_dividendo": "Rentabilidad por dividendo", "payout": "Payout", "beta": "Beta"}
TABLE_METRICS = ["per_adelantado", "per_trailing", "ev_ebitda", "margen_bruto", "margen_operativo", "margen_neto", "roic", "deuda_ebitda", "rentabilidad_dividendo", "crecimiento_esperado_5a", "beta"]


def _slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def fetch_xls(name, region, year=None):
    nm = EU_NAMES.get(name, name) if region == "EU" else name
    if year is None or year == CURRENT_YEAR:
        url = f"{BASE}datasets/{nm}{REGIONS[region]}.xls"
    else:
        url = f"{BASE}archives/{nm}{REGIONS[region]}{year % 100:02d}.xls"
    r = requests.get(url, headers=H, timeout=90)
    if r.status_code != 200 or len(r.content) < 2000:
        return None
    try:
        x = pd.ExcelFile(io.BytesIO(r.content))
        sheet = "Industry Averages" if "Industry Averages" in x.sheet_names else x.sheet_names[-1]
        df = x.parse(sheet, header=None)
    except Exception as e:  # noqa: BLE001
        print(f"  (no se pudo leer {url}: {e})")
        return None
    hdr = next((i for i in range(15) if any("Industry" in str(v) for v in df.iloc[i].tolist())), None)
    if hdr is None:
        return None
    cols, seen = [], {}
    for c in df.iloc[hdr].tolist():
        c = str(c).strip()
        seen[c] = seen.get(c, 0) + 1
        cols.append(c if seen[c] == 1 else f"{c} #{seen[c]}")   # columnas duplicadas (todas / solo rentables): nos quedamos con la primera
    body = df.iloc[hdr + 1:].copy()
    body.columns = cols
    body = body[body.iloc[:, 0].notna()]
    body = body.rename(columns={cols[0]: "industry"})
    body["industry"] = body["industry"].astype(str).str.strip()
    nf = next((c for c in cols if c.lower().startswith("number of firms")), None)
    body["n"] = pd.to_numeric(body[nf], errors="coerce") if nf else 1
    return body


def extract(body, mapping):
    """De un archivo Damodaran a {industry: {metric: value, n}} usando la primera columna cuyo nombre empieza por el texto buscado."""
    out = {}
    cols = list(body.columns)
    for _, row in body.iterrows():
        rec = {"n": float(row["n"]) if pd.notna(row["n"]) else 1.0}
        for key, metric in mapping.items():
            col = next((c for c in cols if c.lower().startswith(key.lower())), None)
            if col is None:
                continue
            v = pd.to_numeric(row[col], errors="coerce")
            if pd.notna(v):
                rec[metric] = float(v) * (100 if metric in PCT and abs(v) <= 3 else 1)
        out[row["industry"]] = rec
    return out


def aggregate(dam: dict, names: list) -> dict:
    """Media ponderada por número de empresas de las industrias Damodaran de la lista."""
    recs = [dam[n] for n in names if n in dam]
    if not recs:
        return {}
    out = {}
    for metric in set(k for r in recs for k in r if k != "n"):
        pairs = [(r[metric], r["n"]) for r in recs if metric in r and r[metric] == r[metric]]
        pairs = [(v, n) for v, n in pairs if abs(v) < 1e4]   # descarta aberrantes (PER de 5.000 por beneficios ≈ 0)
        if pairs:
            w = sum(n for _, n in pairs) or 1
            out[metric] = sum(v * n for v, n in pairs) / w
    out["n_empresas"] = sum(r["n"] for r in recs)
    out["industrias_damodaran"] = [n for n in names if n in dam]
    return out


def main(with_hist=True):
    corr = yaml.safe_load((HERE / "correspondencia.yaml").read_text(encoding="utf-8"))
    years = ([CURRENT_YEAR] + YEARS_HIST) if with_hist else [CURRENT_YEAR]
    raw = {}   # (region, year) -> {industry: {metric: v}}
    audit = []
    for region in REGIONS:
        for year in years:
            merged = {}
            for ds, mapping in DATASETS.items():
                if year != CURRENT_YEAR and ds not in HIST_DATASETS:
                    continue
                body = fetch_xls(ds, region, year)
                if body is None:
                    print(f"  {region} {year} {ds}: no disponible")
                    continue
                for ind, rec in extract(body, mapping).items():
                    merged.setdefault(ind, {"n": rec["n"]}).update({k: v for k, v in rec.items() if k != "n"})
            raw[(region, year)] = merged
            for ind, rec in merged.items():
                audit.append({"region": region, "year": year, "industry": ind, **{k: v for k, v in rec.items()}})
            print(f"{region} {year}: {len(merged)} industrias")
    pd.DataFrame(audit).to_csv(HERE / "_fuente_damodaran.csv", index=False)

    bench = {"actualizado": dt.date.today().isoformat(), "fuente": "Damodaran (NYU Stern), datos de enero de cada año; actual: enero 2026",
             "anios_historico": [y for y in years if y != CURRENT_YEAR], "regiones": {}}
    for region in REGIONS:
        bench["regiones"][region] = {}
        for sector, inds in corr.items():
            for ind, names in inds.items():
                cur = aggregate(raw.get((region, CURRENT_YEAR), {}), names)
                if not cur:
                    continue
                entry = {"industrias_damodaran": cur.pop("industrias_damodaran"), "n_empresas": round(cur.pop("n_empresas"))}
                for metric, v in cur.items():
                    hist = []
                    for y in years:
                        if y == CURRENT_YEAR:
                            continue
                        a = aggregate(raw.get((region, y), {}), names)
                        if metric in a:
                            hist.append(a[metric])
                    m = {"actual": round(v, 2)}
                    if len(hist) >= 4:
                        s = pd.Series(hist + [v])
                        m.update({"mediana_10a": round(float(s.median()), 2), "p25": round(float(s.quantile(0.25)), 2), "p75": round(float(s.quantile(0.75)), 2),
                                  "min": round(float(s.min()), 2), "max": round(float(s.max()), 2), "n_anios": len(s)})
                    entry[metric] = m
                bench["regiones"][region].setdefault(sector, {})[ind] = entry
    (HERE / "benchmarks.yaml").write_text(yaml.safe_dump(bench, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    write_kb(bench, corr)
    print("benchmarks.yaml y entradas de la base escritos")


# ---------------------------------------------------------------- entradas legibles
COMO_LEERLO = {
    "Energía": "Las integradas y las de exploración cotizan a PER bajo de forma estructural (8-14) porque el mercado no capitaliza beneficios cíclicos; el múltiplo útil es EV/EBITDA (4-7) y el FCF yield. La deuda/EBITDA sube cuando cae el crudo (el denominador se hunde), no porque se endeuden. Los márgenes dependen del precio del barril: compararlos con la mediana solo tiene sentido a precio de crudo similar. Midstream y servicios tienen múltiplos propios (más deuda, más estables).",
    "Materiales": "Químicas y mineras son cíclicas: el PER es bajo en el pico del ciclo (beneficios altos) y alto en el valle; leer EV/EBITDA y precio/valor contable junto al ciclo. Las mineras diversificadas y el acero tienen márgenes operativos muy volátiles; la deuda/EBITDA de 1-2 es normal y de 3 es peligrosa. Los gases industriales (Linde, Air Liquide) son la excepción: calidad estable y múltiplos de consumo básico.",
    "Industriales": "Maquinaria y bienes de equipo: PER 15-25 y margen operativo 10-20 %; la deuda/EBITDA típica es 1-2. Aeroespacial tiene márgenes más bajos y deuda más alta por los programas largos. Aerolíneas y transporte: márgenes de un dígito y PER inútil en años de pérdidas; mirar EV/EBITDA y deuda. Constructoras de viviendas: PER bajo (8-12) y precio/valor contable 1-2; su deuda es inventario. Servicios profesionales: márgenes altos y poca deuda, se comparan con tecnología.",
    "Consumo discrecional": "Mezcla de industrias con economías distintas: lujo (márgenes operativos > 25 %, PER 20-30, poca deuda) frente a automoción (margen 5-10 %, PER 5-8, deuda financiera que distorsiona el ratio). Restauración y hoteles tienen deuda de arrendamientos: usar deuda ajustada. Comercio: margen neto de 2-5 %, el múltiplo útil es EV/EBITDA y la rotación. Comparar siempre contra la industria, nunca contra el sector.",
    "Consumo básico": "El sector de la estabilidad: márgenes operativos 12-20 %, PER 18-25 (prima por previsibilidad), deuda/EBITDA 2-3 aceptada por la estabilidad de flujos. Tabaco y bebidas alcohólicas: márgenes muy altos y PER bajo (riesgo regulatorio). Distribución de alimentación: margen neto 1-3 %, PER 12-18, mucha deuda de arrendamientos. Un PER por encima del p75 de su industria con crecimiento del 3 % es la señal de sobrevaloración más clara del sector.",
    "Salud": "Farmacia: margen bruto 65-80 %, margen operativo 25-35 %, PER 12-18 (riesgo de patentes), poca deuda; mirar el crecimiento esperado y la fecha de vencimiento de patentes. Biotecnología: PER inútil en la mayoría (pérdidas); EV/ventas y caja. Equipos médicos: márgenes altos y PER 25-35 (crecimiento estable). Servicios y aseguradoras: margen neto 3-6 %, PER 12-18. Distribución: margen neto < 1 %, se valora por FCF.",
    "Financiero": "Los múltiplos de beneficio funcionan distinto: el precio/valor contable y el ROE son la pareja clave (PBV ≈ ROE / coste del capital). Bancos: PER 8-12, PBV 0,8-1,5 en Europa y 1-2 en EE.UU.; la deuda/EBITDA no aplica. Aseguradoras: PBV 1-2 y ROE 10-15 %; las de vida son sensibles a tipos. Bolsas, gestoras y pagos: economías de tecnología (márgenes 30-50 %, PER 20-30). Comparar bancos europeos y americanos entre sí es un error: regulación, tipos y rentabilidad distintos.",
    "Tecnología de la información": "Software: márgenes brutos 70-85 %, operativos 20-35 %, PER 25-40 y caja neta; el múltiplo relevante es EV/ventas más crecimiento. Semiconductores: cíclicos, márgenes operativos 20-40 % en el pico y 10 % en el valle, PER engañoso en ambos extremos. Hardware: márgenes más bajos (Apple es la excepción). Servicios de TI: márgenes 10-15 % y PER 15-25. El sector entero cotiza con prima sobre el mercado; la cuestión es si su industria la justifica con crecimiento.",
    "Servicios de comunicación": "Dos mundos: telecomunicaciones (deuda/EBITDA 2-3, márgenes EBITDA 35-40 %, PER 10-15, dividendo alto, crecimiento cero) y medios interactivos (márgenes y múltiplos de software). Publicidad: márgenes 12-15 % y PER 10-15, cíclica. Entretenimiento y videojuegos: beneficios irregulares, EV/ventas. Las torres son REITs con otro nombre: deuda alta y múltiplo de flujo.",
    "Utilities": "Reguladas: ROE fijado por el regulador (8-10 %), deuda/EBITDA 4-6 aceptada por la regulación, PER 14-20, dividendo 3-5 %. El múltiplo útil es precio/valor contable (1,2-2) y el crecimiento de la base de activos regulada. Renovables puras: deuda muy alta y beneficios bajos; valorar por EV/EBITDA y capacidad. Generación independiente (Vistra, Constellation): beneficios volátiles ligados a precios de la electricidad; desde 2024 cotizan con prima por centros de datos.",
    "Inmobiliario": "Los REITs se valoran por flujos (FFO, AFFO), no por beneficio contable (la depreciación lo hunde): el PER no sirve. Usar precio/FFO (12-20), rentabilidad por dividendo (3-6 %), deuda/EBITDA (5-7 aceptable, > 8 peligroso) y descuento sobre valor neto de activos. Logística e infraestructura digital con prima; oficinas con descuento estructural desde 2020. Son el sector más sensible al tipo real a 10 años.",
}
TRAMPAS = {
    "Energía": "PER bajo no es barato si el crudo está en máximos (beneficios de pico). Deuda/EBITDA aparentemente alta tras una caída del crudo.",
    "Materiales": "El PER más bajo coincide con el pico de ciclo. Las mineras de oro cotizan con prima por el metal, no por calidad.",
    "Industriales": "La deuda de los constructores de viviendas es inventario, no apalancamiento. Las aerolíneas con PER de 5 suelen estar a punto de perder dinero.",
    "Consumo discrecional": "Automoción con PER 6 no es barata: es cíclica con deuda de financiación. Arrendamientos de hoteles y restauración inflan la deuda ajustada.",
    "Consumo básico": "La prima por estabilidad desaparece cuando el crecimiento baja del 3 %; un PER de 25 con ventas planas es la trampa típica.",
    "Salud": "Farmacia con PER 10 puede tener un vencimiento de patente a dos años. Biotech: el PER negativo no es señal de nada.",
    "Financiero": "La deuda/EBITDA y los márgenes no aplican a bancos y aseguradoras. PBV < 1 puede ser oportunidad o aviso de pérdidas latentes (SVB).",
    "Tecnología de la información": "Semiconductores con PER 12 en el pico del ciclo; software con PER 60 puede ser más barato que uno con PER 30 si crece el triple.",
    "Servicios de comunicación": "Telecos con dividendo del 7 % suelen recortarlo; medios con PER bajo pueden estar en declive estructural.",
    "Utilities": "Deuda/EBITDA de 5 es normal, no alarma; pero el tipo real alto la encarece al refinanciar.",
    "Inmobiliario": "El PER contable no sirve. Rentabilidad por dividendo > 8 % suele anticipar un recorte.",
}


def write_kb(bench: dict, corr: dict):
    def fmt(m, metric):
        if not m:
            return "—"
        a = m["actual"]
        s = f"{a:.1f}" + (" %" if metric in PCT else "")
        if "p25" in m:
            s += f" <span style='color:#888'>({m['p25']:.1f}-{m['p75']:.1f})</span>"
        return s

    index_lines = []
    for sector in corr:
        slug = _slug(sector)
        lines = [f"---\ntipo: benchmark\nid: benchmark-{slug}\nnombre: Valoración y calidad por industria · {sector}\nsector: {sector}\nfuente: Damodaran (NYU Stern), enero de cada año; actual {bench['actualizado']}\nactualizado: {bench['actualizado']}\n---\n",
                 f"# Valoración y calidad por industria · {sector}\n",
                 "Medianas de la industria (media ponderada por número de empresas de las industrias de Damodaran que la componen), con el rango de 10 años entre paréntesis (percentiles 25 y 75 de las medianas anuales 2016-2026). Sirve para leer el PER, el margen o la deuda de una empresa **contra su industria y su década**, no contra la watchlist.\n",
                 "## Cómo leerlo\n", COMO_LEERLO.get(sector, ""), "", "## Trampas de lectura\n", TRAMPAS.get(sector, ""), ""]
        for region, label in (("US", "Estados Unidos"), ("EU", "Europa")):
            data = bench["regiones"].get(region, {}).get(sector, {})
            if not data:
                continue
            lines.append(f"## {label}\n")
            lines.append("| Industria | n | " + " | ".join(LABEL[m] for m in TABLE_METRICS) + " |")
            lines.append("| --- | ---: | " + " | ".join("---:" for _ in TABLE_METRICS) + " |")
            for ind, e in data.items():
                lines.append(f"| {ind} | {e['n_empresas']} | " + " | ".join(fmt(e.get(m), m) for m in TABLE_METRICS) + " |")
            lines.append("")
        lines.append("## Industrias de Damodaran que alimentan cada una\n")
        for ind, names in corr[sector].items():
            lines.append(f"- **{ind}**: {', '.join(names)}")
        lines.append("\n## Para profundizar\n- Damodaran, datos actuales por industria: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html\n- Archivo histórico: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/dataarchived.html\n- Definiciones de variables: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/databreakdown.html")
        (HERE / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")
        index_lines.append(f"- [{sector}]({slug}.md)")
    (HERE / "README.md").write_text("# Benchmarks de valoración por industria\n\nFuente: Damodaran (NYU Stern). Actualización anual (workflow \"Benchmarks de industria\", cada 15 de enero) o manual con `python kb/benchmarks/actualizar.py`.\n\n"
                                   "`benchmarks.yaml` es el archivo que lee el motor (score predictivo y ficha de calidad); las entradas por sector son la versión legible.\n\n" + "\n".join(index_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(with_hist="--sin-historico" not in sys.argv)
