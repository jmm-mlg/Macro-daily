---
tipo: indicador
id: DGS2
nombre: Treasury a 2 años
bloque: Tipos
fuente: Tesoro de EE.UU. vía FRED (DGS2)
frecuencia: diaria
publicacion: cada día hábil, cierre EE.UU.
en_el_motor: solo panel; interviene a través de la curva T10Y2Y
relacionados: [DFF, DGS10, T10Y2Y, expectativas-de-tipos, fed-funds-futures]
actualizado: 2026-10-08
---

# Treasury a 2 años

Es la expectativa del mercado sobre dónde estará el tipo de la Fed en los próximos dos años. Se mueve antes que la Fed, y por eso es el mejor termómetro de si el mercado espera subidas o recortes.

## Qué mide
Rendimiento del bono del Tesoro a 2 años. Su valor es aproximadamente la media de los tipos a corto esperados en ese plazo más una prima pequeña. Por eso se lee como "lo que el mercado cree que hará la Fed".

## Cómo se lee
- **2 años frente al tipo de la Fed (DFF)**: por encima, el mercado espera subidas; por debajo, recortes. La distancia en puntos básicos dividida por 25 aproxima el número de movimientos descontados. Con DFF al 3,88 % y DGS2 al 4,83 % (octubre 2026), el mercado descuenta casi cuatro subidas de 25 pb en dos años.
- **Variación tras un dato**: si el 2 años sube 10 pb o más tras un IPC o unas nóminas, el dato ha cambiado la expectativa de política monetaria; si no se mueve, el dato estaba descontado.
- **Variación mensual**: +40 pb en un mes es un cambio de régimen de expectativas (ocurrió en jun-2022, feb-2023, sep-2026).

## Qué lo mueve
Datos de inflación y empleo, discursos de miembros de la Fed con voto, el dot plot trimestral, y en menor medida la oferta de letras del Tesoro. Es el tramo de la curva que más reacciona a datos.

## Qué mueve
- La pendiente de la curva (T10Y2Y): si sube más que el 10 años, la curva se aplana o invierte.
- El dólar a corto plazo, vía diferencial de tipos a 2 años con el euro y el yen.
- Los valores más sensibles al ciclo de política: bancos regionales, pequeñas compañías con deuda a tipo variable, inmobiliario.

## Umbrales en el motor
No tiene umbral propio: su información entra por la curva (T10Y2Y) y por los futuros de fondos federales que miras en CME FedWatch. Se muestra en el panel para poder comparar con DFF y leer cuántos movimientos descuenta el mercado.

## Casuísticas relacionadas
→ [[mercado-descuenta-mas-subidas-que-la-fed]]: 2 años muy por encima del tipo oficial; el riesgo es que la Fed decepcione a los halcones o confirme a las palomas.
→ [[curva-se-desinvierte]]: por caída del 2 años (bull steepening, recesión cerca) o por subida del 10 (bear steepening, prima de plazo).

## Trampas de lectura
- El 2 años puede subir porque la Fed vaya a subir o porque el mercado deje de esperar recortes; el efecto en bolsa es parecido, el relato no.
- En semanas de subasta de 2 años, movimientos de 5 pb sin noticia son normales.
- No confundir el 2 años con los futuros de fondos federales: los futuros dan la senda mes a mes; el 2 años, la media.

## Episodios
- **Marzo 2023 (SVB)**: cae 100 pb en tres días (de 5,05 % a 3,95 %), la mayor caída desde 1987, cuando el mercado pasó de esperar subidas a esperar recortes de emergencia. La Fed subió igualmente 25 pb; el 2 años recuperó la mitad en un mes.
- **Junio 2022**: +60 pb en dos semanas tras un IPC del 8,6 %; la Fed subió 75 pb por primera vez desde 1994. El 2 años lo anticipó tres días antes del comunicado.
- **Octubre 2026**: 4,83 %, +44 pb en el mes, 95 pb por encima del tipo oficial: el mercado descuenta un ciclo de subidas que la Fed aún no ha confirmado.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/DGS2
- CME FedWatch (probabilidades implícitas por reunión): https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
