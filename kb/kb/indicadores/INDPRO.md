---
tipo: indicador
id: INDPRO
nombre: Producción industrial
bloque: Actividad
fuente: Reserva Federal (informe G.17) vía FRED (INDPRO)
frecuencia: mensual
publicacion: hacia el día 15-17 del mes siguiente, 9:15 ET
en_el_motor: variación interanual; peso 1 en crecimiento (> 1,5 / < 0, tendencia ±0,2); en el calendario
relacionados: [DGORDER, HG=F, ISM-manufacturero, utilizacion-de-capacidad, ciclo-manufacturero]
actualizado: 2026-10-08
---

# Producción industrial

Cuánto produce la industria (manufacturas, minería, energía) de EE.UU. Es el 15 % del PIB pero el sector más cíclico: la producción industrial ha sido negativa en términos interanuales en todas las recesiones desde 1920, y es la serie que el NBER mira junto al empleo para fechar los ciclos.

## Qué mide
Índice de volumen físico de producción (base 2017 = 100) de manufacturas (75 %), minería incluida extracción de petróleo y gas (15 %) y utilities (10 %). Se publica con la utilización de la capacidad instalada (porcentaje de la capacidad en uso), que es el componente de inflación: por encima del 80 % hay cuellos de botella.

## Cómo se lee
- **Interanual**: > 3 % expansión manufacturera fuerte; 0-3 % normal; < 0 contracción. En las dos últimas décadas ha oscilado entre −15 % (2009) y +8 % (2021).
- **Manufacturas sin coches**: el núcleo; los coches distorsionan por paradas de producción.
- **Utilización de la capacidad**: > 80 % inflacionista; < 75 % holgura (2020: 64 %).
- **Frente al ISM manufacturero** (PMI, encuesta de directores de compras, que sale el primer día hábil del mes): el ISM adelanta 1-2 meses; un ISM por debajo de 50 durante tres meses anticipa producción industrial negativa.

## Qué lo mueve
Demanda de bienes (consumo duradero, inversión en equipo, exportaciones), inventarios (el ciclo de inventarios es el ciclo industrial), dólar (exportaciones), precios de la energía (la minería sube con el petróleo), y en 2024-2026 el capex en centros de datos y la relocalización de semiconductores.

## Qué mueve
- Beneficios de industriales, materiales y energía.
- Empleo manufacturero (12 millones de empleos).
- Cobre, petróleo y fletes, con retardo corto.

## Umbrales en el motor
Peso 1: coincidente y revisado; el adelantado (ISM) no está en FRED de forma gratuita. Umbrales 1,5 / 0 %: el cero es el que históricamente separa expansión de recesión industrial.

## Casuísticas relacionadas
→ [[recesion-industrial-sin-recesion-general]]: 2015-2016 y 2023; cuando servicios compensan.
→ [[cobre-sube-con-produccion-plana]]: octubre 2026; oferta frente a demanda.
→ [[utilizacion-sobre-80]]: cuellos de botella; presión de precios de bienes.

## Trampas de lectura
- Revisiones grandes: el dato de un mes puede cambiar de signo en la revisión.
- Utilities dependen del clima (un verano caluroso sube la producción eléctrica sin que mejore la economía).
- Las huelgas (Boeing 2024, automoción 2023) restan décimas que se recuperan después.

## Episodios
- **2015-2016**: −2 % interanual durante un año por el colapso del petróleo (minería) y el dólar fuerte, sin recesión general: la primera "recesión industrial" sin recesión. El S&P 500 cayó un 13 % y recuperó.
- **2023**: plana o ligeramente negativa todo el año mientras servicios crecían al 3 %; la bolsa subió un 24 %. Industriales y materiales se quedaron atrás.
- **Octubre 2026**: +1,42 % (dato de agosto), +0,29, percentil 66; recuperando con el cobre en máximos.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/INDPRO y utilización de la capacidad: https://fred.stlouisfed.org/series/TCU
- Fed, informe G.17 completo (detalle por industria): https://www.federalreserve.gov/releases/g17/
- ISM, informe manufacturero (resumen gratuito mensual): https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/
