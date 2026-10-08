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

- **Calendario de empresas**: a partir de `watchlist.yaml` (185 empresas representativas por industria
  GICS, EE.UU. + Europa, con rol bellwether/representante) genera `docs/empresas.ics` (solo bellwethers,
  con aviso el día anterior) y `docs/empresas-todas.ics` (toda la lista, ex-dividendos y quad witching,
  sin aviso). Fechas de resultados vía Finnhub (hora pre/post mercado) con yfinance de respaldo.
  El email diario incluye la sección "Esta semana en tus empresas".

- **Motor de reglas** (`rules.yaml` + `macro_monitor/rules.py`): cuatro scores (crecimiento, inflación,
  liquidez, riesgo) de −2 a +2, régimen (cuadrante crecimiento × inflación), tensión del cuadro, sesgo por
  sector GICS (matriz régimen × sector + sensibilidades a factores), divergencias entre series y
  disparadores de cambio de conclusión. Cada umbral lleva su justificación en el YAML.
- **Histórico**: cada run guarda `data/history.csv` (todas las series), `data/scores.csv` (scores,
  régimen y sesgos por sector) y `data/latest.json`, commiteados al repo. Es la base del dashboard y
  de la validación de los sesgos contra los ETFs sectoriales.

- **Nota del comité** (`macro_monitor/narrativa.py`): Groq (`gpt-oss-120b`, respaldo `20b`) redacta
  cada día una nota de cinco secciones (qué ha cambiado, lectura del cuadro, esta semana, para la
  cartera, qué cambiaría la conclusión) a partir ÚNICAMENTE del JSON del motor. Se archiva en
  `data/narrativas.md`. Sin clave, el informe sale sin ella.

- **Capa micro** (`macro_monitor/micro.py`): por empresa de la watchlist, revisiones de estimaciones
  de analistas (yfinance), hechos relevantes 8-K con su tipo (SEC EDGAR), operaciones de insiders Form 4
  con detección de "cluster buying" (3+ compradores en 30 días), y discursos/comunicados de Fed y BCE
  clasificados halcón/paloma por Groq. Agrega un pulso por sector (amplitud de revisiones) y marca
  **conflictos** donde el sesgo macro y los analistas discrepan. Bellwethers a diario, toda la lista los lunes.
  Europa: revisiones sí, 8-K/insiders no (no hay equivalente a EDGAR).

- **Base de conocimiento** (`kb/`): una entrada por serie del email (36), casuísticas, sectores,
  mecanismos y biblioteca de fuentes gratuitas. El email enlaza cada serie a su entrada (`kb_url` en
  `config.yaml`). `kb/verificar.py` comprueba las afirmaciones fechadas de las entradas contra FRED y
  yfinance (`kb/verificacion.yaml`) y deja el informe en `kb/_verificacion.md`; corre el día 1 de cada
  mes y a mano desde Actions → "Verificar base de conocimiento".

## Puesta en marcha

1. Crea el repo y sube estos archivos.
2. API key de FRED (gratis): https://fred.stlouisfed.org/docs/api/api_key.html
3. En **Settings → Secrets and variables → Actions** añade:

| Secret | Valor |
|---|---|
| `FRED_API_KEY` | tu clave de FRED |
| `GROQ_API_KEY` | opcional; clave de console.groq.com para la "Nota del comité" (narrativa LLM) |
| `EDGAR_USER_AGENT` | opcional pero recomendado; la SEC pide identificarse: `"Nombre email@dominio"` |
| `FINNHUB_API_KEY` | opcional; clave gratuita de finnhub.io (hora pre/post mercado de los resultados EE.UU.) |
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
python run.py empresas             # solo regenera docs/empresas*.ics
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

## Divisas
El panel incluye euro-dólar, dólar-yen y dólar-yuan (yfinance). El motor usa el dólar (DXY) como factor
sectorial, el yen como factor de carry (USDJPY −4 en un mes → −0,5 en tecnología, comunicación,
discrecional y financiero; disparador < 150) y el euro como factor narrativo (> ±3 %/mes) para la lectura
de las empresas europeas. Marco completo en `kb/conceptos/divisas.md`.

## Pulso de mercado (`macro_monitor/pulso.py`)
Variaciones a 1 día / 1 semana / 1 mes / 3 meses en cinco bloques (Mercado: S&P, Nasdaq, equiponderado, Russell;
VIX y VIX a 3 meses; Treasuries 2/10/30, real, breakeven, curva; Crédito HY/IG/CCC y los ETFs HYG/LQD;
Liquidez: balance de la Fed, cuenta del Tesoro, repo inverso, reservas, NFCI, y la **liquidez neta** =
balance − TGA − RRP) y seis medidas de régimen: estructura del VIX (backwardation), VIX frente a volatilidad
realizada, descomposición del movimiento del 10 años en real y breakeven, tipo de empinamiento, **mercado −
liquidez** (diferencia de z-scores a 3 meses), **prima de riesgo** (earnings yield de SPY − tipo real) y
**correlación acciones-bonos** a 60 días. Señales en el email y en la narrativa; histórico en `data/pulso.csv`.

## Series añadidas el 2026-10-09 (a partir de la base de conocimiento)
Supercore (CUSR0000SASL2RS), peticiones continuadas (CCSA), tasa de renuncias (JTSQUR), utilización
de la capacidad (TCU), grupo de control de ventas (RSCCAS), tasa de ahorro (PSAVERT), morosidad de
tarjetas (DRCCLACBS), gas TTF (TTF=F) y el ratio cobre/oro (CU_AU, serie derivada en `config.yaml →
derived`). Si FRED rechaza un id, la fila sale como "error" en el panel y el resto no se ve afectado.

## Motor de reglas: cómo leerlo

- Score = suma ponderada de señales; cada señal evalúa nivel (percentil o umbral absoluto) y tendencia.
- Régimen: signo de crecimiento × signo de inflación. Si uno es 0, régimen "Mixto": los sesgos
  sectoriales salen solo de los factores, no de la matriz.
- Sesgo sector = base de la matriz (según régimen) + Σ carga × señal de factor, acotado a ±2.
- Tensión: liquidez ≤ −1 con riesgo ≥ +1 = "alta" (valoraciones altas con tipos restrictivos).

## Siguientes pasos previstos

- `run.py validar`: comparar sesgos históricos con el retorno real de XLF/XLE/XLK… a 1 y 3 meses.
- Dashboard estático en GitHub Pages leyendo `data/latest.json` y `data/scores.csv`.
- V2: webhook Apps Script para eventos instantáneos en el calendario principal (si hace falta).
- V3: escribir cada nota en la base "Temas macro" de Notion vía API.
- V4: expectativa propia (media móvil) como proxy de consenso para medir sorpresa.
- V5: datos europeos ampliados (ECB Data Portal, Eurostat, INE).
