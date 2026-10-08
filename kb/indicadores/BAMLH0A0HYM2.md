---
tipo: indicador
id: BAMLH0A0HYM2
nombre: Spread High Yield (ICE BofA US High Yield OAS)
bloque: Crédito
fuente: ICE BofA vía FRED (BAMLH0A0HYM2)
frecuencia: diaria
publicacion: cada día hábil con un día de retraso
en_el_motor: alerta > 5,0 %; peso 2 (invertido) en liquidez (> 5,0 / < 3,5) y peso 2 (invertido) en riesgo por percentil; factor "crédito" (> 4,5 o +0,5 en el mes); disparador > 4,0 %
relacionados: [BAMLC0A0CM, NFCI, VIX, ciclo-de-credito, credito-avisa-antes-que-la-bolsa, estres-de-credito]
actualizado: 2026-10-08
---

# Spread High Yield (OAS)

Lo que pagan las empresas con peor calificación crediticia por encima del Tesoro. Es el precio del riesgo de impago, y el mercado de crédito suele detectar los problemas antes que la bolsa porque sus inversores solo ganan el cupón y pierden el principal: miran el riesgo, no el potencial.

## Qué mide
Diferencial, ajustado por opciones (OAS), entre el rendimiento del índice de bonos corporativos de alto rendimiento de EE.UU. (calificación BB o inferior) y la curva del Tesoro. En puntos porcentuales; 3,12 = 312 puntos básicos.

## Cómo se lee
| Spread | Lectura | Contexto |
| --- | --- | --- |
| < 3,0 % (300 pb) | Complacencia; el riesgo está barato | 2007, 2021, 2024-2026 |
| 3,0-4,0 % | Normal en expansión | Mayor parte de 2017-2019 |
| 4,0-5,0 % | Tensión: los inversores piden más por el riesgo; vigilar | 2016, 2018 Q4 |
| 5,0-7,0 % | Estrés: refinanciar es caro; sube la morosidad | 2011, 2016, 2022 |
| > 8 % (800 pb) | Crisis: el mercado primario se cierra | 2008 (hasta 2.000 pb), mar-2020 (1.100 pb) |

Lo que más informa es la **variación en un mes**: +50 pb desde niveles bajos ha precedido a las correcciones bursátiles de 2015, 2018 y 2022 con 4-8 semanas de adelanto; +100 pb en un mes ha coincidido con el inicio de caídas mayores.

## Qué lo mueve
Expectativas de impagos (que dependen del ciclo y de los tipos), apetito por el riesgo, liquidez de los fondos de crédito, petróleo (el sector energía pesa en el índice HY; en 2015-2016 el spread subió por el crudo), y la oferta de emisiones.

## Qué mueve
- **Coste de refinanciación** de las empresas endeudadas: cuando supera el 8-9 % de rendimiento total, las empresas con vencimientos cercanos entran en problemas.
- **Bolsa con retardo**: el HY suele moverse 1-2 meses antes que el S&P 500 en los giros a la baja; en los giros al alza son más simultáneos.
- **Sectores apalancados**: inmobiliario, telecos, energía de segunda fila, consumo discrecional financiado.
- **Small caps**: el Russell 2000 tiene mucha más deuda a tipo variable que el S&P 500 y sigue al spread HY de cerca.

## Umbrales en el motor
- Alerta en 500 pb: nivel histórico de estrés.
- Disparador en 400 pb: desde niveles bajos, cruzar 400 es la primera señal de que el ciclo de crédito gira.
- Factor "crédito" por nivel > 450 o por subida > 50 pb en el mes: la velocidad importa tanto como el nivel. Carga −1 en discrecional, financiero e inmobiliario; −0,5 en tecnología, industriales, materiales, energía, utilities.
- Peso 2 en liquidez y en riesgo: es la única serie en los dos scores porque informa de ambas cosas.

## Casuísticas relacionadas
→ [[credito-avisa-antes-que-la-bolsa]]: HY sube 50 pb con la bolsa en máximos; qué ha pasado después históricamente.
→ [[hy-sube-con-vix-bajo]]: divergencia; el VIX suele alcanzar al HY, no al revés.
→ [[spread-sube-por-petroleo]]: 2015-2016; cuándo es sectorial y cuándo es sistémico.

## Trampas de lectura
- La calidad del índice HY ha mejorado desde 2020 (más BB, menos CCC); un 350 hoy es algo más estricto que un 350 en 2007. Comparar también el spread CCC.
- El spread se publica con un día de retraso; el ETF HYG en tiempo real lo anticipa.
- Un spread bajo no es señal de compra sino de que el riesgo está caro; es un indicador de riesgo, no de oportunidad, salvo en extremos altos (> 800), que han sido las mejores compras de la historia del crédito.

## Episodios
- **Junio 2007**: 250 pb, mínimo histórico, con los primeros fondos de hipotecas subprime quebrando. Doce meses después, 800; en diciembre de 2008, 2.000. La bolsa hizo máximos en octubre de 2007, cuatro meses después del mínimo del spread.
- **Diciembre 2015 - febrero 2016**: de 500 a 890 pb por el petróleo a 26 $; el S&P 500 cayó un 13 %. La señal fue sectorial (energía) pero el daño, general.
- **Febrero-marzo 2020**: de 350 a 1.100 pb en cinco semanas; la Fed anunció compras de bonos corporativos por primera vez en su historia (23 de marzo) y el spread volvió a 500 en dos meses.
- **2022**: de 300 a 600 pb entre enero y julio, en paralelo a la caída de la bolsa; sin crisis de impagos porque las empresas habían refinanciado en 2021 a tipos bajos.
- **Octubre 2026**: 312 pb, +44 pb en el mes; nivel bajo pero la dirección ha cambiado.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/BAMLH0A0HYM2 y la de CCC: https://fred.stlouisfed.org/series/BAMLH0A3HYC
- Moody's, tasa de impago histórica y previsiones (resúmenes públicos): https://www.moodys.com/
- Howard Marks, memos sobre el ciclo de crédito (Oaktree): https://www.oaktreecapital.com/insights
