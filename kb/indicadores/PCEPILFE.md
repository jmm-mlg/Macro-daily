---
tipo: indicador
id: PCEPILFE
nombre: Deflactor del consumo personal subyacente (PCE core)
bloque: Inflación
fuente: BEA (Bureau of Economic Analysis) vía FRED (PCEPILFE)
frecuencia: mensual
publicacion: último viernes del mes siguiente, 8:30 ET, con la renta y el gasto personal
en_el_motor: variación interanual; peso 3 en inflación (> 2,8 / < 2,0); headline
relacionados: [CPILFESL, CPIAUCSL, DFF, objetivo-del-2-por-ciento, fomc]
actualizado: 2026-10-08
---

# PCE subyacente

La medida de inflación sobre la que la Fed define su objetivo del 2 %. Sale tres semanas después del IPC y rara vez sorprende, porque el IPC y el IPP ya permiten estimarlo con precisión; pero es el número que aparece en las proyecciones del FOMC y el que decide los tipos.

## Qué mide
Índice de precios del gasto en consumo personal excluyendo alimentos y energía, calculado por la BEA a partir de las cuentas nacionales. Difiere del IPC en tres cosas: la cesta cambia con lo que la gente compra (fórmula encadenada, que captura la sustitución y por eso crece menos), incluye gasto pagado por terceros (seguros médicos, Medicare), y pesa menos la vivienda (15 % frente a 45 % en el IPC subyacente) y más la salud (20 %).

## Cómo se lee
- **Interanual**: el objetivo es 2,0 %. Las proyecciones del FOMC dan la senda que espera la Fed; si el dato va por encima de la proyección de diciembre, la Fed endurece.
- **Diferencia con el IPC subyacente**: históricamente el PCE es 0,3-0,5 pp más bajo. Cuando la diferencia se estrecha (2023-2024), es porque la vivienda se enfría y la salud se calienta.
- **Mensual anualizado a 3 y 6 meses**: lo que cita Powell en las ruedas de prensa.

## Qué lo mueve
Lo mismo que el IPC subyacente, más dos componentes propios: servicios financieros imputados (comisiones de gestión, que suben con la bolsa: el PCE tiene un componente que sube cuando sube el S&P 500) y precios de la sanidad (ligados a Medicare, administrativos).

## Qué mueve
Las proyecciones y decisiones del FOMC, y a través de ellas todo lo demás. El mercado lo mueve poco el día del dato porque está anticipado; lo que sorprende son las revisiones de meses anteriores.

## Umbrales en el motor
Peso 3, igual que el IPC subyacente, para que el score de inflación descanse en las dos medidas de tendencia y no en el general. Umbral alto en 2,8 % (algo menor que el 3,0 % del IPC por la diferencia estructural); bajo en 2,0 %, el objetivo.

## Casuísticas relacionadas
→ [[pce-por-encima-de-la-proyeccion-del-fomc]]: la Fed revisa al alza en la siguiente reunión con proyecciones.
→ [[ipc-y-pce-divergen]]: composición (vivienda frente a salud); cuál manda.

## Trampas de lectura
- Las revisiones de meses anteriores son frecuentes y a veces cambian la tendencia; el dato nuevo puede ser bueno y el conjunto malo.
- El componente de servicios financieros hace que el PCE suba en mercados alcistas aunque la inflación real no cambie.
- Sale con el gasto personal, que es el dato de actividad del mes; el mercado a veces reacciona al gasto y no al precio.

## Episodios
- **Febrero 2022**: 5,4 %, máximo desde 1983; en marzo la Fed inició las subidas con un retraso que ella misma reconoció.
- **Diciembre 2023**: 2,9 %, primera lectura por debajo del 3 % desde 2021; el FOMC de ese mes anunció tres recortes para 2024 y la bolsa subió un 14 % en dos meses.
- **Octubre 2026**: 3,01 %, +0,02 pp, percentil 61. Por encima del umbral de 2,8 y de la última proyección de la Fed.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/PCEPILFE
- BEA, publicación mensual de renta y gasto personal: https://www.bea.gov/data/income-saving/personal-income
- Proyecciones económicas del FOMC (SEP), con la senda de PCE subyacente: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
