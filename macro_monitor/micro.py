"""Capa micro: revisiones de analistas, hechos relevantes (8-K), insiders (Form 4) y comunicación de bancos centrales.

Fuentes: yfinance (revisiones y estimaciones), SEC EDGAR (8-K y Form 4, sin clave), RSS Fed/BCE.
Produce: dict con pulso por empresa y por sector, eventos de la semana, discursos clasificados.
"""
import os
import re
import json
import time
import html as _html
import datetime as dt
import pathlib
import xml.etree.ElementTree as ET

import requests

from . import empresas

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
# La SEC exige User-Agent con nombre y email de contacto; configurable con EDGAR_USER_AGENT
H = {"User-Agent": os.environ.get("EDGAR_USER_AGENT", "macro-monitor personal research macro-monitor@example.com")}

ITEMS_8K = {
    "1.01": ("Acuerdo material", 2), "1.02": ("Terminación de acuerdo", 2), "1.03": ("Quiebra", 3),
    "2.01": ("Adquisición o venta de activos", 2), "2.02": ("Resultados", 3), "2.03": ("Nueva deuda", 1),
    "2.04": ("Aceleración de deuda", 3), "2.05": ("Costes de reestructuración", 2), "2.06": ("Deterioros de activos", 3),
    "3.01": ("Aviso de exclusión de cotización", 3), "3.02": ("Emisión de acciones", 1), "3.03": ("Cambio en derechos de accionistas", 1),
    "4.01": ("Cambio de auditor", 2), "4.02": ("Reexpresión de cuentas", 3),
    "5.01": ("Cambio de control", 3), "5.02": ("Salida o nombramiento de directivos/consejeros", 3), "5.03": ("Estatutos", 0),
    "5.07": ("Votaciones de la junta", 1), "5.08": ("Nominaciones", 0),
    "7.01": ("Reg FD: presentación, guía o comunicado", 2), "8.01": ("Otros hechos", 1), "9.01": ("Anexos", 0),
}
EU_SUFFIXES = empresas.EU_SUFFIXES


# ---------------------------------------------------------------- utilidades
def _get(url, **kw):
    r = requests.get(url, headers=H, timeout=30, **kw)
    r.raise_for_status()
    return r


_cik_cache = None


def cik_map() -> dict:
    global _cik_cache
    if _cik_cache is None:
        try:
            m = _get("https://www.sec.gov/files/company_tickers.json").json()
            _cik_cache = {v["ticker"].upper(): int(v["cik_str"]) for v in m.values()}
        except Exception as e:  # noqa: BLE001
            print(f"(edgar cik map: {e})")
            _cik_cache = {}
    return _cik_cache


# ---------------------------------------------------------------- 1. revisiones de analistas
def _int(v) -> int:
    """Entero tolerante a NaN/None/strings."""
    try:
        f = float(v)
        return 0 if f != f else int(f)  # NaN != NaN
    except (TypeError, ValueError):
        return 0


def revisions(ticker: str) -> dict | None:
    import yfinance as yf
    try:
        t = yf.Ticker(ticker)
        rev = t.eps_revisions
        trend = t.eps_trend
        rec = t.recommendations_summary
    except Exception as e:  # noqa: BLE001
        print(f"(revisiones {ticker}: {e})")
        return None
    if rev is None or rev.empty:
        return None
    out = {}
    for period, key in (("0q", "trim"), ("0y", "anual")):
        if period in rev.index:
            r = rev.loc[period]
            up30, dn30 = _int(r.get("upLast30days")), _int(r.get("downLast30days"))
            up7, dn7 = _int(r.get("upLast7days")), _int(r.get("downLast7Days", r.get("downLast7days")))
            net = (up30 - dn30) / (up30 + dn30) if (up30 + dn30) else 0.0
            out[key] = {"up30": up30, "down30": dn30, "up7": up7, "down7": dn7, "net30": round(net, 2)}
    if trend is not None and not trend.empty and "0y" in trend.index:
        tr = trend.loc["0y"]
        cur, ago = tr.get("current"), tr.get("30daysAgo")
        try:
            if cur == cur and ago == ago and cur and ago:
                out["est_anual_chg30_pct"] = round((float(cur) - float(ago)) / abs(float(ago)) * 100, 2)
        except (TypeError, ValueError):
            pass
    if rec is not None and not rec.empty:
        now, prev = rec.iloc[0], rec.iloc[min(1, len(rec) - 1)]
        pos = lambda r: _int(r.get("strongBuy")) + _int(r.get("buy"))  # noqa: E731
        neg = lambda r: _int(r.get("sell")) + _int(r.get("strongSell"))  # noqa: E731
        out["recomendaciones"] = {"compra": pos(now), "venta": neg(now), "cambio_compra_1m": pos(now) - pos(prev)}
    return out


# ---------------------------------------------------------------- 2. hechos relevantes 8-K  y 3. insiders Form 4
def edgar(ticker: str, days: int = 7, insider_days: int = 30) -> dict:
    cik = cik_map().get(ticker.upper())
    if not cik:
        return {"eventos": [], "insiders": [], "cobertura": False}
    try:
        sub = _get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json").json()
    except Exception as e:  # noqa: BLE001
        print(f"(edgar {ticker}: {e})")
        return {"eventos": [], "insiders": [], "cobertura": False}
    f = sub["filings"]["recent"]
    since_ev = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    since_in = (dt.date.today() - dt.timedelta(days=insider_days)).isoformat()
    eventos, insiders = [], []
    for form, date, items, acc, doc in zip(f["form"], f["filingDate"], f.get("items", [""] * len(f["form"])),
                                           f["accessionNumber"], f["primaryDocument"]):
        base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}"
        if form == "8-K" and date >= since_ev:
            codes = [c.strip() for c in (items or "").split(",") if c.strip()]
            desc = [ITEMS_8K.get(c, (c, 1))[0] for c in codes if ITEMS_8K.get(c, (c, 1))[1] > 0]
            imp = max([ITEMS_8K.get(c, (c, 1))[1] for c in codes] or [1])
            eventos.append({"fecha": date, "codigos": codes, "descripcion": " · ".join(desc) or "8-K", "importancia": imp,
                            "url": f"{base}/{doc}"})
        elif form == "4" and date >= since_in and len(insiders) < 25:
            try:
                raw = doc.split("/")[-1]
                root = ET.fromstring(_get(f"{base}/{raw}").text)
                owner = root.findtext(".//reportingOwner/reportingOwnerId/rptOwnerName") or "?"
                rel = root.find(".//reportingOwnerRelationship")
                title = (rel.findtext("officerTitle") if rel is not None else "") or \
                        ("consejero" if rel is not None and rel.findtext("isDirector") == "1" else "")
                for tr in root.findall(".//nonDerivativeTransaction"):
                    code = tr.findtext(".//transactionCoding/transactionCode")
                    if code not in ("P", "S"):
                        continue
                    sh = float(tr.findtext(".//transactionShares/value") or 0)
                    pr = float(tr.findtext(".//transactionPricePerShare/value") or 0)
                    insiders.append({"fecha": tr.findtext(".//transactionDate/value") or date, "quien": owner.title(),
                                     "cargo": title, "tipo": "compra" if code == "P" else "venta",
                                     "importe_usd": round(sh * pr), "acciones": round(sh), "url": f"{base}/{raw}"})
                time.sleep(0.15)  # EDGAR: máx 10 req/s
            except Exception as e:  # noqa: BLE001
                print(f"(form4 {ticker} {date}: {e})")
    compras = [i for i in insiders if i["tipo"] == "compra" and i["importe_usd"] >= 10_000]  # compras simbólicas no cuentan
    compradores = {i["quien"] for i in compras}
    importe_compras = sum(i["importe_usd"] for i in compras)
    return {"eventos": eventos, "insiders": insiders, "cobertura": True,
            "compra_cluster": len(compradores) >= 3 and importe_compras >= 250_000, "n_compradores": len(compradores),
            "importe_compras": importe_compras,
            "importe_ventas": sum(i["importe_usd"] for i in insiders if i["tipo"] == "venta")}


# ---------------------------------------------------------------- 4. bancos centrales
FEEDS = [
    ("Fed", "discurso", "https://www.federalreserve.gov/feeds/speeches.xml"),
    ("Fed", "comunicado", "https://www.federalreserve.gov/feeds/press_monetary.xml"),
    ("BCE", "comunicado", "https://www.ecb.europa.eu/rss/press.html"),
]


def _rss_items(url):
    txt = _get(url).text
    out = []
    for it in re.findall(r"<item>(.*?)</item>", txt, re.S):
        g = lambda tag: re.search(rf"<{tag}>(.*?)</{tag}>", it, re.S)  # noqa: E731
        t, l, d = g("title"), g("link"), (g("pubDate") or g("dc:date"))
        clean = lambda m: _html.unescape(re.sub(r"<!\[CDATA\[|\]\]>", "", m.group(1))).strip() if m else ""  # noqa: E731
        out.append({"titulo": clean(t), "url": clean(l), "fecha_raw": clean(d)})
    return out


def _parse_date(s):
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return dt.date(int(m[1]), int(m[2]), int(m[3])) if m else None


def _page_text(url, limit=7000):
    try:
        t = _get(url).text
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
        t = _html.unescape(re.sub(r"\s+", " ", t))
        return t[:limit]
    except Exception:  # noqa: BLE001
        return ""


def _classify_speech(title, text) -> dict | None:
    key = os.environ.get("GROQ_API_KEY")
    if not key or not text:
        return None
    prompt = ("Clasifica este discurso o comunicado de un banco central para un inversor. Responde SOLO con JSON: "
              '{"postura": entero de -2 (muy paloma: recortes, preocupación por crecimiento) a +2 (muy halcón: subidas, '
              'inflación persistente), 0 si no trata de política monetaria; "tema": 3-6 palabras; '
              '"resumen": una frase de máximo 30 palabras con lo relevante para tipos o mercados; '
              '"relevante": true/false (false si es regulación bancaria, pagos u otro tema sin impacto en tipos)}'
              f"\n\nTÍTULO: {title}\n\nTEXTO:\n{text}")
    for model in ("openai/gpt-oss-20b", "openai/gpt-oss-120b"):
        for intento in (1, 2):
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                  headers={"Authorization": f"Bearer {key}"}, timeout=60,
                                  json={"model": model, "temperature": 0, "max_tokens": 600, "reasoning_effort": "low",
                                        "messages": [{"role": "user", "content": prompt}]})
                if r.status_code in (413, 429) and intento == 1:
                    time.sleep(25)
                    continue
                r.raise_for_status()
                txt = r.json()["choices"][0]["message"]["content"]
                m = re.search(r"\{.*\}", txt, re.S)
                return json.loads(m.group(0)) if m else None
            except Exception as e:  # noqa: BLE001
                print(f"(clasificación discurso {model}: {e})")
                break
    return None


MAX_DISCURSOS_CLASIFICADOS = 6


def central_banks(days: int = 7) -> list:
    since = dt.date.today() - dt.timedelta(days=days)
    out = []
    clasificados = 0
    for banco, tipo, url in FEEDS:
        try:
            items = _rss_items(url)
        except Exception as e:  # noqa: BLE001
            print(f"(rss {banco}: {e})")
            continue
        for it in items:
            d = _parse_date(it["fecha_raw"])
            if not d or d < since:
                continue
            if banco == "BCE" and "/press/key/" not in it["url"] and "monetary" not in it["url"].lower() \
                    and "/press/pr/" in it["url"] and not re.search(r"monetary policy|interest rate", it["titulo"], re.I):
                continue  # BCE: solo discursos y decisiones de política monetaria
            kind = "discurso" if "/press/key/" in it["url"] or tipo == "discurso" else "comunicado"
            cls = None
            if clasificados < MAX_DISCURSOS_CLASIFICADOS:
                cls = _classify_speech(it["titulo"], _page_text(it["url"]))
                clasificados += 1
                time.sleep(3)  # Groq gratuito: espaciar llamadas
            if cls and cls.get("relevante") is False:
                continue
            out.append({"banco": banco, "tipo": kind, "fecha": d.isoformat(), "titulo": it["titulo"], "url": it["url"],
                        **({"postura": cls.get("postura"), "tema": cls.get("tema"), "resumen": cls.get("resumen")} if cls else {})})
    out.sort(key=lambda x: x["fecha"], reverse=True)
    return out


# ---------------------------------------------------------------- orquestación
def run(scope: str = "bellwethers", days: int = 7) -> dict:
    wl = empresas.load_watchlist()
    if scope == "bellwethers":
        wl = [c for c in wl if c["role"] == "bellwether" or c["sector"] == "Extra"]
    companies = []
    for c in wl:
        t = c["t"]
        try:
            rev = revisions(t)
        except Exception as e:  # noqa: BLE001
            print(f"(revisiones {t}: {e})"); rev = None
        try:
            ed = edgar(t, days) if not t.endswith(EU_SUFFIXES) else {"eventos": [], "insiders": [], "cobertura": False}
        except Exception as e:  # noqa: BLE001
            print(f"(edgar {t}: {e})"); ed = {"eventos": [], "insiders": [], "cobertura": False}
        companies.append({"t": t, "name": c["name"], "sector": c["sector"], "region": c["region"], "role": c["role"],
                          "revisiones": rev, **ed})
    # Pulso por sector: amplitud de revisiones (media de net30 anual) + eventos
    sectors = {}
    for co in companies:
        s = sectors.setdefault(co["sector"], {"n": 0, "net": [], "up": 0, "down": 0, "eventos": 0, "cluster": 0})
        r = (co.get("revisiones") or {}).get("anual")
        if r:
            s["n"] += 1
            s["net"].append(r["net30"])
            s["up"] += r["net30"] > 0.2
            s["down"] += r["net30"] < -0.2
        s["eventos"] += len([e for e in co["eventos"] if e["importancia"] >= 2])
        s["cluster"] += bool(co.get("compra_cluster"))
    pulse = {}
    for sec, s in sectors.items():
        breadth = sum(s["net"]) / len(s["net"]) if s["net"] else None
        sig = 0 if breadth is None else 1 if breadth > 0.2 else -1 if breadth < -0.2 else 0
        pulse[sec] = {"amplitud_revisiones": None if breadth is None else round(breadth, 2), "senal": sig,
                      "empresas_cubiertas": s["n"], "mejorando": s["up"], "empeorando": s["down"],
                      "hechos_relevantes": s["eventos"], "clusters_insiders": s["cluster"]}
    return {"date": dt.date.today().isoformat(), "scope": scope, "companies": companies, "sector_pulse": pulse,
            "central_banks": central_banks(days)}


def conflicts(micro: dict, sectors_macro: list) -> list:
    """Sectores donde el sesgo macro y el pulso micro discrepan de signo."""
    out = []
    for s in sectors_macro:
        p = micro["sector_pulse"].get(s["label"])
        if not p or p["senal"] == 0 or s["bias"] == 0 or p["empresas_cubiertas"] < 3:
            continue
        if abs(p["amplitud_revisiones"] or 0) < 0.33:
            continue
        if (p["senal"] > 0) != (s["bias"] > 0):
            out.append({"sector": s["label"], "macro": s["bias"], "micro": p["senal"], "amplitud": p["amplitud_revisiones"],
                        "texto": f"Macro {s['bias']:+d} pero los analistas {'suben' if p['senal'] > 0 else 'recortan'} estimaciones "
                                 f"({p['mejorando']} mejorando / {p['empeorando']} empeorando de {p['empresas_cubiertas']})."})
    return out


def save(micro: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "micro.json").write_text(json.dumps(micro, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


# ---------------------------------------------------------------- email
def _money(v):
    return f"{v/1e6:.1f} M$" if v >= 1e6 else f"{v/1e3:.0f} k$"


def to_html(micro: dict, confl: list) -> str:
    h = ["<h3>Pulso micro · revisiones, hechos relevantes, insiders</h3>"]
    if confl:
        h.append("<div style='background:#fff3e0;border:1px solid #e0b060;border-radius:6px;padding:8px 12px;margin-bottom:8px'>"
                 "<b>Conflictos macro / micro</b><ul style='margin:4px 0'>")
        for c in confl:
            h.append(f"<li><b>{c['sector']}</b>: {c['texto']}</li>")
        h.append("</ul></div>")
    # sectores
    h.append("<table cellpadding='5' style='border-collapse:collapse;width:100%'><tr style='background:#f0f0f0'>"
             "<th align='left'>Sector</th><th align='right'>Amplitud rev. 30d</th><th align='right'>Mejoran / empeoran</th>"
             "<th align='right'>Hechos</th><th align='right'>Clusters compra</th></tr>")
    for sec, p in sorted(micro["sector_pulse"].items(), key=lambda x: -(x[1]["amplitud_revisiones"] or -9)):
        amp = "—" if p["amplitud_revisiones"] is None else f"{p['amplitud_revisiones']:+.2f}"
        col = "#07a" if p["senal"] > 0 else "#b00" if p["senal"] < 0 else "#222"
        h.append(f"<tr><td>{sec}</td><td align='right' style='color:{col};font-weight:bold'>{amp}</td>"
                 f"<td align='right'>{p['mejorando']} / {p['empeorando']} <span style='color:#999'>de {p['empresas_cubiertas']}</span></td>"
                 f"<td align='right'>{p['hechos_relevantes']}</td><td align='right'>{p['clusters_insiders']}</td></tr>")
    h.append("</table>")
    # hechos relevantes e insiders por empresa
    rows = []
    for co in micro["companies"]:
        for e in co["eventos"]:
            if e["importancia"] >= 2:
                rows.append((e["fecha"], f"<b>{co['name']}</b> <span style='color:#999'>{co['t']}</span>", "8-K",
                             f"<a href='{e['url']}'>{e['descripcion']}</a>", e["importancia"]))
        if co.get("compra_cluster"):
            rows.append((co["insiders"][0]["fecha"], f"<b>{co['name']}</b> <span style='color:#999'>{co['t']}</span>", "Insiders",
                         f"Compras de {co['n_compradores']} directivos/consejeros en 30 días, {_money(co['importe_compras'])}", 3))
        else:
            for i in co["insiders"]:
                if i["tipo"] == "compra" and i["importe_usd"] >= 100_000:
                    rows.append((i["fecha"], f"<b>{co['name']}</b> <span style='color:#999'>{co['t']}</span>", "Insider",
                                 f"<a href='{i['url']}'>Compra</a> de {i['quien']} ({i['cargo'] or 'consejero'}): {_money(i['importe_usd'])}", 2))
        r = co.get("revisiones") or {}
        a = r.get("anual")
        if a and abs(a["net30"]) >= 0.6 and (a["up30"] + a["down30"]) >= 3:
            rows.append((micro["date"], f"<b>{co['name']}</b> <span style='color:#999'>{co['t']}</span>", "Revisiones",
                         f"{'Suben' if a['net30'] > 0 else 'Recortan'} estimaciones anuales: {a['up30']} al alza / {a['down30']} a la baja en 30 días"
                         + (f"; estimación {r['est_anual_chg30_pct']:+.1f}%" if r.get("est_anual_chg30_pct") is not None else ""), 2))
    if rows:
        rows.sort(key=lambda x: (-x[4], x[0]), reverse=False)
        rows.sort(key=lambda x: x[0], reverse=True)
        h.append("<h4 style='margin:12px 0 4px'>Empresas: qué ha cambiado</h4><table cellpadding='5' style='border-collapse:collapse;width:100%'>")
        for d, who, kind, what, imp in rows[:25]:
            style = " style='background:#fff3f3'" if imp >= 3 else ""
            h.append(f"<tr{style}><td style='white-space:nowrap;color:#666'>{d}</td><td>{who}</td><td style='white-space:nowrap'>{kind}</td><td>{what}</td></tr>")
        h.append("</table>")
    else:
        h.append("<p style='color:#666'>Sin hechos relevantes ni compras de insiders significativas esta semana.</p>")
    # bancos centrales
    cb = micro.get("central_banks") or []
    if cb:
        h.append("<h4 style='margin:12px 0 4px'>Bancos centrales · últimos 7 días</h4><table cellpadding='5' style='border-collapse:collapse;width:100%'>")
        for s in cb[:12]:
            post = s.get("postura")
            tag = "" if post is None else ("<span style='color:#b00'>halcón</span>" if post > 0 else "<span style='color:#07a'>paloma</span>" if post < 0 else "neutral")
            h.append(f"<tr><td style='white-space:nowrap;color:#666'>{s['fecha']}</td><td style='white-space:nowrap'><b>{s['banco']}</b></td>"
                     f"<td><a href='{s['url']}'>{_html.escape(s['titulo'])}</a>" + (f"<br><span style='font-size:12px;color:#555'>{_html.escape(s.get('resumen') or '')}</span>" if s.get("resumen") else "")
                     + f"</td><td style='white-space:nowrap'>{tag} {'' if post is None else f'({post:+d})'}</td></tr>")
        h.append("</table>")
    return "\n".join(h)
