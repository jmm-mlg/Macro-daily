---
tipo: indicador
id: UMCSENT
nombre: Confianza del consumidor (Universidad de Michigan)
bloque: Actividad
fuente: Universidad de Michigan, Surveys of Consumers, vía FRED (UMCSENT, dato final mensual)
frecuencia: mensual (preliminar el segundo viernes, final el cuarto viernes, 10:00 ET)
en_el_motor: nivel; peso 1 en crecimiento (percentil ≥ 60 / ≤ 15, tendencia ±2; umbral bajo rebajado de 25 a 15 el 2026-10-08); en el calendario
relacionados: [RSAFS, CPIAUCSL, T10YIE, expectativas-de-inflacion, consumo-fuerte-con-confianza-baja, conference-board]
actualizado: 2026-10-08
---

# Confianza del consumidor (Michigan)

Cómo ven los hogares su situación financiera y la economía, según una encuesta telefónica a unas 600 personas. Es un indicador de sentimiento, no de gasto: dice cómo se siente la gente, no lo que hace. Su valor está en los extremos y en el componente de expectativas de inflación, que la Fed vigila.

## Qué mide
Índice compuesto (1966 = 100) a partir de cinco preguntas sobre situación financiera actual y futura, condiciones económicas a 1 y 5 años, y si es buen momento para comprar bienes duraderos. Se publica con dos subíndices (condiciones actuales y expectativas) y con las expectativas de inflación a 1 y a 5-10 años, que son la parte que mueve el mercado.

## Cómo se lee
| Índice | Lectura |
| --- | --- |
| > 90 | Optimismo; típico de expansión madura (2018-2019: 95-100) |
| 70-90 | Normal |
| 55-70 | Pesimismo; típico de recesión o inflación alta |
| < 55 | Extremo; mínimos históricos (junio 2022: 50,0; 2026: 51,7) |

Los extremos bajos han sido, de forma contraintuitiva, buenos momentos para la bolsa: el mínimo de junio de 2022 coincidió con el suelo del mercado bajista a cuatro meses vista; el de 2008 (55) precedió al suelo de 2009 por cuatro meses. La confianza en mínimos con consumo que aguanta (octubre 2026) es una divergencia que el motor marca.

**Expectativas de inflación a 5-10 años**: > 3 % desancladas (la Fed las cita como argumento para no recortar); 2,5-3 % normales. A 1 año: muy sensibles a la gasolina y a los titulares; en 2025 saltaron al 6 % por los aranceles.

## Qué lo mueve
Gasolina (el precio más visible), inflación de alimentos, bolsa (para los hogares con cartera), titulares de despidos, política (desde 2016 la encuesta tiene un sesgo partidista fuerte: la confianza de cada partido cambia con quién gobierna, lo que reduce su valor como indicador económico).

## Qué mueve
- Poco de forma directa; el consumo se explica mejor por renta y empleo que por confianza.
- Expectativas de inflación: la Fed las cita; una lectura alta a 5-10 años endurece el tono.
- Sentimiento de mercado: un dato muy bajo refuerza las narrativas de recesión.

## Umbrales en el motor
Peso 1 por percentil, con umbrales asimétricos (≥ 60 positivo, ≤ 15 negativo). El umbral bajo se rebajó de 25 a 15 el 8 de octubre de 2026 porque el cambio metodológico de 2024 bajó el nivel de la serie y el percentil a 10 años mezcla dos metodologías. Zona muerta de ±2 puntos.

## Casuísticas relacionadas
→ [[consumo-fuerte-con-confianza-baja]]: ventas +1,1 % con el índice en percentil 5.
→ [[confianza-en-minimos-como-senal-contraria]]: 2008, 2011, 2022; el suelo de la bolsa cerca.
→ [[expectativas-de-inflacion-desancladas-en-michigan]]: 2022 y 2025; reacción de la Fed.

## Trampas de lectura
- Muestra pequeña (600); el error es grande; el dato preliminar y el final difieren varios puntos.
- Sesgo partidista desde 2016: comparar con el Conference Board (muestra de 3.000, más ligado al empleo).
- En 2024 Michigan cambió la metodología de teléfono a internet; el nivel bajó varios puntos por el cambio, no por la economía.

## Episodios
- **Junio 2022**: 50,0, mínimo histórico de la serie (desde 1952), con gasolina a 5 $ e inflación al 9 %. El S&P 500 hizo suelo en octubre; las expectativas de inflación a 5-10 años tocaron el 3,3 % y la Fed subió 75 pb en parte por ese dato (Powell lo citó).
- **Abril 2025**: expectativas de inflación a 1 año al 6,5 % por los aranceles, máximo desde 1981, con la inflación real al 2,4 %. La Fed no reaccionó.
- **Octubre 2026**: 51,7, −3,5, percentil 5; consumo nominal fuerte. Divergencia activa.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/UMCSENT y expectativas de inflación a 1 año: https://fred.stlouisfed.org/series/MICH
- Universidad de Michigan, tablas completas y comentario mensual: https://data.sca.isr.umich.edu/
- Conference Board, índice de confianza (contraste): https://www.conference-board.org/topics/consumer-confidence
