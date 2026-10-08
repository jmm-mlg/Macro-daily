---
tipo: mecanismo
id: politica-monetaria-retardos
nombre: Decisión de la Fed → economía real: los retardos
cadena: "Subida de tipos → condiciones financieras (días) → vivienda y crédito (3-6 meses) → inversión y empleo (6-12 meses) → inflación (12-24 meses)"
plazo: "de días a dos años según el eslabón"
series: [DFF, DGS2, NFCI, MORTGAGE30US, ICSA, CPILFESL]
sectores: [financiero, inmobiliario, discrecional, utilities]
casuisticas: [pausa-de-la-fed, primer-recorte-del-ciclo, fed-sube-y-el-nfci-no-se-mueve]
actualizado: 2026-10-08
---

# Decisión de la Fed → economía real: los retardos

Friedman lo llamó "retardos largos y variables": una subida de tipos tarda meses en frenar la economía y hasta dos años en bajar la inflación. Eso tiene dos consecuencias para invertir: la Fed casi siempre llega tarde (sube cuando la inflación ya está y recorta cuando el paro ya sube), y el mercado opera con lo que la Fed hará, no con lo que hace. El 2 años y los futuros de fondos federales son la Fed del mercado.

## Cadena y retardos
| Eslabón | Retardo | Serie |
| --- | --- | --- |
| Mercados financieros (tipos, bolsa, dólar, spreads) | Minutos a días | DGS2, NFCI |
| Hipotecas y vivienda | 1-3 meses a tipos; 3-6 a ventas y permisos | MORTGAGE30US, PERMIT |
| Crédito bancario (condiciones y volumen) | 2-4 trimestres | SLOOS (externa), BAMLH0A0HYM2 |
| Inversión empresarial | 2-4 trimestres | NEWORDER |
| Empleo | 3-6 trimestres | ICSA, PAYEMS |
| Inflación subyacente | 4-8 trimestres | CPILFESL, PCEPILFE |

## Cómo lo usa el mercado
- La bolsa descuenta la senda de tipos a 1-2 años: lo que importa en cada FOMC no es la decisión (conocida) sino el cambio en la senda (dot plot, tono).
- **Entre la última subida y el primer recorte** ("la pausa") la bolsa ha subido en todos los ciclos desde 1989 salvo en 2000-2001 y 2007: es el mejor periodo porque la restricción deja de crecer y los beneficios aún no han caído.
- **El primer recorte** es suelo si llega sin recesión (1995, 1998, 2019, 2024) y techo si llega con la recesión ya en marcha (2001, 2007). La diferencia la marca el empleo en el momento del recorte.

## Evidencia
- Romer y Romer (2004): un shock de política monetaria de 100 pb reduce la producción industrial un 4 % con un retardo máximo de 2 años.
- Fed, modelo FRB/US: el pico de efecto sobre el PIB de una subida está a 4-6 trimestres.

## Cuándo falla
- Cuando los hogares y empresas han refinanciado a largo (2020-2021): la transmisión por el crédito es más lenta; el "retardo" se alarga (2022-2024).
- Cuando la política fiscal empuja en sentido contrario (déficit del 6-7 % del PIB con la Fed subiendo, 2023).
- Cuando las condiciones financieras no se endurecen (bolsa y spreads compensan): la Fed sube más de lo previsto.

## Qué hacer con ello
- Operar la senda, no la decisión: CME FedWatch y el 2 años dicen qué está descontado; el dato que mueve el mercado es el que cambia la senda.
- En la pausa, exposición alta en sectores de calidad; en el primer recorte, mirar las peticiones: si están bajas, suelo (comprar cíclicos); si suben, techo (defensivos).
- Los efectos de las subidas de 2026 sobre el empleo llegarán en 2027; el cuadro de hoy es el de las decisiones de hace un año.
