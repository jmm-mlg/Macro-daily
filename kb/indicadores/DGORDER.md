---
tipo: indicador
id: DGORDER (en el motor desde 2026-10-08: NEWORDER, core capex orders)
nombre: Pedidos de bienes duraderos
bloque: Actividad
fuente: Oficina del Censo vía FRED (DGORDER, nominal, desestacionalizado)
frecuencia: mensual
publicacion: hacia el día 25 del mes siguiente, 8:30 ET (adelantado); completo una semana después
en_el_motor: variación mensual %; peso 2 en crecimiento (> 0,5 / < −0,5, tendencia ±0,5); en el calendario
relacionados: [INDPRO, HG=F, capex, pedidos-de-bienes-de-capital, cobre-sube-con-pedidos-cayendo]
actualizado: 2026-10-08
---

# Pedidos de bienes duraderos

Cuánto han encargado las empresas y los hogares de bienes que duran más de tres años: aviones, maquinaria, ordenadores, coches, electrodomésticos. Es el dato adelantado de inversión empresarial, porque un pedido hoy es producción dentro de meses.

## Qué mide
Nuevos pedidos recibidos por fabricantes de bienes duraderos, en dólares nominales, según encuesta a unos 5.000 fabricantes. Muy volátil por aviones (Boeing puede sumar o restar 10 puntos en un mes) y defensa. Por eso el mercado mira una partida concreta: **pedidos de bienes de capital no militares excluyendo aviones** ("core capex orders"), que es la medida de inversión empresarial en equipo.

## Cómo se lee
- **Total mensual**: titular, pero inservible sin desagregar; puede variar ±5 % por un pedido de aviones.
- **Core capex orders** (variación mensual y a 3 meses anualizada): > 0,5 % mensual sostenido es inversión expandiéndose; negativo tres meses seguidos, contracción. Es el dato que entra en la estimación de inversión del PIB.
- **Envíos** (shipments) de bienes de capital: lo que ya se ha entregado; entra directamente en el PIB del trimestre.
- **Pedidos pendientes** (backlog): sube cuando los fabricantes no dan abasto (2021-2022).

## Qué lo mueve
Beneficios y flujo de caja de las empresas (el capex sigue a los beneficios con 2-3 trimestres de retardo), coste de capital (tipos y spreads), utilización de la capacidad (por encima del 80 % obliga a invertir), expectativas (ISM nuevos pedidos adelanta 1-2 meses), incentivos fiscales (amortización acelerada), y en 2024-2026 la inversión en centros de datos e infraestructura eléctrica.

## Qué mueve
- Producción industrial, con 1-3 meses de retardo.
- Beneficios de bienes de equipo (Caterpillar, Deere, Eaton, Siemens) y semiconductores de equipo (ASML, Applied Materials); sus pedidos propios son versiones sectoriales de este dato.
- Cobre y acero.

## Umbrales en el motor
Peso 2 en crecimiento, por ser adelantado; umbrales ±0,5 % con zona muerta ±0,5 pp por la volatilidad. **Desde el 8 de octubre de 2026 el motor usa la serie core (NEWORDER: bienes de capital no militares sin aviones) en lugar del total**, porque el total lo distorsionan los pedidos de aviones. Esta entrada cubre ambas.

## Casuísticas relacionadas
→ [[cobre-sube-con-pedidos-cayendo]]: octubre 2026; quién tiene razón sobre el ciclo industrial.
→ [[capex-cae-con-beneficios-en-maximos]]: señal de que las empresas no creen en la demanda; precede a despidos.
→ [[pedidos-de-aviones-distorsionan]]: cómo leer un titular de +10 % o −10 %.

## Trampas de lectura
- Nominal: en 2021-2022 subía por precios.
- Boeing y defensa; mirar siempre la serie core.
- Revisiones: el dato adelantado se revisa una semana después con el informe completo, a veces cambiando de signo.
- Los pedidos pueden cancelarse; en 2020 el backlog de aviones se evaporó.

## Episodios
- **2015-2016**: core capex orders cayendo un 5 % interanual durante dieciocho meses por el petróleo (los productores recortaron inversión un 40 %); sin recesión general.
- **2021**: +20 % interanual, el mayor ciclo de capex desde los años 90, por la reposición post-pandemia y la escasez de suministros.
- **Octubre 2026**: −0,07 % mensual (dato de agosto), −0,94 pp, percentil 39; plano mientras el cobre marca máximos.

## Para profundizar
- Serie total: https://fred.stlouisfed.org/series/DGORDER y core capex orders: https://fred.stlouisfed.org/series/NEWORDER
- Censo, publicación mensual (M3) con el detalle por industria: https://www.census.gov/manufacturing/m3/index.html
