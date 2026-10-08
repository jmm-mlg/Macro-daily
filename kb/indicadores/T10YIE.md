---
tipo: indicador
id: T10YIE
nombre: Breakeven de inflación a 10 años
bloque: Tipos
fuente: FRED (T10YIE), diferencia entre DGS10 y DFII10
frecuencia: diaria
publicacion: cada día hábil, cierre EE.UU.
en_el_motor: peso 1 en el score de inflación (> 2,5 alto, < 2,0 bajo)
relacionados: [DGS10, DFII10, CPIAUCSL, UMCSENT, expectativas-de-inflacion, oro-cae-con-inflacion-alta]
actualizado: 2026-10-08
---

# Breakeven de inflación a 10 años

La inflación media anual que el mercado de bonos espera para los próximos diez años. Es lo que la Fed vigila para saber si las expectativas siguen "ancladas" en el 2 %; si se desanclan, la Fed sube tipos aunque el crecimiento sufra.

## Qué mide
Diferencia entre el rendimiento del Treasury nominal a 10 años y el del TIPS a 10 años. Es la inflación a la que un inversor sería indiferente entre ambos bonos. Incluye una pequeña prima de riesgo de inflación y una prima de liquidez de los TIPS, por lo que no es exactamente la expectativa pura.

## Cómo se lee
| Nivel | Lectura |
| --- | --- |
| < 1,5 % | Expectativas por debajo del objetivo: riesgo deflacionario (2015, mar-2020) |
| 1,8-2,4 % | Ancladas: la Fed tiene margen |
| 2,4-2,8 % | Tensionadas: la Fed vigila; cada dato de IPC pesa el doble |
| > 2,8 % | Desancladas: la Fed sube aunque el empleo sufra (abr-2022: 3,0 %) |

Más informativa que el nivel es la **tendencia tras un dato**: si el IPC sale alto y el breakeven no sube, el mercado cree que es transitorio; si sube, cree que es persistente.

## Qué lo mueve
Datos de inflación publicados, petróleo (con fuerza: el breakeven a 10 años se mueve con el crudo mucho más de lo que la teoría justificaría), credibilidad de la Fed, y flujos hacia TIPS.

## Qué mueve
- La reacción de la Fed: es su variable de credibilidad.
- La descomposición del 10 años: una subida del nominal por breakeven favorece a materias primas, energía y bancos; una subida por tipo real castiga a todo.
- Oro: sigue al tipo real, no al breakeven; pero un breakeven desanclado suele acabar en tipo real alto.

## Umbrales en el motor
Peso 1 en inflación con umbrales 2,5 / 2,0: es un complemento a los datos publicados (IPC, PCE, IPP), que pesan más porque son los que la Fed mira. Su valor añadido está en ser diario cuando los otros son mensuales.

## Casuísticas relacionadas
→ [[ipc-alto-con-breakeven-estable]]: el mercado ve el dato como transitorio; sectores cíclicos aguantan.
→ [[breakeven-sube-con-petroleo]]: inflación importada; la Fed suele mirar a través de ella.
→ [[oro-cae-con-inflacion-alta]].

## Trampas de lectura
- El breakeven a 10 años incluye los próximos dos años; el "5y5y forward" (inflación esperada entre el año 5 y el 10, serie T5YIFR) aísla las expectativas de largo plazo y es el que cita la Fed.
- En pánicos de liquidez (mar-2020) los TIPS se venden más que los nominales y el breakeven se hunde sin que las expectativas hayan cambiado.
- La encuesta de Michigan de expectativas a 5-10 años es la otra medida que mira la Fed; cuando mercado y encuesta divergen, la Fed se fía más de la encuesta.

## Episodios
- **Marzo 2020**: cae a 0,5 % en dos semanas; la Fed anuncia QE ilimitado; vuelve al 2 % en seis meses.
- **Abril 2022**: 3,0 %, máximo desde que existe la serie; la Fed acelera a subidas de 75 pb. Octubre 2022: 2,3 % con el petróleo bajando; es cuando la Fed empieza a hablar de moderar.
- **Octubre 2026**: 2,36 %, estable en el mes a pesar del IPC al 3,7 %: el mercado no ve persistencia. Si rompe el 2,5 %, el score de inflación y el tipo real suben juntos.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/T10YIE y la 5y5y forward: https://fred.stlouisfed.org/series/T5YIFR
- Fed de Cleveland, expectativas de inflación por modelos y encuestas: https://www.clevelandfed.org/indicators-and-data/inflation-expectations
- Encuesta de Michigan (expectativas a 1 y 5 años): https://data.sca.isr.umich.edu/
