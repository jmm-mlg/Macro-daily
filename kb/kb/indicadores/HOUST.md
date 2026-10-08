---
tipo: indicador
id: HOUST
nombre: Viviendas iniciadas
bloque: Vivienda
fuente: Oficina del Censo y HUD vía FRED (HOUST, miles anualizadas)
frecuencia: mensual
publicacion: con los permisos, 8:30 ET
en_el_motor: nivel; solo panel; en el calendario
relacionados: [PERMIT, MORTGAGE30US, inversion-residencial, empleo-en-construccion]
actualizado: 2026-10-08
---

# Viviendas iniciadas

Cuántas viviendas han empezado a construirse (se ha excavado el cimiento). Sigue a los permisos con 1-2 meses y es lo que entra en el PIB como inversión residencial; dice si los permisos se convierten en actividad.

## Qué mide
Inicios de construcción residencial en miles de unidades anualizadas, desestacionalizados; unifamiliares y multifamiliares. Se publica con las viviendas en construcción y las terminadas, que cierran el ciclo.

## Cómo se lee
Los mismos rangos que los permisos (> 1.700 fuerte, < 1.000 recesión). Lo informativo es la **relación con los permisos**: si los inicios caen más que los permisos, los constructores han pedido licencias que no ejecutan (esperan a que bajen los tipos o los costes); si los inicios superan a los permisos, están usando licencias acumuladas y el stock de permisos se agota.

**Viviendas en construcción**: el stock de obra en curso; en 2022-2023 alcanzó un récord (1,7 millones) por los retrasos de materiales, y su entrega en 2024 añadió oferta de alquiler que enfrió los alquileres.

## Qué lo mueve
Permisos (1-2 meses antes), clima (los inicios de invierno son muy sensibles), disponibilidad de mano de obra y materiales, y financiación a los constructores (líneas de crédito de bancos regionales).

## Qué mueve
- Inversión residencial en el PIB (4 % del PIB, pero 20 % de su variación en los ciclos).
- Empleo en construcción (8 millones).
- Demanda de materiales con retardo corto.
- Oferta de vivienda terminada a 9-12 meses, y con ella precios y alquileres.

## Umbrales en el motor
Sin peso: redundante con los permisos y más ruidoso por el clima. Se muestra para la lectura de la cadena.

## Casuísticas relacionadas
→ [[permisos-sin-inicios]]: constructores esperando; suele preceder a recortes de precios de vivienda nueva.
→ [[inicios-multifamiliares-en-maximos]]: 2022; exceso de oferta de alquiler a dos años vista.

## Trampas de lectura
- Volátil: ±10 % mensual es normal; mirar la media de 3 meses.
- Clima: un febrero frío resta 100.000 anualizadas que marzo devuelve.
- Multifamiliares concentran la volatilidad.

## Episodios
- **Enero 2006**: pico de 2,27 millones; abril 2009: 478.000, el mínimo desde que hay datos (1959).
- **2021-2022**: 1,8 millones con viviendas en construcción en récord por los cuellos de botella; las terminadas llegaron en 2023-2024.
- **Octubre 2026**: 1,275 millones (agosto), −34.000, percentil 28; por debajo de los permisos (1,403): los constructores retrasan.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/HOUST y en construcción: https://fred.stlouisfed.org/series/UNDCONTSA
- Censo, construcción residencial: https://www.census.gov/construction/nrc/index.html
