---
tipo: indicador
id: PERMIT
nombre: Permisos de construcción de viviendas
bloque: Vivienda
fuente: Oficina del Censo y HUD vía FRED (PERMIT, miles anualizadas)
frecuencia: mensual
publicacion: hacia el día 17-19 del mes siguiente, 8:30 ET, con las viviendas iniciadas
en_el_motor: nivel; peso 1 en crecimiento (percentil ≥ 70 / ≤ 30, tendencia ±30); en el calendario
relacionados: [HOUST, MORTGAGE30US, DGS10, vivienda-y-ciclo, constructoras, leading-indicators]
actualizado: 2026-10-08
---

# Permisos de construcción

Cuántas viviendas nuevas han sido autorizadas ese mes. Es el primer eslabón de la cadena de la vivienda (permiso → inicio → construcción → venta) y uno de los diez componentes del índice de indicadores adelantados del Conference Board: adelanta al ciclo general en 6-12 meses.

## Qué mide
Permisos de construcción residencial concedidos por los ayuntamientos, en miles de unidades anualizadas, desestacionalizados. Se desglosa en unifamiliares (la señal limpia, ligada a la demanda de los hogares) y multifamiliares (edificios de alquiler, ligados a la financiación y muy volátiles).

## Cómo se lee
| Nivel (miles anualizadas) | Lectura (para la población actual) |
| --- | --- |
| > 1.700 | Expansión fuerte; riesgo de exceso de oferta (2021-2022: 1.900) |
| 1.400-1.700 | Normal; cubre la formación de hogares (estimada en 1,2-1,5 millones al año) |
| 1.100-1.400 | Débil; déficit de oferta acumulándose |
| < 1.000 | Recesión inmobiliaria (2009-2011: 500-600) |

Lo que importa es la tendencia de unifamiliares: tres meses de caída es giro. Y la relación con las hipotecas: los permisos reaccionan a los tipos hipotecarios con 2-4 meses de retardo.

## Qué lo mueve
Tipo hipotecario (el principal), precios de la vivienda (margen del constructor), coste de materiales y mano de obra, suelo disponible y regulación, y la confianza de los constructores (índice NAHB, que sale dos días antes y adelanta).

## Qué mueve
- Viviendas iniciadas (1-2 meses después) y construcción (6-12 meses de actividad y empleo por vivienda).
- Materiales (madera, cemento, cobre), electrodomésticos, muebles, mejora del hogar.
- Constructoras cotizadas (D.R. Horton, Lennar, Pulte), que a su vez adelantan al dato: suelen hacer suelo o techo 3-6 meses antes.
- Oferta futura de vivienda y, por tanto, precios y alquileres a 1-2 años, que entran en el IPC.

## Umbrales en el motor
Peso 1 por percentil. Es adelantado pero el motor ya tiene las hipotecas (más adelantadas aún) en liquidez; aquí mide si la demanda responde.

## Casuísticas relacionadas
→ [[hipoteca-cara-con-precios-altos]]: permisos cayendo con precios estables; el ajuste viene por cantidad, no por precio.
→ [[permisos-caen-tres-meses]]: señal de giro del ciclo con 6-12 meses de adelanto.
→ [[multifamiliar-se-desploma]]: 2023-2024; exceso de oferta de alquiler y su efecto en el IPC de vivienda.

## Trampas de lectura
- Multifamiliares pueden mover el total ±10 % en un mes por un proyecto grande; mirar unifamiliares.
- El clima afecta a los inicios más que a los permisos.
- Revisiones moderadas; el dato preliminar es fiable.

## Episodios
- **Septiembre 2005**: pico de 2,2 millones; el mínimo llegó en marzo de 2009 (513.000). Los permisos cayeron durante dos años antes de que la bolsa hiciera máximos en octubre de 2007: el aviso más largo de la historia.
- **2022**: de 1,9 millones (enero) a 1,35 (diciembre) con las hipotecas del 3 % al 7 %; las constructoras cayeron un 40 % y luego subieron un 80 % en 2023 cuando el déficit de oferta sostuvo precios.
- **Octubre 2026**: 1,403 millones (dato de agosto), −30.000, percentil 38; cayendo con la hipoteca al 7,3 %.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/PERMIT y unifamiliares: https://fred.stlouisfed.org/series/PERMIT1
- Censo, construcción residencial (permisos, inicios, terminadas): https://www.census.gov/construction/nrc/index.html
- NAHB, índice de confianza de constructores: https://www.nahb.org/news-and-economics/housing-economics/indices/housing-market-index
