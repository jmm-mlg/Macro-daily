# Macro Monitor · estado del proyecto y guía para retomar

Última actualización: 2026-10-13. Este archivo es el punto de entrada para continuar el proyecto en una sesión nueva.
Léelo entero antes de tocar nada; después, `README.md` (detalle técnico) y `kb/README.md` (índice de la base).

## 1. Qué es
Sistema diario, gratuito y sin ordenador encendido (GitHub Actions) que: descarga 48 series macro y de mercado,
calcula régimen, scores y sesgos por sector (motor de reglas), lee 251 empresas (revisiones, 8-K, insiders, fichas
técnicas), calcula una **Decisión del día** (exposición, dónde buscar, candidatas con disparadores concretos, matriz
de acuerdo, casuísticas activas, sensibilidad) y la explica con una nota redactada por un LLM; valora la cartera
registrada en CSV; y publica una base de conocimiento de 159 entradas como sitio web. Todo llega por email a las 07:30.

- Repo: `jmm-mlg/Macro-daily` (público). Pages: `https://jmm-mlg.github.io/Macro-daily/` (calendarios `.ics` y `kb/`).
- Usuario: opera en paper (IBKR) con capital de referencia 1.000.000 USD, riesgo 0,5-1 % por operación según cuadro.
- Guía de lectura (7 niveles): documento Claude Docs `c517c2c3-375a-4ffd-965c-b6438da61c4e`, exportada a `guia-de-lectura-macro-monitor.md`.
- Proyecto de Claude "Analista senior · Macro Monitor": conocimiento = `kb/` + guía + `rules.yaml`; instrucciones ya redactadas (ver sesión del 10/10).

## 2. Cómo trabajamos (convenciones)
- Las entregas son zips con la estructura del repo (`delta/...`): se descomprimen encima de la carpeta de GitHub Desktop, "reemplazar", commit, push. La carpeta `.github` está oculta en Windows: si un workflow no se actualiza, se edita por la web.
- Workflows en Python 3.12 (`daily.yml`, `event.yml`, `verificar-kb.yml`, `kb-site.yml`, `benchmarks.yml`). Antes era 3.11: no usar f-strings con comillas anidadas del mismo tipo.
- El email se lanza a mano (Actions → Macro daily → Run workflow) porque el cron de GitHub llega con horas de retraso; alternativa documentada: cron externo (cron-job.org + token fino) a las 07:15 Europe/Madrid.
- Micro completo (251 empresas, 15-20 min) a demanda: Run workflow con la casilla "micro_completo", o `python run.py micro all`.
- Groq gratuito limita a ~8.000 tokens/min por modelo: el payload de la narrativa se recorta a 12 KB (`narrativa.fit_payload`); Gemini es respaldo automático (`GEMINI_API_KEY`), o principal con la variable `LLM_PROVIDER=gemini`.
- FRED sirve las series ICE BofA solo ~3 años por API: el percentil de los spreads es a 3 años (el email lo marca).
- Cada umbral o peso de `rules.yaml` lleva fecha y motivo. Cada entrada de la base sigue `kb/PLANTILLA.md` (9 campos) y se escribe en español.

## 3. Secrets y variables (Settings → Secrets and variables → Actions)
`FRED_API_KEY`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_TO`, `GROQ_API_KEY`, `EDGAR_USER_AGENT`,
`GEMINI_API_KEY` (respaldo LLM), `FINNHUB_API_KEY` (opcional; la clave actual devuelve 401: revisar o borrar).
Variable opcional: `LLM_PROVIDER` (gemini | groq).

## 4. Mapa del código (`macro_monitor/`)
| Módulo | Qué hace | Salida |
| --- | --- | --- |
| `fetch.py` | FRED (con reintentos) y yfinance | series |
| `analyze.py` | valor, variación, percentil (ventana real `pct_years`), alertas | filas del panel |
| `rules.py` | scores, régimen, tensión, factores, matriz sectorial, divergencias, disparadores; histórico | `data/scores.csv`, `triggers.csv`, `latest.json` |
| `report.py` | HTML/texto del email, enlaces a la base (`kb_url` en `config.yaml`) | email |
| `calendar.py`, `empresas.py` | `macro.ics`, `empresas.ics`, `empresas-todas.ics`; resultados y ex-dividendos (yfinance, Finnhub opcional) | `docs/*.ics` |
| `micro.py` | revisiones de analistas, 8-K/Form 4 (EDGAR), bancos centrales (RSS + LLM), conflictos macro/micro | `data/micro.json` |
| `pulso.py` | variaciones 1d/1s/1m/3m por bloque, liquidez neta, VIX, curva, prima de riesgo, correlación | `data/pulso.json/.csv` |
| `ficha.py` | fichas técnicas (stop, tamaño en USD, fuerza relativa, estado de tendencia, retroceso/ruptura), momentum de 22 ETFs | `data/fichas.csv`, `momentum_sectorial.csv` |
| `cartera.py` | valora `cartera/operaciones.csv`: P&L acción/divisa, R, avisos, límites, cerradas | `data/cartera_estado.csv` |
| `benchmark.py` | lee `kb/benchmarks/benchmarks.yaml`; compara una empresa con su industria (yfinance info) | lectura por candidata |
| `decision.py` | Decisión del día: banda, sectores, candidatas (embudo), **patas y disparadores**, casuísticas activas, sensibilidad, deltas, historial | `data/decision.json` |
| `llm.py` | cliente Groq + Gemini con reintentos | texto |
| `narrativa.py` | prompt de seis secciones orientadas a decisión; recorte de payload; comprobación de vocabulario y signos | `data/narrativas.md` |

Configuración: `config.yaml` (series, mercado, derivadas, micro, ficha/tamaño, kb_url), `rules.yaml` (todas las reglas),
`watchlist.yaml` v2 (251 empresas, 85 industrias), `central_banks.yaml`, `cartera/operaciones.csv` (registro manual).

Base de conocimiento (`kb/`): indicadores (38), sectores (11), mecanismos (15), casuísticas (80), conceptos (divisas),
benchmarks (11 + `benchmarks.yaml` + `correspondencia.yaml` + `actualizar.py`), `BIBLIOTECA.md`, `PLANTILLA.md`,
`verificar.py` + `verificacion.yaml` (68 afirmaciones; 7 manuales por ICE BofA), `build_nav.py` + `_hooks.py` (sitio MkDocs).

## 5. Reglas de negocio que hay que respetar al ampliar
- Embudo (guía, nivel 5): régimen → sector → empresa → disparador con fecha. Régimen manda y veta; tendencia filtra; predictiva confirma.
- Tamaño: capital 1.000.000 USD; riesgo 0,5 % base +0,25 (Goldilocks/Reflación sin tensión alta) +0,25 (sector +2 sin conflicto), tope 1 %; stop ≤ 8 %; posición ≤ 10 % (5 % en Mixto o tensión alta); matriz de acuerdo 3/3 completo, 2/3 mitad, 1/3 no; en Mixto máximo mitad.
- Límites de cartera: ≤ 12 posiciones, ≤ 25 % por sector, ≤ 70 % por región, ≤ 2 posiciones por factor, riesgo abierto ≤ 5 %.
- La narrativa no calcula: explica la decisión del motor; no puede contradecir "abrir_hoy"; vocabulario del sistema prohibido.
- Nunca recomendar una empresa sin disparador activo; el disparador macro es contexto, no abre.

## 6. Estado de los datos (13/10/2026)
Régimen Mixto/transición, tensión media. Crecimiento 0, inflación +1, liquidez −1, riesgo 0. Tipo real 2,92 % (máximo de la
década), 10 años 5,28 %, HY 309 pb (CCC +173 pb en un mes), nóminas +29k con peticiones 197k, IPC 3,71 % / subyacente 2,76 % /
PCE 3,01 %, Michigan 51,7, S&P 500 en máximos, prima de riesgo 1,1 %, correlación acciones-bonos +0,42, euro 1,12, dólar-yen 158.
Decisión: exposición 50-70 %, buscar solo en Energía; Shell y Exxon con ruptura de 52 semanas y acuerdo 3/3 (factor 0,5);
Repsol, Conoco, Chevron, Total con disparadores pendientes. Sin posiciones registradas aún.

## 7. Pendiente, por orden de valor
1. **Scores completos de tendencia y predictiva** (−2…+2, pesos en `rules.yaml`; diseño acordado el 11/10: estructura, momentum 12-1, fuerza relativa, calidad de tendencia, distancia a máximos; revisiones, sorpresas de resultados, calidad y valoración contra industria, hechos). Hoy `decision.legs()` usa signos provisionales. Sustituir sin cambiar la matriz; guardar los tres scores a diario por empresa para validar.
2. **Validación** (`run.py validar`): sesgos sectoriales vs ETFs a 1 y 3 meses; acierto por pata y régimen. Necesita ~1 mes de `data/`; preparar el código ya.
3. **Salidas y rotación**: tres salidas por posición (tendencia rota, revisiones giradas, régimen cambiado) y reemplazo por ranking; columnas de las tres patas al abrir en `cartera/operaciones.csv`.
4. **COT** (CFTC semanal): z-score de posicionamiento en S&P, 10 años, crudo, cobre, oro, euro, yen.
5. **Dashboard** en Pages leyendo `data/` (mockup hecho en sesión anterior).
6. Base: `episodios/` (una entrada por crisis), conceptos (prima de riesgo, duración, R, ATR, Sahm, Beveridge), casuística "CCC se amplía con HY contenido".
7. **Semiautomatización IBKR paper** cuando haya 15-20 operaciones registradas.
Mantenimiento: cron tras el cambio de hora (26/10); umbral PCE en `rules.yaml` tras cada SEP (dic/mar/jun/sep); benchmarks se regeneran el 15/01.

## 8. Cómo retomar en una sesión nueva
1. Leer este archivo y pegar el último email (o `data/decision.json` y `data/narrativas.md`).
2. Para cualquier cambio: trabajar sobre los archivos del repo, probar con datos reales de yfinance (FRED no es accesible sin clave desde el entorno de Claude: usar filas simuladas con los valores del email), entregar como zip `delta/`.
3. Comprobar siempre: `python -c "import ast; ..."` de cada módulo, `yaml.safe_load` de cada YAML, y que no haya f-strings con comillas anidadas.
