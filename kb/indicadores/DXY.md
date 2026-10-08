---
tipo: indicador
id: DX-Y.NYB
nombre: Índice del dólar (DXY)
bloque: Mercado
fuente: ICE vía yfinance (DX-Y.NYB)
frecuencia: diaria (tiempo real)
publicacion: continuo
en_el_motor: nivel; factor "dólar" (percentil ≥ 75 fuerte / ≤ 25 débil; carga −1 en materiales, −0,5 en tecnología, comunicación, salud, industriales, energía, básico)
relacionados: [DFII10, ECBDFR, DFF, euro-dolar, beneficios-exteriores, emergentes, dolar-fuerte-y-materias-primas]
actualizado: 2026-10-08
---

# Índice del dólar (DXY)

El valor del dólar frente a una cesta de seis divisas (euro 58 %, yen 14 %, libra 12 %, dólar canadiense 9 %, corona sueca 4 %, franco suizo 4 %). Un dólar fuerte reduce los beneficios de las multinacionales americanas al convertirlos, encarece las materias primas para el resto del mundo y tensiona a los emergentes endeudados en dólares.

## Qué mide
Media geométrica ponderada del tipo de cambio del dólar frente a esas seis divisas; base 100 en 1973. Por su composición es sobre todo un índice euro-dólar invertido. El "dólar ponderado por comercio" de la Fed (DTWEXBGS en FRED) incluye China y México y es más representativo, pero el DXY es el que cotiza y el que miran los operadores.

## Cómo se lee
| DXY | Lectura (últimos 20 años) |
| --- | --- |
| > 105 | Dólar fuerte; estrés en emergentes y materias primas (2022: 114) |
| 95-105 | Rango normal |
| < 90 | Dólar débil; favorable a materias primas, emergentes y multinacionales (2017, 2020-2021) |

La tendencia importa más que el nivel: un dólar que sube un 5 % en un trimestre resta 2-3 puntos de crecimiento de beneficios al S&P 500 (el 40 % de sus ventas son exteriores). Y la causa: dólar fuerte por diferencial de tipos (2022) es distinto de dólar fuerte por refugio (2008, mar-2020) o por crecimiento relativo (2024).

## Qué lo mueve
Diferencial de tipos reales entre EE.UU. y el resto (el principal), crecimiento relativo, aversión al riesgo (el dólar sube en pánico), política comercial (los aranceles de 2025 lo debilitaron, contra la teoría, por la pérdida de confianza), intervenciones (Japón en 2022 y 2024), y flujos de reservas.

## Qué mueve
- Beneficios de las multinacionales de EE.UU. (tecnología, salud, consumo básico): la "cobertura natural" de los exportadores europeos es inversa.
- Materias primas en dólares (inversa): petróleo, cobre, oro.
- Emergentes: deuda en dólares más cara; salidas de capital.
- Inflación importada en Europa y Japón.
- Condiciones financieras globales: un dólar fuerte es endurecimiento para todo el mundo salvo EE.UU.

## Umbrales en el motor
Factor "dólar" por percentil: ≥ 75 activa cargas negativas en los sectores con más ventas exteriores o ligados a materias primas; ≤ 25 las invierte. No está en ningún score porque su efecto es sectorial, no de régimen.

## Casuísticas relacionadas
→ [[dolar-fuerte-y-materias-primas]]: cuándo el dólar manda sobre el cobre y el petróleo y cuándo no (2022: ambos subieron).
→ [[dolar-sube-con-bolsa-cayendo]]: refugio; 2008, 2020; qué lo distingue de un dólar de tipos.
→ [[dolar-cae-con-tipos-subiendo]]: 2025; pérdida de confianza; señal de régimen anómalo.

## Trampas de lectura
- Es un índice euro-dólar: un movimiento del BCE lo mueve tanto como uno de la Fed.
- No incluye China ni México, los dos mayores socios comerciales de EE.UU.
- Las multinacionales cubren el riesgo de cambio con retardo; el efecto en resultados llega 1-2 trimestres después.

## Episodios
- **2014-2015**: +25 % en un año (de 80 a 100) por la divergencia Fed-BCE; beneficios del S&P 500 planos en 2015 por la conversión; petróleo de 100 a 30.
- **Septiembre 2022**: 114, máximo desde 2002, con la Fed subiendo 75 pb y el euro por debajo de la paridad; emergentes y materias primas (salvo energía) en mínimos.
- **Abril 2025**: cayó un 5 % en un mes mientras el 10 años subía: la combinación anómala que señaló la desconfianza en los activos de EE.UU. tras los aranceles.
- **Octubre 2026**: 101,9, +2,7 en el mes, percentil 73; a punto de activar el factor.

## Para profundizar
- Dólar ponderado por comercio de la Fed (más representativo): https://fred.stlouisfed.org/series/DTWEXBGS
- BIS, tipos de cambio efectivos y liquidez global en dólares: https://www.bis.org/statistics/eer.htm
- Fed de Nueva York, encuesta trimestral del mercado de divisas: https://www.newyorkfed.org/markets/fxc
