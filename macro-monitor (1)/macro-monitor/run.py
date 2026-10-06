"""
macro-monitor — rutina principal.

  python run.py daily     -> informe completo (todas las series + calendario) y email
  python run.py event     -> solo series headline publicadas HOY; email solo si hay novedad
  python run.py calendar  -> regenera docs/macro.ics (publicaciones FRED + FOMC/BCE)
  python run.py daily --no-email   -> imprime en consola, no envía
"""
import sys
import json
import datetime as dt
import pathlib
import yaml

from macro_monitor import fetch, analyze, report, calendar as cal_mod

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "output"


def load_config():
    return yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))


def build_rows(cfg, only_headline=False, only_updated_today=False):
    years = cfg.get("lookback_years", 10)
    rows, by_id = [], {}
    today = dt.date.today().isoformat()

    for sc in cfg["fred"]:
        if only_headline and not sc.get("headline"):
            continue
        row = {"id": sc["id"], "name": sc["name"], "block": sc["block"], "unit": sc.get("unit", "")}
        try:
            if only_updated_today:
                meta = fetch.fred_meta(sc["id"])
                if meta["last_updated"] != today:
                    continue
            s = fetch.fred_series(sc["id"], years)
            row.update(analyze.compute(s, sc.get("transform", "level"), sc))
        except Exception as e:  # noqa: BLE001
            row["error"] = f"error: {e}"
        rows.append(row)
        by_id[sc["id"]] = row

    if not only_headline:
        for mc in cfg.get("market", []):
            row = {"id": mc["ticker"], "name": mc["name"], "block": "Mercado", "unit": ""}
            try:
                s = fetch.market_series(mc["ticker"], years)
                row.update(analyze.compute(s, "level", mc))
            except Exception as e:  # noqa: BLE001
                row["error"] = f"error: {e}"
            rows.append(row)
            by_id[mc["ticker"]] = row
    return rows, by_id


def collect_alerts(rows):
    return [{"name": r["name"], "msg": m, "value": r["value"]}
            for r in rows if "alerts" in r for m in r["alerts"]]


def write_calendar(cfg, by_id=None):
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    ics = cal_mod.build_ics(cfg, by_id)
    (docs / "macro.ics").write_text(ics, encoding="utf-8")
    n = ics.count("BEGIN:VEVENT")
    print(f"Calendario generado: docs/macro.ics ({n} eventos)")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    send = "--no-email" not in sys.argv
    cfg = load_config()
    OUT.mkdir(exist_ok=True)
    today = dt.date.today().isoformat()

    if mode == "daily":
        rows, by_id = build_rows(cfg)
        reg = analyze.regime(by_id)
        alerts = collect_alerts(rows)
        try:
            cal = fetch.fred_calendar(7)
        except Exception as e:  # noqa: BLE001
            cal = [{"date": "", "release": f"(calendario no disponible: {e})"}]
        try:
            write_calendar(cfg, by_id)
        except Exception as e:  # noqa: BLE001
            print(f"(calendario no regenerado: {e})")
        title = "Macro Monitor · Nota diaria"
        html = report.render_html(rows, reg, cal, alerts, title)
        text = report.render_text(rows, reg, alerts)
        subject = f"[Macro] {today} · {reg['label'].split(' (')[0]}" + (f" · {len(alerts)} alertas" if alerts else "")

    elif mode == "event":
        rows, by_id = build_rows(cfg, only_headline=True, only_updated_today=True)
        rows = [r for r in rows if "error" not in r]
        if not rows:
            print("Sin publicaciones headline hoy. Nada que enviar.")
            return
        reg = analyze.regime(by_id)
        alerts = collect_alerts(rows)
        title = "Macro Monitor · Dato publicado hoy"
        html = report.render_html(rows, reg, [], alerts, title)
        text = report.render_text(rows, reg, alerts)
        names = ", ".join(r["name"] for r in rows)
        subject = f"[Macro · DATO] {today} · {names}"
    elif mode == "calendar":
        write_calendar(cfg)
        return
    else:
        raise SystemExit("modo desconocido: usa daily | event | calendar")

    (OUT / f"{mode}_{today}.html").write_text(html, encoding="utf-8")
    (OUT / f"{mode}_{today}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(text)

    if send:
        report.send_email(subject, html, text)
        print(f"\nEmail enviado: {subject}")


if __name__ == "__main__":
    main()
