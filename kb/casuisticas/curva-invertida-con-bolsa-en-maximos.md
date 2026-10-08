---
tipo: casuistica
id: curva-invertida-con-bolsa-en-maximos
nombre: Curva invertida con la bolsa en máximos
señales: [T10Y2Y < 0, ^GSPC percentil ≥ 90]
en_el_motor: alerta de curva invertida + ^GSPC en percentil alto; T10Y2Y −1 y ^GSPC +1 en el score de riesgo se compensan
relacionados: [T10Y2Y, ^GSPC, BAMLH0A0HYM2, ICSA, curva-se-desinvierte, credito-avisa-antes-que-la-bolsa]
actualizado: 2026-10-09
---

# Curva invertida con la bolsa en máximos

Los bonos dicen recesión y las acciones dicen expansión. Es la situación más frecuente de lo que parece: la curva se invierte 6-18 meses antes de la recesión y la bolsa suele subir durante la mayor parte de ese plazo (2006-2007: 18 meses, +25 %). Operar la inversión vendiendo bolsa es llegar un año antes. La pregunta útil no es "quién tiene razón" sino "cuánto queda".

## Cómo identificarla
- T10Y2Y negativo durante más de un mes.
- S&P 500 en percentil ≥ 90 o en máximos históricos.
- Lo que separa "queda mucho" de "queda poco": HY (si está en mínimos, queda mucho; si ha subido 100 pb desde el mínimo, queda poco), peticiones (en mínimos / subiendo), NFCI (laxo / endureciendo), y la propia curva (profundizando la inversión / empezando a desinvertir).

## Qué significa
El mercado de bonos descuenta que la Fed tendrá que recortar mucho; el de acciones descuenta que los beneficios seguirán creciendo mientras tanto. Ambos pueden tener razón secuencialmente: la bolsa sube hasta que el crédito o el empleo se rompen, y entonces cae. La inversión no es señal de venta; la desinversión por bull steepening con peticiones subiendo sí.

## Qué reacciona
- Durante la inversión: bancos pierden margen relativo (pero lo compensan con tipos altos si los depósitos no se repreciaban: 2022-2024); utilities y REITs sufren por tipos cortos altos; growth de calidad y megacaps lideran (2023-2024).
- Al resolverse: ver [[curva-se-desinvierte]].

## Qué hacer (en términos del embudo)
- No reducir exposición solo por la inversión; mantener la banda del régimen.
- Sí: preparar la lista de defensivos y revisar las frases "cierro si…" para que incluyan los disparadores de peticiones y HY.
- Rotar progresivamente hacia calidad (balance limpio, caja) conforme la inversión madure (> 12 meses) y el HY suba desde mínimos.
- Marcar la desinversión como el momento de decidir.

## Qué la resuelve
- Recesión: la bolsa cae un 20-50 % empezando 0-6 meses después de la desinversión (2001, 2008).
- Falso positivo: la curva se desinvierte por recortes preventivos sin recesión (2024); la bolsa sigue subiendo.

## Episodios
- **Diciembre 2005 - junio 2007**: 18 meses invertida con el S&P 500 +25 %; techo en octubre de 2007, cuatro meses después de la desinversión.
- **Febrero 2000**: invertida con el Nasdaq en máximo; techo en marzo de 2000, un mes después; recesión en marzo de 2001.
- **Julio 2022 - septiembre 2024**: 26 meses invertida con el S&P 500 +45 % (desde el mínimo de octubre de 2022); sin recesión. El caso que más ha cuestionado la regla; explicación habitual: exceso de reservas, refinanciación a largo en 2021, política fiscal expansiva.

## Para profundizar
- Campbell Harvey (Duke), sobre la curva como indicador y sus falsos positivos (entrevistas y papers en SSRN)
- Fed de Cleveland, modelo de probabilidad de recesión por la curva (10 años − 3 meses): https://www.clevelandfed.org/indicators-and-data/yield-curve-and-predicted-gdp-growth
