---
tipo: mecanismo
id: tipo-real-y-multiplos
nombre: Tipo real → múltiplos de valoración
cadena: "Tipo real sube → tasa de descuento sube → valor presente de beneficios futuros cae → PER cae, más cuanto más lejanos los beneficios"
plazo: "semanas (el mercado reprecia rápido); el efecto en sectores de larga duración es inmediato"
series: [DFII10, DGS10, ^GSPC]
sectores: [tecnologia, comunicacion, inmobiliario, utilities]
casuisticas: [bolsa-y-tipo-real-en-maximos, subida-rapida-del-10-anos]
actualizado: 2026-10-08
---

# Tipo real → múltiplos de valoración

El mecanismo más importante del motor. El precio de una acción es el valor presente de sus beneficios futuros, descontados a una tasa que es el tipo real más una prima de riesgo. Si el tipo real sube 100 pb y nada más cambia, el valor de un flujo a 10 años cae un 9 %, el de un flujo a 20 años un 17 %, y el de un flujo a 1 año un 1 %. Por eso el mismo movimiento de tipos castiga a una software sin beneficios (cuyos flujos están lejos) mucho más que a una tabaquera (cuyos flujos son ahora).

## Cadena
1. La Fed endurece (o el mercado lo descuenta) → el 2 años sube → el 10 años nominal sube.
2. Si la inflación esperada no sube, la subida del nominal es subida del **tipo real**.
3. La tasa de descuento del mercado sube en la misma magnitud (la prima de riesgo cambia poco a corto plazo).
4. El PER adelantado del índice cae. Regla aproximada observada 2010-2024: ~1 punto de PER por cada 50 pb de tipo real sostenidos, desde un PER de 18-22.
5. Dentro del índice, la rotación: de duración larga (growth, REITs, utilities) a duración corta (value, energía, bancos).

## Plazo y magnitud
- Reacción del índice: días a semanas; el 80 % del ajuste en el primer mes.
- Rotación sectorial: semanas; dura mientras dura la tendencia del tipo real.
- Magnitud en 2022: tipo real +270 pb, PER del S&P 500 de 21 a 15, índice −25 % con BPA plano; Nasdaq −33 %; software no rentable −70 %.

## Evidencia
- Toda la teoría de valoración (DCF). Empíricamente, la correlación entre cambios del tipo real y cambios del PER del S&P 500 es negativa y fuerte desde 1997 (cuando existen TIPS).
- Asness, "Fight the Fed Model" (2003): hay que comparar earnings yield con tipo real, no con nominal.
- Damodaran, primas de riesgo implícitas: cuando el tipo real sube y el índice no cae, la prima implícita se comprime, y las primas comprimidas predicen retornos bajos a 5-10 años.

## Cuándo falla
- Cuando el tipo real sube por crecimiento fuerte: los beneficios esperados suben a la vez y compensan (2017, 2024). Mirar GDPNow y revisiones de analistas.
- Cuando la prima de riesgo cae a la vez (mercado eufórico): el múltiplo aguanta pese al tipo real (2026). Es la situación de la casuística "bolsa y tipo real en máximos".
- Cuando la subida del nominal es inflación esperada (breakeven) y no tipo real: el efecto es sectorial (favorece materias primas), no de múltiplo general.

## Qué hacer con ello
- Antes de cualquier posición de duración larga (growth, REITs, utilities), mirar la tendencia del tipo real a 1 y 3 meses; con tendencia alcista, no.
- En rotación por tipo real, preferir sectores con flujos cercanos y balance limpio.
- El pico del tipo real ha coincidido con el suelo de la bolsa en 2018, 2022 y 2023: cuando la Fed señala el fin de las subidas, la duración rebota primero y más.
