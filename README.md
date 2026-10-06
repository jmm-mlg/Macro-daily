# macro-monitor

Panel diario de datos macro que mueven la bolsa. Corre en GitHub Actions, sin ordenador encendido,
y manda el resumen por email. Fuentes gratuitas: FRED (St. Louis Fed) y Yahoo Finance.

## Qué hace

- **Nota diaria** (lunes a viernes, ~07:30 CET): ~30 series en 7 bloques (tipos, inflación, empleo,
  actividad, vivienda, crédito, mercado). Para cada una: último valor, variación, percentil en 10 años,
  alertas por umbral. Añade un **semáforo de régimen** (crecimiento × inflación) y el calendario de
  publicaciones de los próximos 7 días.
- **Alerta de dato** (~14:15 y ~15:15 UTC): si hoy se ha publicado alguna serie marcada `headline`
  (IPC, PCE, nóminas, paro, PIB, ventas minoristas), manda un email solo con eso. Si no hay nada, no envía.

- **Calendario para Google Calendar**: cada día regenera `docs/macro.ics` con las publicaciones
  de los próximos 60 días (hora exacta, series afectadas, último valor) y las reuniones FOMC y BCE
  (`central_banks.yaml`). Se sirve por GitHub Pages y Google Calendar lo lee por suscripción.

## Puesta en marcha

1. Crea el repo y sube estos archivos.
2. API key de FRED (gratis): https://fred.stlouisfed.org/docs/api/api_key.html
3. En **Settings → Secrets and variables → Actions** añade:

| Secret | Valor |
|---|---|
| `FRED_API_KEY` | tu clave de FRED |
| `SMTP_HOST` | `smtp.gmail.com` (u otro) |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | tu email remitente |
| `SMTP_PASS` | contraseña de aplicación (en Gmail: cuenta → Seguridad → Contraseñas de aplicaciones) |
| `EMAIL_TO` | destinatario(s), separados por coma |

4. Lanza a mano **Actions → Macro daily → Run workflow** para probar.
5. **Google Calendar**: en el repo, Settings → Pages → Source: *Deploy from a branch*, rama `main`,
   carpeta `/docs`. Tras el primer run existirá `https://<usuario>.github.io/macro-monitor/macro.ics`.
   En Google Calendar: *Otros calendarios → + → Desde URL* y pega esa dirección. Google lo refresca
   cada 12-24 h (las publicaciones se conocen con semanas de antelación, así que es suficiente).
   Si no quieres activar Pages, vale también la URL raw:
   `https://raw.githubusercontent.com/<usuario>/macro-monitor/main/docs/macro.ics`.

## Uso local

```bash
pip install -r requirements.txt
export FRED_API_KEY=...
python run.py daily --no-email     # imprime en consola, guarda output/daily_<fecha>.html
python run.py event --no-email
python run.py calendar             # solo regenera docs/macro.ics
```

## Personalizar

Todo está en `config.yaml`: añade o quita series FRED (cualquier id de https://fred.stlouisfed.org),
cambia la transformación (`level`, `diff`, `mom`, `yoy`, `qoq_ann`), marca `headline: true` para
que entre en la alerta de evento, o pon umbrales con `alert: {above: X, msg: "..."}`.

Calendario: en `config.yaml → calendar.releases` eliges qué releases de FRED entran (por fragmento del
nombre), su hora ET e importancia (🔴🟠⚪). Las reuniones de bancos centrales van en `central_banks.yaml`
(añadir las del año siguiente cuando Fed y BCE las publiquen).

## Límites conocidos (V1)

- No hay **consenso de analistas**, así que no mide la sorpresa. La variación es vs dato anterior / hace un mes.
- Los **PMI de S&P Global** y la serie completa de Michigan son de pago; el ISM no está en FRED.
- El percentil usa la ventana cargada (10 años), no toda la historia.

## Siguientes pasos previstos

- V2: webhook Apps Script para eventos instantáneos en el calendario principal (si hace falta).
- V3: escribir cada nota en la base "Temas macro" de Notion vía API.
- V4: expectativa propia (media móvil) como proxy de consenso para medir sorpresa.
- V5: datos europeos ampliados (ECB Data Portal, Eurostat, INE).
