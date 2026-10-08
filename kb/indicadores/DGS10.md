---
tipo: indicador
id: DGS10
nombre: Treasury a 10 años
bloque: Tipos
fuente: Tesoro de EE.UU. vía FRED (DGS10); en mercado, yfinance ^TNX
frecuencia: diaria
publicacion: cada día hábil, cierre EE.UU.; ^TNX en tiempo real
en_el_motor: peso 2 (invertido) en el score de liquidez por percentil (≥ 85 alto, ≤ 30 bajo); disparador > 5,50 %
relacionados: [DFII10, T10YIE, DGS2, T10Y2Y, MORTGAGE30US, prima-de-plazo, earnings-yield]
actualizado: 2026-10-08
---

# Treasury a 10 años

El tipo de interés de referencia del mundo: fija el coste de las hipotecas, el de la deuda corporativa y la vara con la que se mide el rendimiento de la bolsa (earnings yield).

## Qué mide
Rendimiento al vencimiento del bono del Tesoro de EE.UU. a 10 años, a precio de mercado. Se descompone en tipo real (DFII10) más inflación esperada (T10YIE), o alternativamente en tipos cortos esperados más prima de plazo. ^TNX en yfinance es el mismo dato multiplicado por 10 (52,8 = 5,28 %).

## Cómo se lee
- Nivel frente al earnings yield del S&P 500 (inverso del PER adelantado): cuando el 10 años supera al earnings yield, el bono ofrece más que la bolsa sin riesgo de beneficios. Ocurrió en 2000 y de nuevo en 2024-2026.
- Nivel frente al tipo de la Fed: 10 años por debajo del tipo oficial = curva invertida (ver T10Y2Y).
- Variación: +25 pb en una semana es un movimiento grande; +50 pb en un mes, un shock. La bolsa tolera subidas lentas y castiga las rápidas.
- Percentil: por encima del percentil 85 de la década, el mercado hipotecario y el inmobiliario comercial empiezan a tensarse.

## Qué lo mueve
Expectativas de política monetaria (el 2 años las resume), inflación esperada, oferta del Tesoro (subastas, déficit), demanda extranjera, aversión al riesgo (en pánico baja: "flight to quality"). Reacciona a nóminas, IPC y FOMC en segundos.

## Qué mueve
- Hipotecas a 30 años (≈ 10 años + 150-250 pb según el momento) y con ellas vivienda, constructoras y mejora del hogar.
- Coste de la deuda corporativa: investment grade cotiza como 10 años + spread.
- Valoración de todo activo de larga duración: growth, REITs, utilities, infraestructuras.
- Dólar: directa, vía diferencial con Alemania y Japón.
- Bancos: la pendiente (ver T10Y2Y) más que el nivel.

## Umbrales en el motor
- Percentil ≥ 85: señal negativa de liquidez; ≤ 30: positiva. Peso 2, inferior al tipo real (3), porque parte de la subida nominal puede ser inflación esperada y no restricción real.
- Disparador 5,50 %: nivel al que un bono sin riesgo rinde más que el earnings yield típico de la bolsa (en torno al 4 % con PER 25), haciendo la comparación insostenible salvo con crecimiento de beneficios superior al 8 % anual.

## Casuísticas relacionadas
→ [[subida-rapida-del-10-anos]]: más de 50 pb en un mes; qué sectores caen primero.
→ [[bono-supera-earnings-yield]]: el "modelo de la Fed" invertido.
→ [[curva-se-desinvierte]]: cuando el 10 años sube más que el 2 años (bear steepening) frente a cuando el 2 años cae (bull steepening).

## Trampas de lectura
- Subida del 10 años por inflación esperada (breakeven) no es lo mismo que por tipo real: la primera favorece a materias primas y bancos, la segunda castiga a todo.
- Un 10 años que baja en pánico no es "liquidez": es huida. Mirar el spread HY al mismo tiempo.
- Las subastas del Tesoro (martes-jueves de semanas concretas) mueven el 10 años 5-10 pb sin dato macro; no leer eso como cambio de régimen.

## Episodios
- **1994**: de 5,8 % a 8,0 % en un año por subidas de la Fed sin aviso; el peor año de la historia de los bonos; la bolsa acabó plana pero con una caída del 9 % a mitad de año.
- **Octubre 2023**: toca el 5,0 % por primera vez desde 2007 por prima de plazo (déficit, emisiones); S&P 500 −10 % desde julio; da la vuelta en cuanto el Tesoro reduce la emisión a largo plazo (1 de noviembre).
- **Abril 2025**: sube 50 pb en una semana en plena caída de la bolsa por los aranceles, rompiendo la correlación habitual; fue la señal de que el mercado dudaba del Tesoro como refugio y precipitó el giro de la política arancelaria.
- **2026**: 5,28 % en octubre, percentil 100 de la década, con la bolsa en máximos.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/DGS10
- Modelo de prima de plazo de la Fed de Nueva York (ACM): https://www.newyorkfed.org/research/data_indicators/term-premia-tabs
- Calendario de subastas del Tesoro: https://www.treasurydirect.gov/auctions/upcoming/
