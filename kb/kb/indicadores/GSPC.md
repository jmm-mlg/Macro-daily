---
tipo: indicador
id: ^GSPC
nombre: S&P 500
bloque: Mercado
fuente: S&P Dow Jones Indices vía yfinance (^GSPC)
frecuencia: diaria (tiempo real)
publicacion: sesión de 9:30 a 16:00 ET
en_el_motor: nivel; peso 2 en riesgo (percentil ≥ 85 / ≤ 30, tendencia ±100 puntos); señal cruzada con DFII10
relacionados: [DFII10, ^VIX, BAMLH0A0HYM2, earnings-yield, prima-de-riesgo, amplitud-de-mercado, concentracion]
actualizado: 2026-10-08
---

# S&P 500

Las 500 mayores empresas cotizadas de EE.UU., ponderadas por capitalización. Es a la vez el activo que el motor intenta leer y uno de sus insumos: su posición en la década mide el apetito por el riesgo, y su relación con el tipo real, la prima de riesgo.

## Qué mide
Índice de precios (sin dividendos) ponderado por capitalización ajustada por flotante. En 2026 las diez mayores empresas pesan más del 35 % del índice, lo que hace que su comportamiento dependa de pocas compañías (tecnología y comunicación son el 40 %). El índice equiponderado (RSP) es la lectura de "la empresa media".

## Cómo se lee
- **Percentil a 10 años**: por construcción el S&P 500 pasa mucho tiempo en percentiles altos (tendencia alcista), por lo que el percentil 100 solo dice que está en máximos; lo informativo es la combinación con tipos y spreads.
- **Earnings yield** (beneficio por acción esperado a 12 meses / precio ≈ 1/PER): con PER 25, 4 %. Comparado con el tipo real (prima de riesgo) o con el 10 años nominal ("modelo de la Fed", criticado).
- **Amplitud**: porcentaje de valores por encima de su media de 200 sesiones; por debajo del 40 % con el índice en máximos, la subida es estrecha y frágil (2024, 2026).
- **Distancia a la media de 200 sesiones**: > 10 % extendido; < −10 % sobrevendido.
- **Reacción a datos**: la variable que el email no tiene; un buen dato que el índice vende es más informativo que el dato.

## Qué lo mueve
A largo plazo, beneficios (el BPA del S&P 500 ha crecido un 6-7 % anual desde 1950) y la tasa a la que se descuentan (tipo real más prima de riesgo). A corto, flujos, posicionamiento, Fed, y la narrativa dominante.

## Qué mueve
- Efecto riqueza: el consumo del 20 % de hogares con más patrimonio sigue a la bolsa; ese quintil es la mitad del consumo.
- Condiciones financieras (NFCI lo incluye): una bolsa alta relaja las condiciones y obliga a la Fed a ser más dura.
- PCE, vía servicios financieros imputados.
- Confianza empresarial y del consumidor.

## Umbrales en el motor
Peso 2 en riesgo por percentil. Señal cruzada con DFII10 cuando ambos superan el percentil 85.

## Casuísticas relacionadas
→ [[bolsa-y-tipo-real-en-maximos]].
→ [[amplitud-estrecha-en-maximos]]: índice en máximos con menos del 40 % de valores sobre su media de 200; 2024, 2026.
→ [[buenas-noticias-son-malas-noticias]]: cuándo el índice cae con datos fuertes.
→ [[correccion-del-10-por-ciento]]: frecuencia (una al año de media) y qué la distingue de un mercado bajista (cuando coincide con HY > 400 y curva).

## Trampas de lectura
- El percentil 100 no es señal de venta: el índice está en máximos históricos el 7 % de las sesiones y los retornos a 12 meses desde máximos son iguales a la media.
- La concentración hace que el índice diga poco sobre la empresa media; mirar el equiponderado y el Russell 2000.
- El PER depende del BPA esperado, que los analistas revisan a la baja en recesión: un PER de 18 con BPA que va a caer un 20 % es un PER de 22.

## Episodios
- **Octubre 2007**: máximo con HY en 400 pb (desde 250 en junio), NFCI subiendo, permisos cayendo dos años. Mínimo en marzo de 2009, −57 %.
- **Marzo 2020**: −34 % en 23 sesiones, la caída más rápida de la historia; suelo el 23 de marzo con el anuncio de QE ilimitado.
- **2022**: −25 % con BPA plano, todo compresión de múltiplos por el tipo real; suelo en octubre con IPC al 7,7 %.
- **Octubre 2026**: 7.826, percentil 100, con tipo real en percentil 100 y HY subiendo 44 pb en el mes.

## Para profundizar
- S&P Dow Jones Indices, metodología y composición: https://www.spglobal.com/spdji/en/indices/equity/sp-500/
- Shiller, datos históricos de PER, dividendos y tipos desde 1871 (CAPE): http://www.econ.yale.edu/~shiller/data.htm
- Yardeni Research, gráficos gratuitos de valoración y beneficios: https://www.yardeni.com/
