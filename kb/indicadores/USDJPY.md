---
tipo: indicador
id: JPY=X
nombre: Dólar-yen
bloque: Mercado
fuente: yfinance (JPY=X), yenes por dólar
frecuencia: diaria (continuo)
publicacion: continuo
en_el_motor: panel; factor "yen" (USDJPY −4 en el mes = yen apreciándose: carga +0,5 en tecnología, comunicación, discrecional y financiero → −0,5); disparador < 150
relacionados: [DX-Y.NYB, ^VIX, ^GSPC, DGS10, divisas, liquidez-global-y-carry, deshacer-del-carry]
actualizado: 2026-10-09
---

# Dólar-yen

Cuántos yenes vale un dólar. Japón ha tenido tipos cercanos a cero durante 25 años, y el yen ha sido la moneda en la que el mundo pide prestado para invertir en activos de riesgo (carry trade). Un dólar-yen alto y subiendo (yen débil) significa carry acumulándose: combustible para los activos de riesgo mientras dure, y para una sacudida cuando se deshaga. El 5 de agosto de 2024 es el ejemplo: el yen subió un 12 % en tres semanas y el Nikkei cayó un 12 % en un día.

## Cómo se lee
| USD/JPY | Lectura (2022-2026) |
| --- | --- |
| > 155 | Yen muy débil; intervenciones del Ministerio de Finanzas japonés probables (2022: 152; 2024: 160); carry en máximos |
| 140-155 | Rango de los últimos años |
| < 140 | Yen fuerte; el carry se ha deshecho o el BoJ ha subido; riesgo para activos de riesgo globales |

Lo que importa es la **velocidad**: −4 en un mes (de 158 a 154) es el aviso; −10 en tres semanas (agosto 2024) es el deshacer. El cruce sigue de cerca al diferencial de tipos a 10 años EE.UU.-Japón (el 10 años japonés sube desde 2023: 1-1,5 %) y se mueve en sentido contrario al VIX en los episodios de pánico.

## Qué lo mueve
Diferencial de tipos EE.UU.-Japón (el principal), política del Banco de Japón (salida de tipos negativos en marzo de 2024, subidas lentas desde entonces), intervenciones directas (venta de dólares por el Ministerio de Finanzas: septiembre-octubre 2022, abril-mayo 2024, julio 2024), aversión al riesgo (el yen sube en pánico), y flujos de inversores japoneses (los mayores tenedores extranjeros de Treasuries).

## Qué mueve
- Activos de riesgo globales vía carry: Nasdaq, emergentes, cripto, Nikkei.
- Exportadoras japonesas (Toyota, Sony): ganan con yen débil; el Nikkei sube con USD/JPY.
- Treasuries: si los inversores japoneses repatrían (yen subiendo, tipos japoneses atractivos), venden Treasuries y el 10 años americano sube.
- Para la watchlist: efecto indirecto vía apetito por el riesgo y vía competencia (automoción alemana frente a japonesa con yen débil).

## Umbrales en el motor
Factor "yen": USDJPY −4 en un mes activa señal −1 con carga +0,5 en los sectores más comprados con carry (tecnología, comunicación, discrecional, financiero), es decir, −0,5 en cada uno. Disparador en 150 (desde 158): el nivel por debajo del cual el carry empieza a perder dinero para muchas posiciones.

## Casuísticas relacionadas
→ [[deshacer-del-carry]]: cómo identificarlo y qué hacer.
→ [[dolar-sube-con-bolsa-cayendo]]: el yen y el dólar como refugios compiten; cuando sube el yen y cae el dólar es carry; cuando suben los dos, es pánico.

## Trampas de lectura
- Las intervenciones japonesas mueven el cruce 4-5 yenes en horas y revierten en semanas; no leer una intervención como cambio de tendencia.
- El BoJ sube tipos muy despacio (25 pb al año); el diferencial con EE.UU. sigue siendo enorme; el carry no desaparece, se interrumpe.
- El tamaño del carry no se conoce; las estimaciones (BIS, bancos de inversión) van de 500.000 M$ a 4 billones según qué se cuente.

## Episodios
- **Octubre 2022**: 152, máximo en 32 años; intervención de 60.000 M$; el yen rebotó a 128 en enero de 2023 cuando el BoJ amplió la banda del 10 años.
- **Abril-julio 2024**: 162, máximo en 38 años; intervenciones en mayo y julio; subida del BoJ el 31 de julio; deshacer del carry el 5 de agosto (142 el 5 de agosto).
- **Octubre 2026**: 158,3, +4,5 en el mes, percentil 95; carry acumulándose; disparador en 150.

## Para profundizar
- Banco de Japón, decisiones y perspectivas: https://www.boj.or.jp/en/mopo/index.htm
- Ministerio de Finanzas de Japón, intervenciones (publicadas mensualmente): https://www.mof.go.jp/english/policy/international_policy/reference/feio/index.htm
- CFTC, posicionamiento en yen (COT): https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- BIS, carry trade (informes trimestrales): https://www.bis.org/publ/qtrpdf/
