---
tipo: indicador
id: MORTGAGE30US
nombre: Tipo hipotecario a 30 años (EE.UU.)
bloque: Vivienda
fuente: Freddie Mac, Primary Mortgage Market Survey, vía FRED (MORTGAGE30US)
frecuencia: semanal
publicacion: jueves a las 12:00 ET
en_el_motor: peso 1 (invertido) en liquidez (> 7,0 / < 5,5); factor "hipoteca" (> 7,0; carga −1 en discrecional e inmobiliario, −0,5 en materiales)
relacionados: [DGS10, PERMIT, HOUST, vivienda-y-ciclo, efecto-riqueza, asequibilidad]
actualizado: 2026-10-08
---

# Tipo hipotecario a 30 años

El coste de financiar una casa en EE.UU., que es el precio que más decide el ciclo de la vivienda, y la vivienda es el sector que históricamente entra y sale primero de las recesiones ("housing is the business cycle", Leamer 2007).

## Qué mide
Tipo medio ofrecido por los prestamistas para hipotecas a tipo fijo a 30 años conformes (garantizables por Freddie Mac y Fannie Mae). Encuesta semanal. Es aproximadamente el Treasury a 10 años más un diferencial que ha oscilado entre 150 y 300 pb: 150-170 en condiciones normales, más de 250 cuando los compradores de MBS (la Fed, los bancos) se retiran.

## Cómo se lee
| Tipo | Lectura (con precios de 2024-2026) |
| --- | --- |
| < 5 % | Asequible; demanda y construcción fuertes |
| 5-6 % | Neutral |
| 6-7 % | Caro; ventas de segunda mano en mínimos de 30 años (2023-2024) |
| > 7 % | Muy caro; la cuota media supera el 40 % de la renta mediana; construcción se frena (2023 Q4, 2026) |

Hay que leerlo con el precio de la vivienda: la variable real es la **cuota sobre renta** (asequibilidad). Y con el "efecto cerrojo": con el stock de hipotecas al 3-4 % de 2020-2021, los propietarios no venden porque perderían su tipo; la oferta de segunda mano es anormalmente baja y sostiene precios aunque las ventas caigan.

## Qué lo mueve
El 10 años (en un 80 %), el diferencial hipotecario (que depende de la volatilidad de tipos y de la demanda de MBS), y la política de la Fed sobre su cartera de MBS.

## Qué mueve
- Ventas de viviendas (segunda mano responde en 1-2 meses; nueva, en 3-6) y a través de ellas, permisos e inicios de construcción.
- Constructoras (DHI, LEN), mejora del hogar (HD, LOW), muebles y electrodomésticos, materiales de construcción: el bloque "vivienda" de la bolsa, que ha sido históricamente el mejor indicador adelantado del S&P 500 a 12 meses.
- Consumo vía efecto riqueza y refinanciaciones: con tipos altos no hay refinanciación y el consumidor no extrae liquidez de la casa.

## Umbrales en el motor
7,0 % como umbral de "muy caro": es el nivel que en 2023 llevó las ventas de segunda mano a mínimos desde 1995. Factor "hipoteca" con carga −1 en consumo discrecional (mejora del hogar, muebles, coches financiados) e inmobiliario; −0,5 en materiales (construcción).

## Casuísticas relacionadas
→ [[hipoteca-cara-con-precios-altos]]: asequibilidad en mínimos; la salida es por precio (caída) o por tipo (recortes), y la bolsa de constructoras anticipa cuál.
→ [[diferencial-hipotecario-anormal]]: cuando la hipoteca sube más que el 10 años, hay estrés en MBS; 2022-2023.

## Trampas de lectura
- El dato de Freddie Mac es de hipotecas conformes a tipo fijo; las jumbo y las variables tienen otra dinámica.
- El efecto en la economía depende del stock: en 2023 el tipo medio pagado por los propietarios era del 3,7 % mientras el nuevo era del 7 %; el daño se concentró en quien compraba, no en quien ya tenía.
- En Europa el equivalente es el euríbor + diferencial, con hipotecas variables mayoritarias en España e Italia: el canal es más rápido y más potente.

## Episodios
- **2006**: 6,8 % con precios en máximos; la construcción empezó a caer en el verano de 2006, dieciocho meses antes que la bolsa. Las constructoras cayeron un 50 % en 2006-2007 antes de la crisis general.
- **2020-2021**: mínimo histórico 2,65 % (enero 2021); boom de precios del 40 % en dos años.
- **Octubre 2023**: 7,8 %, máximo desde 2000; ventas de segunda mano en 3,8 millones anualizadas, mínimo desde 1995.
- **Octubre 2026**: 7,28 %, percentil 98, +62 pb en el mes; permisos e inicios cayendo.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/MORTGAGE30US
- Freddie Mac PMMS (dato y comentario semanal): https://www.freddiemac.com/pmms
- Leamer, "Housing IS the Business Cycle" (Jackson Hole 2007, PDF en la Fed de Kansas City): https://www.kansascityfed.org/ (buscar el título)
- NAR, ventas de segunda mano e índice de asequibilidad: https://www.nar.realtor/research-and-statistics
