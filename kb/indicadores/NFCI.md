---
tipo: indicador
id: NFCI
nombre: Índice de condiciones financieras de la Fed de Chicago (NFCI)
bloque: Crédito
fuente: Reserva Federal de Chicago vía FRED (NFCI)
frecuencia: semanal
publicacion: miércoles a las 8:30 ET con datos de la semana anterior (viernes)
en_el_motor: alerta > 0; peso 3 (invertido) en liquidez (> 0 restrictivo, < −0,5 laxo)
relacionados: [DFII10, BAMLH0A0HYM2, VIX, DX-Y.NYB, condiciones-financieras, liquidez]
actualizado: 2026-10-08
---

# Índice de condiciones financieras (NFCI)

Un solo número que resume 105 variables de tipos, crédito, apalancamiento y volatilidad. Positivo significa condiciones más restrictivas que la media histórica; negativo, más laxas. Es la mejor respuesta a la pregunta "¿el dinero está ayudando o estorbando?", porque la Fed no solo actúa con los tipos.

## Qué mide
Índice ponderado de 105 indicadores de los mercados monetarios, de deuda, de acciones y del sistema bancario, normalizado a media 0 y desviación típica 1 desde 1971. Tiene tres subíndices: riesgo (volatilidad y primas), crédito (condiciones de préstamo) y apalancamiento (deuda sobre activos). La versión ajustada (ANFCI) descuenta el ciclo económico para aislar lo puramente financiero.

## Cómo se lee
| NFCI | Lectura |
| --- | --- |
| < −0,7 | Muy laxo; burbujas de liquidez (2006, 2021) |
| −0,7 a −0,3 | Laxo; típico de expansión madura |
| −0,3 a 0 | Neutral tirando a restrictivo |
| 0 a +1 | Restrictivo; el crédito se encarece y escasea (2022, finales) |
| > +1 | Estrés (nov-2008: +3,1; mar-2020: +1,0 en un mes) |

Más útil que el nivel es el **cambio en cuatro semanas**: +0,3 es un endurecimiento significativo; +0,5 ha coincidido con correcciones bursátiles.

## Qué lo mueve
Tipos reales, spreads de crédito, VIX, dólar, bolsa (una bolsa que sube relaja las condiciones, lo que hace al índice algo circular), condiciones de préstamo bancario (encuesta SLOOS), y el crecimiento del crédito.

## Qué mueve
Es un resumen, así que "mueve" lo que mueven sus componentes. Su valor es de confirmación: una Fed que sube tipos con NFCI negativo no está consiguiendo endurecer (2023: las subidas se vieron compensadas por la bolsa y los spreads); eso suele llevar a más subidas.

## Umbrales en el motor
Peso 3 en liquidez, junto al tipo real: son las dos variables que resumen el bloque. Alerta en 0 porque es el punto donde las condiciones pasan a ser más restrictivas que la media de 50 años. Umbral bajo en −0,5 para marcar laxitud.

## Casuísticas relacionadas
→ [[fed-sube-y-el-nfci-no-se-mueve]]: la bolsa y los spreads neutralizan a la Fed; suele acabar en subidas adicionales o en tipos altos más tiempo.
→ [[nfci-sube-rapido]]: +0,5 en un mes; la fase de daño ya ha empezado.

## Trampas de lectura
- Incluye la bolsa entre sus componentes, por lo que no es independiente del activo que intentas predecir.
- El dato es de la semana anterior; en una crisis rápida llega tarde (mar-2020 saltó cuando la bolsa ya había caído un 25 %).
- Con tipos reales altos y bolsa en máximos (octubre 2026: −0,55), el índice puede decir "laxo" mientras el coste de capital real es alto: mirar los dos.

## Episodios
- **2007-2008**: el NFCI pasó de −0,8 (junio de 2007) a +0,6 (diciembre) mientras la bolsa aún hacía máximos en octubre, y a +3,1 a finales de noviembre de 2008 (máximo de la serie); fue uno de los indicadores más adelantados de la crisis.
- **Octubre 2022**: en torno a −0,1, máximo del ciclo de subidas sin llegar a positivo; a partir de ahí relajó aunque la Fed siguió subiendo, y la bolsa hizo suelo ese mes.
- **Octubre 2026**: −0,55, percentil 34: condiciones laxas pese al tipo real al 2,95 %; la bolsa y los spreads bajos lo explican. Es una de las contradicciones del cuadro.

## Para profundizar
- Serie y subíndices: https://fred.stlouisfed.org/series/NFCI
- Fed de Chicago, metodología y lista de los 105 componentes: https://www.chicagofed.org/research/data/nfci/about
- Encuesta SLOOS (condiciones de préstamo bancario, trimestral): https://www.federalreserve.gov/data/sloos.htm
