---
tipo: indicador
id: RSAFS
nombre: Ventas minoristas y de restauración
bloque: Actividad
fuente: Oficina del Censo vía FRED (RSAFS, desestacionalizada, nominal)
frecuencia: mensual
publicacion: hacia el día 15 del mes siguiente, 8:30 ET
en_el_motor: variación mensual %; peso 2 en crecimiento (> 0,4 / < −0,2, tendencia ±0,3); headline
relacionados: [GDPC1, UMCSENT, CES0500000003, PCE, grupo-de-control, consumo-fuerte-con-confianza-baja]
actualizado: 2026-10-08
---

# Ventas minoristas

Cuánto gastan los hogares en tiendas, concesionarios, gasolineras, comercio electrónico y restaurantes. Es la primera lectura mensual del consumo, que es dos tercios del PIB, y por eso mueve el GDPNow el día que sale.

## Qué mide
Ventas nominales (sin descontar inflación) de los minoristas y restaurantes de EE.UU., según encuesta a unos 5.000 establecimientos. Incluye coches (20 % del total, muy volátil), gasolina (8 %, que sube con el precio sin que suba el volumen) y materiales de construcción. No incluye servicios salvo restauración.

## Cómo se lee
- **Mensual total**: el titular; con error estándar de ±0,5 pp, un mes no dice nada.
- **Grupo de control** (sin coches, gasolina, materiales de construcción ni restauración): el que entra en el cálculo del PIB y el que mira el mercado. Es la cifra que buscar en la publicación.
- **Real**: deflactando por el IPC de bienes; con inflación al 3,7 % un crecimiento nominal del 3 % anual es una caída real.
- **Variación interanual**: > 4 % nominal fuerte; 2-4 % normal; < 2 % débil con inflación al 2-3 %.

## Qué lo mueve
Renta real disponible (empleo, salarios, inflación), riqueza (bolsa, vivienda), crédito al consumo y su coste (tarjetas al 22 %), ahorro acumulado (el exceso de la pandemia se agotó en 2024), confianza, y el precio de la gasolina (que sube las ventas nominales sin que suba el gasto real en otras cosas).

## Qué mueve
- GDPNow, el mismo día.
- Sectores de consumo: discrecional (coches, muebles, electrónica), restauración, comercio electrónico; y los bellwethers Walmart, Amazon, Home Depot, que publican sus propias cifras y a menudo discrepan del dato oficial.
- Expectativas de Fed si sorprende mucho.

## Umbrales en el motor
Peso 2 en crecimiento con umbrales ±0,4 / −0,2 % mensual y zona muerta ±0,3 pp por el ruido. Coincidente, no adelantado.

## Casuísticas relacionadas
→ [[consumo-fuerte-con-confianza-baja]]: ventas +1,1 % con Michigan en percentil 5 (octubre 2026); quién tiene razón y cuánto dura.
→ [[consumo-financiado-con-credito]]: ventas fuertes con ahorro en mínimos y morosidad de tarjetas subiendo; el consumidor de renta baja primero.
→ [[ventas-nominales-suben-por-gasolina]]: el espejismo del precio.

## Trampas de lectura
- Nominal: con inflación alta parece fuerte sin serlo.
- Las revisiones del mes anterior son frecuentes y grandes.
- La estacionalidad de las rebajas (Black Friday, Prime Day) se ajusta mal cuando las fechas cambian.
- El dato de coches depende de los incentivos y de la disponibilidad; en 2021-2022 los coches distorsionaron todo.

## Episodios
- **Abril 2020**: −14,7 % mensual, récord; mayo: +18 %.
- **Enero 2023**: +3,0 % mensual tras un diciembre débil; el mercado pasó de "recesión inminente" a "no landing" en un dato.
- **Octubre 2026**: +1,13 % mensual (dato de agosto), +1,59 pp, percentil 83; el consumo nominal aguanta con confianza en mínimos y salarios reales negativos.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/RSAFS
- Censo, publicación mensual con el grupo de control y el detalle por tipo de tienda: https://www.census.gov/retail/index.html
- Fed de Nueva York, informe trimestral de deuda y crédito de los hogares (morosidad por tipo): https://www.newyorkfed.org/microeconomics/hhdc
