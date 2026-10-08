---
tipo: indicador
id: ^VIX
nombre: VIX (volatilidad implícita del S&P 500)
bloque: Mercado
fuente: Cboe vía yfinance (^VIX)
frecuencia: diaria (tiempo real)
publicacion: sesión de 9:30 a 16:15 ET
en_el_motor: nivel; alerta > 25; peso 3 (invertido) en riesgo (> 25 / < 15, tendencia ±2); disparador > 25
relacionados: [^GSPC, BAMLH0A0HYM2, NFCI, curva-del-vix, volatilidad-realizada, miedo-y-codicia]
actualizado: 2026-10-08
---

# VIX

La volatilidad que el mercado de opciones espera para el S&P 500 en los próximos 30 días, anualizada. Es el precio del seguro contra caídas: alto cuando hay miedo, bajo cuando hay complacencia. Es el único indicador del motor que es mejor comprar cuando está alto.

## Qué mide
Índice calculado por Cboe a partir de los precios de opciones del S&P 500 con vencimiento en torno a 30 días. Un VIX de 15 significa que el mercado espera un movimiento anualizado del 15 %, es decir, de aproximadamente el 1 % diario (15 / √252 ≈ 0,95). Un VIX de 30, del 2 % diario.

## Cómo se lee
| VIX | Lectura |
| --- | --- |
| < 12 | Complacencia extrema; históricamente precede a sacudidas (ene-2018, feb-2020) |
| 12-15 | Calma; típico de mercado alcista ordenado |
| 15-20 | Normal |
| 20-25 | Nerviosismo; correcciones del 5 % |
| 25-35 | Miedo; correcciones del 10 % en curso |
| > 35 | Pánico; 2008 (80), 2020 (82), ago-2024 (65 intradía), abr-2025 (60) |

Estructura temporal: normalmente los futuros del VIX a 3 meses cotizan por encima del VIX al contado (contango). Cuando el contado supera a los futuros (backwardation), el miedo es inmediato y suele marcar suelos de corto plazo.

## Qué lo mueve
Caídas de la bolsa (la relación es asimétrica: una caída del 3 % sube el VIX más de lo que una subida del 3 % lo baja), eventos con fecha (elecciones, FOMC, resultados de Nvidia), flujos de opciones (la venta sistemática de volatilidad por fondos lo comprime en mercados tranquilos), y el apalancamiento (en 2018 y 2024 los productos de volatilidad amplificaron los movimientos).

## Qué mueve
- Posicionamiento: muchos fondos sistemáticos dimensionan sus posiciones por la volatilidad; un VIX que sube obliga a vender, lo que sube el VIX ("vol-targeting").
- Spreads de crédito con retardo corto.
- NFCI, directamente (es uno de sus componentes).

## Umbrales en el motor
Peso 3 en riesgo, el máximo, invertido. 25 como umbral de miedo: por encima, los retornos del S&P 500 a 3-6 meses han sido superiores a la media (el miedo se paga). 15 como umbral de complacencia. Alerta y disparador en 25.

## Casuísticas relacionadas
→ [[vix-sobre-25]]: históricamente mejor comprar que vender; cuánto dura el pico.
→ [[hy-sube-con-vix-bajo]]: divergencia; el crédito avisa y el VIX se entera después.
→ [[vix-bajo-con-tipo-real-alto]]: complacencia con coste de capital alto; 2007, 2026.

## Trampas de lectura
- El VIX mide la volatilidad esperada, no la dirección; sube más con caídas pero puede subir en subidas violentas.
- Un VIX bajo no es señal de venta inmediata; puede estar bajo durante años (2017: media de 11).
- Los picos del VIX son rápidos (días) y la vuelta a la calma lenta (semanas); vender volatilidad en el pico es rentable pero arriesgado.
- El VIX intradía puede ser mucho mayor que el cierre (5 de agosto de 2024: 65 intradía, 38 al cierre).

## Episodios
- **5 de febrero de 2018 ("Volmageddon")**: el VIX pasó de 17 a 37 en un día; un producto inverso (XIV) perdió el 96 % y se liquidó. El S&P 500 cayó un 10 % y recuperó en dos meses.
- **16 de marzo de 2020**: cierre récord de 82,7. Suelo de la bolsa una semana después.
- **5 de agosto de 2024**: 65 intradía por el deshacer del carry del yen; el S&P 500 solo cayó un 3 % ese día; recuperó los máximos en un mes. Caso de pánico sin recesión.
- **Octubre 2026**: 15,2, percentil 34, estable; calma con tipo real en máximos.

## Para profundizar
- Cboe, metodología del VIX y datos históricos: https://www.cboe.com/tradable_products/vix/
- Curva de futuros del VIX (contango/backwardation): https://vixcentral.com/
- Cboe, "The VIX Index and Volatility-Based Global Indexes" (PDF introductorio gratuito): https://www.cboe.com/
