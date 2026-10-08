---
tipo: indicador
id: BAMLC0A0CM
nombre: Spread Investment Grade (ICE BofA US Corporate OAS)
bloque: Crédito
fuente: ICE BofA vía FRED (BAMLC0A0CM)
frecuencia: diaria
publicacion: cada día hábil con un día de retraso
en_el_motor: solo panel; el crédito entra por el HY
relacionados: [BAMLH0A0HYM2, DGS10, ciclo-de-credito, coste-de-capital]
actualizado: 2026-10-08
---

# Spread Investment Grade (OAS)

Lo que pagan las grandes empresas con buena calificación por encima del Tesoro. Es el coste marginal de la deuda para el S&P 500 y el termómetro de si el mercado de bonos corporativos funciona con normalidad.

## Qué mide
Diferencial ajustado por opciones del índice de bonos corporativos de EE.UU. con calificación BBB o superior frente al Tesoro. En puntos porcentuales; 0,84 = 84 pb. Más del 50 % del índice es BBB, el escalón justo por encima del high yield: es ahí donde se concentra el riesgo de "ángeles caídos" (rebajas a HY) en recesión.

## Cómo se lee
| Spread | Lectura |
| --- | --- |
| < 1,0 % (100 pb) | Normal en expansión; mercado primario abierto |
| 1,0-1,5 % | Tensión moderada |
| 1,5-2,5 % | Estrés; las empresas retrasan emisiones (2011, 2016, 2022) |
| > 3 % | Crisis sistémica (2008: 600 pb; mar-2020: 400 pb) |

Se mueve menos que el HY (una cuarta o quinta parte) pero cuando se mueve es más grave, porque afecta a empresas que no deberían tener problemas.

## Qué lo mueve
Lo mismo que el HY con menos intensidad, más la oferta de emisiones (las grandes emisiones de fusiones amplían el spread temporalmente) y la demanda de aseguradoras y fondos de pensiones.

## Qué mueve
- El coste de capital de las grandes empresas: WACC = tipo del Tesoro + spread IG para la deuda, más el coste del capital para los fondos propios.
- El ratio BBB/HY: cuando el spread BBB se acerca al BB, el mercado anticipa rebajas de rating.
- Bancos y aseguradoras, que tienen carteras de bonos IG: spreads que se amplían reducen su valor contable.

## Umbrales en el motor
Sin umbral: el HY da la misma señal antes y con más amplitud. Se muestra para confirmar: un HY en 400 con IG en 90 es un problema de las empresas débiles; un HY en 400 con IG en 150 es un problema de todas.

## Casuísticas relacionadas
→ [[ig-se-amplia-con-hy-estable]]: raro; suele ser oferta de emisiones o un problema de un sector grande (bancos en 2023).
→ [[angeles-caidos]]: rebajas masivas de BBB a HY en recesión; 2020 vio 200.000 M$ en tres meses.

## Trampas de lectura
- **FRED solo sirve por API los últimos ~3 años de las series ICE BofA** (restricción de licencia): el percentil "a 10 años" del email es, para esta serie, un percentil a 3 años, y el email lo indica entre paréntesis. El histórico completo se ve en el gráfico de la web de FRED y en los índices de ICE.
- El spread IG está contaminado por la duración: el índice tiene vencimiento medio de 10-12 años; parte de su variación es prima de plazo, no riesgo de crédito.
- Los bancos pesan mucho en el índice; un problema bancario (mar-2023) mueve el IG más que el HY.

## Episodios
- **Marzo 2020**: de 100 a 400 pb en tres semanas; el mercado primario IG se cerró durante una semana, algo que no pasó ni en 2008. La Fed intervino comprando bonos IG; en abril las empresas emitieron un récord de 300.000 M$.
- **Marzo 2023**: SVB y Credit Suisse; el IG subió de 120 a 165 pb en dos semanas, más proporcionalmente que el HY, porque los bancos son IG.
- **Octubre 2026**: 84 pb, percentil 47; sin señal.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/BAMLC0A0CM y la BBB: https://fred.stlouisfed.org/series/BAMLC0A4CBBB
- Fed, informe de estabilidad financiera (semestral, con sección de crédito corporativo): https://www.federalreserve.gov/publications/financial-stability-report.htm
