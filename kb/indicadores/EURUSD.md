---
tipo: indicador
id: EURUSD=X
nombre: Euro-dólar
bloque: Mercado
fuente: yfinance (EURUSD=X), dólares por euro
frecuencia: diaria (continuo)
publicacion: continuo
en_el_motor: panel; factor "euro" (> ±3 %/mes) sin carga sectorial, para narrativa y lectura europea
relacionados: [DX-Y.NYB, ECBDFR, DFF, DGS2, CP0000EZ19M086NEST, divisas, divergencia-fed-bce]
actualizado: 2026-10-09
---

# Euro-dólar

Cuántos dólares vale un euro. Para una cartera mixta es la divisa que importa: convierte cada posición americana a euros y reparte ganadores y perdedores entre exportadoras europeas y americanas. Su motor principal es el diferencial de tipos entre la Fed y el BCE.

## Cómo se lee
| EUR/USD | Lectura (2015-2026) |
| --- | --- |
| > 1,20 | Euro fuerte; BCE más duro que la Fed o dólar débil (2017-2018, 2021) |
| 1,08-1,20 | Rango normal |
| 1,00-1,08 | Euro débil; divergencia Fed-BCE o crisis europea (2022, 2024 final) |
| < 1,00 | Paridad rota; solo en 2022 (energía, guerra) |

Variación: 3 % en un mes es mucho (octubre 2026: −3,7 %); 10 % en un año es un ciclo. Qué mirar con él: diferencial de tipos a 2 años EE.UU.-Alemania (el mejor predictor a 3-6 meses) y el diferencial de tipos oficiales (DFF − ECBDFR: 138 pb en octubre de 2026).

## Qué lo mueve
Diferencial de tipos y de expectativas (Fed frente a BCE), crecimiento relativo (EE.UU. ha crecido más desde 2010 y el euro ha caído de 1,40 a 1,10), energía (Europa importa en dólares: el gas caro de 2022 hundió el euro), riesgo político europeo (Italia, Francia), y el dólar como refugio.

## Qué mueve
- Beneficios: exportadoras europeas ganan con euro débil (cada −5 % del euro son +2-3 pp de crecimiento de BPA para LVMH o Airbus); multinacionales americanas pierden.
- Inflación europea: euro débil = inflación importada; el BCE lo vigila.
- Tus posiciones: el resultado en euros de una acción americana es el de la acción más el del euro-dólar.
- Bolsa europea frente a americana: el euro débil ha coincidido con mejor comportamiento relativo de Europa (2022-2023 primer semestre).

## Umbrales en el motor
Factor "euro" activo con movimiento mensual superior al 3 %; sin carga sectorial en la matriz (es de EE.UU.), pero entra en la narrativa y en la lectura de resultados de las europeas de la watchlist.

## Casuísticas relacionadas
→ [[divergencia-fed-bce]]: diferencial de tipos que se abre o se cierra.
→ [[dolar-cae-con-tipos-subiendo]]: cuando el euro sube sin que el BCE haga nada (desconfianza en el dólar, 2025).

## Trampas de lectura
- El euro-dólar es el inverso del DXY en un 58 %: un movimiento del BCE lo mueve tanto como uno de la Fed.
- Las empresas europeas cubren a 6-12 meses; el efecto en resultados llega con retardo.
- Un euro débil por energía cara (2022) no favorece a las exportadoras europeas tanto como uno débil por tipos: el coste energético se come el margen.

## Episodios
- **2014-2015**: de 1,39 a 1,05 por la divergencia Fed-BCE (QE del BCE, fin del QE de la Fed); DAX +25 % en 2015.
- **Septiembre 2022**: 0,96, por debajo de la paridad por primera vez en 20 años; gas a 300 €/MWh; la Fed en 75 pb por reunión.
- **2025**: de 1,04 a 1,17 con la Fed sin recortar: el dólar cayó por pérdida de confianza (aranceles); las exportadoras europeas sufrieron.
- **Octubre 2026**: 1,119, −3,7 % en el mes, percentil 47; diferencial Fed-BCE de 138 pb; el 2 años americano subiendo más que el alemán.

## Para profundizar
- BCE, tipo de cambio de referencia y estadísticas: https://data.ecb.europa.eu/
- Diferencial de tipos a 2 años EE.UU.-Alemania: DGS2 en FRED frente al Bund a 2 años en el Data Portal del BCE
