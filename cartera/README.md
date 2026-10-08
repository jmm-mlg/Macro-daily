# Registro de operaciones

`operaciones.csv`: una fila por operación. Lo rellenas tú al abrir (y al cerrar); el motor lo lee cada mañana y
produce la sección "Cartera" del email y `data/cartera_estado.csv`. Edita el archivo desde GitHub Desktop (y push)
o desde el editor de GitHub.

## Columnas
| Columna | Qué poner | Ejemplo |
| --- | --- | --- |
| id | Número correlativo | 1 |
| fecha_apertura | AAAA-MM-DD | 2026-10-13 |
| ticker | Como en la watchlist (sufijos .MC, .PA, .L…) | XOM, SAN.MC, SHEL.L |
| lado | largo o corto | largo |
| acciones | Número entero | 295 |
| precio_entrada | En moneda local (Londres en libras, no peniques) | 169.05 |
| stop | Precio del stop estructural, moneda local | 161.97 |
| fx_entrada | Dólares por unidad de la moneda local el día de la entrada (1 si es USD; el email lo muestra en el pulso de divisas) | 1.119 |
| regimen | Del email del día | mixto |
| tension | Del email del día | media |
| sesgo_sector | Del email del día | 1 |
| amplitud_revisiones | Del pulso micro | 1.0 |
| disparador | El hecho con fecha que justificó la entrada | "Resultados 30/10 con guía al alza" |
| cierro_si | La frase de cierre | "WTI cae de p70 o HY > 400" |
| fecha_cierre, precio_cierre, motivo_cierre, leccion | Vacíos hasta cerrar. motivo: stop / objetivo / regimen / disparador / discrecional | |
| estado | abierta o cerrada | abierta |

Las columnas con texto libre van entre comillas dobles si contienen comas.

## Lo que calcula el motor para cada posición abierta
Precio actual, resultado en dólares (separado en acción y divisa), resultado en R, distancia al stop,
si el stop ha sido alcanzado, si está a +1R (mover stop a entrada) o +2R (cerrar mitad), días hasta
resultados, y si el sesgo del sector ha pasado a negativo o un disparador en contra se ha activado.
A nivel de cartera: exposición total y por sector y región, riesgo abierto (suma de distancias a stop)
y comprobación de los límites del nivel 6 de la guía.
