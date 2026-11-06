"""Ledger externo (Google Sheets publicado como CSV): registro único de operaciones.

Cuatro pestañas publicadas como CSV, una URL cada una en variables de entorno:
  LEDGER_OPERACIONES  una fila por tramo (id, posicion_id, tramo, fecha_entrada, ticker, lado, origen, regimen,
                      entrada, stop, objetivo, acciones, riesgo_usd, riesgo_pct, importe, manda, estado,
                      fecha_salida, salida, motivo_salida, r_obtenido, plan_cumplido, nota, pnl_usd)
  LEDGER_PARAMETROS   capital, tope_posicion, max_posiciones, perdida_semanal_max, comision_orden, tramos_pesos
                      y, más abajo, la tabla de orígenes (codigo, riesgo, activo, descripcion)
  LEDGER_VETO         ticker, apta (SI/NO/DUDA), fecha_revision, motivo
  LEDGER_TEMAS        tema, ticker, rol_en_cadena, lider, fecha_alta, nota

Si LEDGER_OPERACIONES no está definida, nada cambia: el motor sigue leyendo cartera/operaciones.csv.

Qué hace cuando está configurado:
  - apply(cfg): capital y tope por posición pasan a ser los del Ledger (config.yaml queda como respaldo).
  - cartera.load() reconstruye la cartera desde las filas con estado ABIERTA (cerradas desde CERRADA).
  - propuestas(): tres bloques para el email, cada fila en el orden de columnas del Ledger:
      · Órdenes propuestas  (origen MACRO_TEC): candidatas de la Decisión del día con orden_posible.
      · Candidatas técnicas (origen TEC): retroceso a MA50 o ruptura de 52 semanas en cualquier empresa de la
        watchlist cuyo sector no esté vetado por el régimen, sin apoyo macro.
      · Añadidos propuestos: tramos 2 y 3 (reparto 50/30/20 del riesgo) sobre posiciones ABIERTAS en MACRO_TEC.
    Bloqueos: max_posiciones alcanzado, ticker ya abierto, pérdida realizada de 7 días por encima del límite,
    veto NO (DUDA se marca). Tamaño = min(riesgo_origen × capital ÷ distancia, tope × capital ÷ precio).
"""
import os
import json
import math
import datetime as dt
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

COLS = ["id", "posicion_id", "tramo", "fecha_entrada", "ticker", "lado", "origen", "regimen", "entrada", "stop", "objetivo",
        "acciones", "riesgo_usd", "riesgo_pct", "importe", "manda", "estado", "fecha_salida", "salida", "motivo_salida",
        "r_obtenido", "plan_cumplido", "nota"]
ENV = {"operaciones": "LEDGER_OPERACIONES", "parametros": "LEDGER_PARAMETROS", "veto": "LEDGER_VETO", "temas": "LEDGER_TEMAS"}
PESOS_TRAMOS = (0.5, 0.3, 0.2)
_cache: dict = {}


def configured() -> bool:
    return bool(os.environ.get(ENV["operaciones"]))


def _read(key: str) -> pd.DataFrame:
    """Lee una pestaña (URL o ruta local). Cachea por ejecución. Devuelve DataFrame vacío si no está configurada."""
    if key in _cache:
        return _cache[key]
    src = os.environ.get(ENV[key], "")
    if not src:
        _cache[key] = pd.DataFrame()
        return _cache[key]
    df = pd.read_csv(src, dtype=str, keep_default_na=False)
    df.columns = [c.strip() for c in df.columns]
    _cache[key] = df
    return df


def _num(v, default=None):
    if v is None:
        return default
    s = str(v).strip().replace("%", "")
    if s == "":
        return default
    # formato español: 1.234,5 -> 1234.5 ; 0,2 -> 0.2 ; también acepta 1234.5 y 0.2
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return default


# ---------------------------------------------------------------- lectura
def parametros() -> dict:
    """Parámetros y tabla de orígenes. Valores por defecto si falta alguno."""
    df = _read("parametros")
    out = {"capital": 100_000.0, "tope_posicion": 0.20, "max_posiciones": 5, "perdida_semanal_max": 0.03, "comision_orden": 1.0,
           "origenes": {}}
    if df.empty:
        return out
    cols = list(df.columns)
    # bloque 1: Parámetro | Valor | Nota
    for _, r in df.iterrows():
        k = str(r.get(cols[0], "")).strip()
        v = str(r.get(cols[1], "")).strip() if len(cols) > 1 else ""
        if k in ("capital", "max_posiciones", "comision_orden"):
            out[k] = _num(v, out[k])
        elif k in ("tope_posicion", "perdida_semanal_max"):
            x = _num(v, out[k])
            out[k] = x / 100 if x is not None and x > 1 else x   # admite 20 o 0,2 o 20 %
        elif k == "tramos_pesos":
            out["tramos_pesos"] = v
        # bloque 2: filas de la tabla de orígenes (codigo | riesgo | activo | descripcion) debajo de la cabecera "codigo"
        elif k and k.isupper() and len(cols) >= 3:
            riesgo = _num(v)
            if riesgo is not None:
                if riesgo > 1:                 # 1 o 0,5 escritos como porcentaje
                    riesgo = riesgo / 100
                activo = str(r.get(cols[2], "")).strip().upper() == "SI"
                out["origenes"][k] = {"riesgo": riesgo, "activo": activo,
                                      "descripcion": str(r.get(cols[3], "")).strip() if len(cols) > 3 else ""}
    out["max_posiciones"] = int(out["max_posiciones"] or 5)
    if not out["origenes"]:
        out["origenes"] = {"MACRO_TEC": {"riesgo": 0.01, "activo": True, "descripcion": ""},
                           "TEC": {"riesgo": 0.005, "activo": True, "descripcion": ""}}
    return out


def operaciones() -> pd.DataFrame:
    df = _read("operaciones")
    if df.empty:
        return df
    df = df[df["ticker"].str.strip() != ""].copy()
    df["estado"] = df["estado"].str.strip().str.upper()
    df["origen"] = df["origen"].str.strip().str.upper()
    df["ticker"] = df["ticker"].str.strip().str.upper()
    for c in ("entrada", "stop", "objetivo", "acciones", "salida", "r_obtenido", "pnl_usd", "riesgo_usd", "tramo"):
        if c in df:
            df[c] = df[c].map(_num)
    return df


def operaciones_as_cartera() -> pd.DataFrame:
    """Traduce el Ledger al esquema que valora cartera.build (una fila por tramo)."""
    df = operaciones()
    if df.empty:
        return pd.DataFrame()
    rows = []
    for _, r in df.iterrows():
        est = {"ABIERTA": "abierta", "CERRADA": "cerrada"}.get(r["estado"])
        if not est:
            continue
        rows.append({"id": r.get("id", ""), "fecha_apertura": r.get("fecha_entrada", ""), "ticker": r["ticker"],
                     "lado": "corto" if str(r.get("lado", "")).strip().upper() == "SHORT" else "largo",
                     "acciones": r.get("acciones"), "precio_entrada": r.get("entrada"), "stop": r.get("stop"), "fx_entrada": 1.0,
                     "regimen": r.get("regimen", ""), "tension": "", "sesgo_sector": None, "amplitud_revisiones": None,
                     "disparador": r.get("origen", ""), "cierro_si": "", "fecha_cierre": r.get("fecha_salida", ""),
                     "precio_cierre": r.get("salida"), "motivo_cierre": r.get("motivo_salida", ""), "leccion": r.get("nota", ""),
                     "estado": est, "posicion_id": r.get("posicion_id", ""), "tramo": r.get("tramo"), "origen": r.get("origen", "")})
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    for c in ("acciones", "precio_entrada", "stop", "fx_entrada", "precio_cierre"):
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def veto() -> dict:
    df = _read("veto")
    if df.empty or "ticker" not in df or "apta" not in df:
        return {}
    return {str(r["ticker"]).strip().upper(): str(r["apta"]).strip().upper() for _, r in df.iterrows() if str(r["ticker"]).strip()}


def temas() -> pd.DataFrame:
    df = _read("temas")
    if df.empty or "ticker" not in df:
        return df
    return df[df["ticker"].str.strip() != ""].copy()


def perdida_7d() -> float:
    """Pérdida realizada (USD, positiva) de las operaciones CERRADAS con fecha_salida en los últimos 7 días."""
    df = operaciones()
    if df.empty or "fecha_salida" not in df:
        return 0.0
    lim = (dt.date.today() - dt.timedelta(days=7)).isoformat()
    tot = 0.0
    for _, r in df[df["estado"] == "CERRADA"].iterrows():
        f = str(r.get("fecha_salida", "")).strip()[:10]
        if f >= lim:
            pnl = r.get("pnl_usd")
            if pnl is None and r.get("r_obtenido") is not None and r.get("riesgo_usd") is not None:
                pnl = r["r_obtenido"] * r["riesgo_usd"]
            if pnl is not None and pnl < 0:
                tot += -pnl
    return tot


def apply(cfg: dict) -> dict:
    """Capital y tope por posición desde el Ledger (sustituyen a config.yaml mientras el Ledger esté configurado)."""
    if not configured():
        return cfg
    p = parametros()
    f = cfg.setdefault("ficha", {})
    f["capital"] = p["capital"]
    f["moneda"] = "USD"
    f["posicion_max_pct"] = p["tope_posicion"] * 100
    f["posicion_max_pct_cautela"] = p["tope_posicion"] * 100
    cfg["_ledger"] = p
    return cfg


# ---------------------------------------------------------------- propuestas
def _next_ids(df: pd.DataFrame):
    def mx(col, pref):
        n = 0
        if not df.empty and col in df:
            for v in df[col]:
                s = str(v).strip().upper()
                if s.startswith(pref) and s[len(pref):].isdigit():
                    n = max(n, int(s[len(pref):]))
        return n
    return mx("id", "L"), mx("posicion_id", "P")


def _size(capital, riesgo, tope, entrada, stop, fx, comision):
    dist = abs(entrada - stop)
    if dist <= 0 or entrada <= 0:
        return 0, "TOPE"
    por_riesgo = int(max(0.0, (capital * riesgo - 2 * comision)) // (dist * fx))
    por_tope = int((capital * tope) // (entrada * fx))
    return max(0, min(por_riesgo, por_tope)), ("RIESGO" if por_riesgo <= por_tope else "TOPE")


def _fila(idn, pid, tramo, ticker, lado, origen, regimen, entrada, stop, objetivo, acciones, riesgo_usd, capital, manda, nota):
    return {"id": f"L{idn:03d}", "posicion_id": f"P{pid:03d}", "tramo": tramo, "fecha_entrada": dt.date.today().isoformat(),
            "ticker": ticker, "lado": lado, "origen": origen, "regimen": regimen, "entrada": round(entrada, 2), "stop": round(stop, 2),
            "objetivo": round(objetivo, 2), "acciones": int(acciones), "riesgo_usd": round(riesgo_usd), "riesgo_pct": round(riesgo_usd / capital * 100, 2) if capital else None,
            "importe": round(acciones * entrada), "manda": manda, "estado": "PROPUESTA", "fecha_salida": "", "salida": "", "motivo_salida": "",
            "r_obtenido": "", "plan_cumplido": "", "nota": nota}


def propuestas(cfg: dict, res: dict, fichas: dict | None, dec: dict | None, cartera_data: dict | None) -> dict:
    p = cfg.get("_ledger") or parametros()
    capital, tope, com = float(p["capital"]), float(p["tope_posicion"]), float(p["comision_orden"] or 0)
    ops = operaciones()
    vt = veto()
    abiertas = ops[ops["estado"] == "ABIERTA"] if not ops.empty else ops
    n_abiertas = int(abiertas["posicion_id"].replace("", pd.NA).dropna().nunique()) if not abiertas.empty else 0
    tickers_abiertos = set(abiertas["ticker"]) if not abiertas.empty else set()
    lid, pid = _next_ids(ops)
    out = {"date": dt.date.today().isoformat(), "capital": capital, "ordenes": [], "tecnicas": [], "anadidos": [], "bloqueos": [],
           "n_abiertas": n_abiertas, "max_posiciones": p["max_posiciones"], "perdida_7d": perdida_7d(), "dudas": []}
    org = p["origenes"]
    bloqueo_total = False
    if n_abiertas >= p["max_posiciones"]:
        out["bloqueos"].append(f"{n_abiertas} posiciones abiertas (máximo {p['max_posiciones']}): no se proponen nuevas")
        bloqueo_total = True
    if out["perdida_7d"] > capital * p["perdida_semanal_max"]:
        out["bloqueos"].append(f"pérdida realizada de 7 días {out['perdida_7d']:,.0f} USD > {p['perdida_semanal_max']*100:.0f} % del capital: sin nuevas hasta el lunes".replace(",", "."))
        bloqueo_total = True
    regimen = f"{res['regime']['label']} / {res['tension']}"
    fmap = {f["t"]: f for f in (fichas or {}).get("fichas", [])}

    def permitido(t):
        if t in tickers_abiertos:
            return False, "ya abierta"
        if vt.get(t) == "NO":
            return False, "veto VALOR = NO"
        return True, ""

    def nueva(f, origen, nota):
        nonlocal lid, pid
        o = org.get(origen)
        if not o or not o["activo"]:
            return
        ok, why = permitido(f["t"])
        if not ok:
            return
        fx = float(f.get("fx_a_capital") or 1.0)
        entrada, stop = float(f["precio"]), float(f["stop"])
        acc, manda = _size(capital, o["riesgo"], tope, entrada, stop, fx, com)
        if acc <= 0:
            return
        if vt.get(f["t"]) == "DUDA":
            nota = "veto VALOR = DUDA; " + nota
            out["dudas"].append(f["t"])
        lid += 1; pid += 1
        riesgo_usd = acc * abs(entrada - stop) * fx + 2 * com
        fila = _fila(lid, pid, 1, f["t"], "LONG", origen, regimen, entrada, stop, entrada + 2 * (entrada - stop), acc, riesgo_usd, capital, manda,
                     nota + (f" (moneda {f['moneda']})" if f.get("moneda", "USD") != "USD" else ""))
        fila["empresa"] = f.get("name", f["t"]); fila["sector"] = f.get("sector", "")
        (out["ordenes"] if origen == "MACRO_TEC" else out["tecnicas"]).append(fila)

    if not bloqueo_total:
        # 1) MACRO_TEC: candidatas de la Decisión con orden posible
        hechos = set()
        for c in (dec or {}).get("candidatas", []):
            if not c.get("orden_posible"):
                continue
            f = fmap.get(c["ticker"])
            if not f:
                continue
            t = c["disparador_activo"][0] if c.get("disparador_activo") else {"nombre": "disparador", "detalle": ""}
            nueva(f, "MACRO_TEC", f"{t['nombre']}; acuerdo {c['patas']['a_favor']}/3; sector {c['sector']}")
            hechos.add(c["ticker"])
        # 2) TEC: disparador técnico en cualquier empresa de la watchlist, sector no vetado, sin apoyo macro
        vetados = {v["sector"] for v in (dec or {}).get("sectores_vetados", [])}
        for f in sorted(fmap.values(), key=lambda x: -(x.get("rel_3m") or -99)):
            if f["t"] in hechos or f["sector"] in vetados:
                continue
            if not (f.get("pullback_ma50") or f.get("breakout_52s")):
                continue
            if not f.get("cabe") or not f.get("sobre_ma200") or f.get("ventana_resultados"):
                continue
            disp = "retroceso a MA50" if f.get("pullback_ma50") else "ruptura de 52 semanas"
            nueva(f, "TEC", f"{disp}; sin apoyo macro; sector {f['sector']} {f.get('sesgo_sector', 0):+d}")
        out["tecnicas"] = out["tecnicas"][:6]

    # 3) Añadidos: tramos 2 y 3 sobre posiciones ABIERTAS en MACRO_TEC
    o = org.get("MACRO_TEC", {"riesgo": 0.01, "activo": True})
    precios = {px["ticker"]: px for px in (cartera_data or {}).get("posiciones", [])}
    if not abiertas.empty and "posicion_id" in abiertas:
        for pos_id, g in abiertas.groupby("posicion_id"):
            if not pos_id or (g["origen"] != "MACRO_TEC").all():
                continue
            g = g.sort_values("tramo")
            t1 = g.iloc[0]
            ticker = t1["ticker"]
            f = fmap.get(ticker); pr = precios.get(ticker)
            price = float(pr["precio"]) if pr else (float(f["precio"]) if f else None)
            if price is None or t1.get("entrada") is None or t1.get("stop") is None:
                continue
            e1, s1 = float(t1["entrada"]), float(t1["stop"])
            R = abs(e1 - s1)
            if R <= 0:
                continue
            lado = 1 if str(t1.get("lado", "LONG")).upper() != "SHORT" else -1
            avance = (price - e1) * lado / R
            tramos = set(int(x) for x in g["tramo"].dropna()) if g["tramo"].notna().any() else {1}
            fx = float(f.get("fx_a_capital") or 1.0) if f else 1.0
            tot_imp = float(sum((g["acciones"].fillna(0) * g["entrada"].fillna(0)) * fx))
            if 2 not in tramos and avance >= 1.0:
                acc = int(max(0.0, capital * o["riesgo"] * PESOS_TRAMOS[1] - 2 * com) // (R * fx))
                acc = min(acc, int(max(0.0, capital * tope - tot_imp) // (price * fx)))
                if acc > 0:
                    lid += 1
                    nuevo_stop = e1
                    fila = _fila(lid, int(str(pos_id)[1:]) if str(pos_id)[1:].isdigit() else 0, 2, ticker, "LONG" if lado == 1 else "SHORT", "MACRO_TEC",
                                 regimen, price, nuevo_stop, e1 + lado * 2 * R, acc, acc * abs(price - nuevo_stop) * fx + 2 * com, capital, "RIESGO",
                                 f"tramo 2: precio a +{avance:.1f}R; stop de toda la posición a la entrada 1 ({e1:.2f})")
                    fila["posicion_id"] = str(pos_id)
                    fila["tramos_previos"] = sorted(tramos)
                    out["anadidos"].append(fila)
            elif 2 in tramos and 3 not in tramos and f and (avance >= 2.0 or (f.get("pullback_ma50") and avance > 1.0)):
                acc = int(max(0.0, capital * o["riesgo"] * PESOS_TRAMOS[2] - 2 * com) // (R * fx))
                acc = min(acc, int(max(0.0, capital * tope - tot_imp) // (price * fx)))
                if acc > 0:
                    lid += 1
                    nuevo_stop = float(f["stop"])  # mínimo de 20 sesiones / 2 ATR, el más cercano
                    fila = _fila(lid, 0, 3, ticker, "LONG" if lado == 1 else "SHORT", "MACRO_TEC", regimen, price, nuevo_stop,
                                 e1 + lado * 3 * R, acc, acc * abs(price - nuevo_stop) * fx + 2 * com, capital, "RIESGO",
                                 f"tramo 3: precio a +{avance:.1f}R; stop de toda la posición al último mínimo ({nuevo_stop:.2f})")
                    fila["posicion_id"] = str(pos_id)
                    fila["tramos_previos"] = sorted(tramos)
                    out["anadidos"].append(fila)
    return out


def save(pr: dict):
    DATA.mkdir(exist_ok=True)
    (DATA / "propuestas.json").write_text(json.dumps(pr, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


# ---------------------------------------------------------------- email
def _tabla(filas: list) -> str:
    cols = [c for c in COLS if c not in ("estado", "fecha_salida", "salida", "motivo_salida", "r_obtenido", "plan_cumplido")]
    h = ["<table cellpadding='3' style='border-collapse:collapse;font-size:11px;width:100%'><tr style='background:#f0f0f0'>"]
    h += [f"<th align='left'>{c}</th>" for c in cols]
    h.append("</tr>")
    for f in filas:
        h.append("<tr>" + "".join(f"<td style='border-bottom:1px solid #eee;white-space:nowrap'>{f.get(c, '')}</td>" for c in cols) + "</tr>")
    h.append("</table>")
    return "\n".join(h)


def to_html(pr: dict | None) -> str:
    if not pr:
        return ""
    h = [f"<h4 style='margin:10px 0 4px'>Ledger · {pr['n_abiertas']} posiciones abiertas de {pr['max_posiciones']}"
         + (f" · pérdida 7 días {pr['perdida_7d']:,.0f} USD".replace(",", ".") if pr.get("perdida_7d") else "") + "</h4>"]
    if pr["bloqueos"]:
        h.append("<p style='margin:0 0 6px;color:#b00;font-size:13px'><b>Bloqueos:</b> " + "; ".join(pr["bloqueos"]) + ".</p>")
    for key, titulo, vacio in (("ordenes", "Órdenes propuestas (MACRO_TEC)", "ninguna candidata con disparador activo y apoyo macro"),
                               ("tecnicas", "Candidatas técnicas (TEC, sin apoyo macro, riesgo reducido)", "ningún disparador técnico en sectores no vetados"),
                               ("anadidos", "Añadidos propuestos (tramos 2 y 3)", "ninguna posición MACRO_TEC en condición de añadir")):
        filas = pr.get(key, [])
        h.append(f"<p style='margin:8px 0 2px;font-size:13px'><b>{titulo}:</b> " + (f"{len(filas)}" if filas else vacio) + "</p>")
        if filas:
            h.append("<p style='margin:0 0 4px;font-size:12px;color:#555'>" + "; ".join(f"<b>{f.get('empresa', f['ticker'])}</b>: {f['nota']}" for f in filas) + "</p>")
            h.append(_tabla(filas))
    if pr.get("dudas"):
        h.append(f"<p style='margin:4px 0;font-size:12px;color:#8a5a0a'>Veto VALOR en DUDA: {', '.join(pr['dudas'])}.</p>")
    h.append("<p style='margin:4px 0 8px;font-size:11px;color:#999'>Cada fila va en el orden de columnas del Ledger: valida el stop en el gráfico, "
             "copia la fila a Operaciones y cambia el estado a ABIERTA (o RECHAZADA con el motivo).</p>")
    return "\n".join(h)


def summary_for_llm(pr: dict | None) -> dict:
    if not pr:
        return {}
    return {"n_abiertas": pr["n_abiertas"], "bloqueos": pr["bloqueos"],
            "ordenes_propuestas": [{"ticker": f["ticker"], "acciones": f["acciones"], "entrada": f["entrada"], "stop": f["stop"], "riesgo_pct": f["riesgo_pct"]} for f in pr["ordenes"]],
            "candidatas_tecnicas": [f["ticker"] for f in pr["tecnicas"]],
            "anadidos": [{"ticker": f["ticker"], "tramo": f["tramo"], "acciones": f["acciones"]} for f in pr["anadidos"]]}


# ---------------------------------------------------------------- comprobación
def check() -> list:
    """Lee las cuatro pestañas y devuelve los problemas encontrados (lista vacía = todo bien)."""
    problemas = []
    esperado = {"operaciones": COLS, "parametros": [], "veto": ["ticker", "apta"], "temas": ["tema", "ticker"]}
    for key in ENV:
        if not os.environ.get(ENV[key]):
            problemas.append(f"{ENV[key]} no definida")
            continue
        try:
            df = _read(key)
        except Exception as e:  # noqa: BLE001
            problemas.append(f"{key}: no se puede leer ({e})")
            continue
        falta = [c for c in esperado[key] if c not in df.columns]
        if falta:
            problemas.append(f"{key}: faltan columnas {falta}")
    if not problemas:
        p = parametros()
        if not p["origenes"]:
            problemas.append("parametros: tabla de orígenes vacía")
    return problemas
