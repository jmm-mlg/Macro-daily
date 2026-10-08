---
tipo: indicador
id: CPILFESL
nombre: IPC subyacente de EE.UU.
bloque: Inflación
fuente: BLS vía FRED (CPILFESL)
frecuencia: mensual
publicacion: con el IPC general, 8:30 ET
en_el_motor: variación interanual; peso 3 en inflación (> 3,0 / < 2,0, tendencia ±0,1); headline
relacionados: [CPIAUCSL, PCEPILFE, CES0500000003, supercore, inflacion-persistente]
actualizado: 2026-10-08
---

# IPC subyacente de EE.UU.

El IPC sin energía ni alimentos. Es la medida de la inflación "que se queda", porque elimina los dos componentes más volátiles y más ligados a materias primas. La Fed y el mercado lo miran más que al general.

## Qué mide
Índice de precios al consumo excluyendo alimentos (13 % de la cesta) y energía (7 %). Lo que queda es 80 % de la cesta: vivienda (45 % del subyacente), servicios sin vivienda (30 %: salud, transporte, ocio, seguros) y bienes (25 %: coches, ropa, muebles). Dentro, el mercado distingue tres bloques con dinámica distinta: bienes (deflacionarios desde 2023 por la normalización de suministros), vivienda (retardada) y servicios sin vivienda ("supercore", ligado a salarios).

## Cómo se lee
| Interanual | Lectura |
| --- | --- |
| > 4 % | La Fed sube agresivamente (2022-2023) |
| 3-4 % | Persistente; la Fed en pausa o subiendo despacio |
| 2,5-3 % | Tolerable; recortes lentos |
| 2-2,5 % | Objetivo a la vista; recortes |
| < 2 % | Riesgo de desinflación excesiva; recortes rápidos |

Mensual: la Fed necesita una racha de 0,2 % o menos (anualiza al 2,4 %) para recortar con confianza. 0,3 % es ambiguo; 0,4 % es señal de alarma.

## Qué lo mueve
Alquileres (con un año de retardo respecto a Zillow y Apartment List), salarios en servicios, precios de coches usados (muy volátiles, índice Manheim los anticipa), seguros (de coche y de salud, que subieron un 20 % en 2023-2024), dólar en bienes.

## Qué mueve
La política de la Fed más que ningún otro dato salvo el PCE subyacente. Y por tanto el 2 años, el dólar y los múltiplos. Un subyacente que baja con el general subiendo (por energía) es un escenario favorable para la bolsa porque la Fed mira a través de la energía.

## Umbrales en el motor
Peso 3, el máximo del score, compartido con el PCE subyacente. Umbrales 3,0 (alto) y 2,0 (bajo): el 3 % es el nivel por encima del cual la Fed no ha recortado en los últimos 30 años salvo crisis. Zona muerta de ±0,1 pp en tendencia porque una décima es ruido.

## Casuísticas relacionadas
→ [[subyacente-baja-y-general-sube]]: energía; favorable para bolsa, la Fed mira a través.
→ [[supercore-acelera]]: servicios sin vivienda subiendo = salarios = la inflación más persistente; la Fed se pone dura.
→ [[bienes-deflacionarios-servicios-inflacionarios]]: la composición de 2023-2025; qué sectores ganan margen.

## Trampas de lectura
- El 45 % de vivienda hace que el subyacente llegue tarde a los giros: en 2023 los alquileres de mercado ya caían mientras el OER seguía subiendo al 7 %.
- Un mes aislado no cambia nada; la Fed mira tres y seis meses anualizados.
- La mediana del IPC (Fed de Cleveland) y el IPC recortado (trimmed mean, Fed de Dallas) son medidas alternativas de tendencia que a veces discrepan del subyacente; cuando discrepan, suelen tener razón ellas.

## Episodios
- **Septiembre 2022**: 6,6 %, máximo desde 1982; el dato (13 de octubre) hizo caer el S&P 500 un 2 % en la apertura y subir un 2,6 % al cierre: el famoso "reversal" que marcó el suelo del mercado bajista.
- **2023**: de 5,6 % a 3,9 % con la bolsa subiendo un 24 %; la desinflación fue el motor del año.
- **Primer trimestre 2024**: tres lecturas de 0,4 % m/m retrasaron el primer recorte de marzo a septiembre.
- **Octubre 2026**: 2,76 %, −0,02 pp, percentil 42: el subyacente no acompaña al general; la presión viene de energía e IPP.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/CPILFESL
- Fed de Cleveland, IPC mediano y recortado: https://www.clevelandfed.org/indicators-and-data/median-cpi
- Fed de Dallas, trimmed mean PCE: https://www.dallasfed.org/research/pce
