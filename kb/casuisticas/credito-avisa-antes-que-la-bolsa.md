---
tipo: casuistica
id: credito-avisa-antes-que-la-bolsa
nombre: El spread HY sube con la bolsa en máximos
señales: [BAMLH0A0HYM2 +50 pb o más en el mes desde niveles bajos, ^GSPC percentil ≥ 85]
en_el_motor: factor crédito se activa con +50 pb en el mes; HY pesa 2 en liquidez y 2 en riesgo; disparador 400 pb
relacionados: [BAMLH0A0HYM2, ^GSPC, ^VIX, NFCI, credito-a-actividad, hy-sube-con-vix-bajo, correccion-del-10-por-ciento]
actualizado: 2026-10-09
---

# El spread HY sube con la bolsa en máximos

El mercado de crédito empieza a cobrar más por el riesgo mientras el de acciones sigue celebrando. Históricamente el crédito ha avisado 4-8 semanas antes de las correcciones bursátiles de 2015, 2018 y 2022, y 4 meses antes del techo de 2007. No todas las subidas del HY acaban en corrección, pero casi todas las correcciones empezaron con una subida del HY que la bolsa ignoró.

## Cómo identificarla
- HY +50 pb en el mes desde niveles bajos (< 350 pb). Octubre 2026: +44, desde 268 a 312.
- S&P 500 en máximos o percentil ≥ 85.
- VIX sin acompañar (ver [[hy-sube-con-vix-bajo]]).
- Mirar qué sube dentro del HY: si es el tramo CCC (el más débil) es señal de ciclo; si es un sector (energía 2015), es sectorial; si es todo el índice, es apetito por el riesgo.

## Qué significa
Los inversores en bonos, que solo cobran cupón, ven más riesgo de impago o de iliquidez; o simplemente dejan de aceptar primas mínimas. El mercado de acciones, que mira el potencial, tarda en verlo. La subida es el primer eslabón del mecanismo [[credito-a-actividad]].

## Qué reacciona y en qué plazo
| Activo | Plazo típico |
| --- | --- |
| Small caps (Russell 2000) | Caen primero (2-4 semanas): deuda a tipo variable |
| Sectores apalancados (REITs, telecos, energía de segunda fila) | 2-6 semanas |
| S&P 500 | 4-8 semanas; corrección del 5-10 % si el HY sigue subiendo |
| VIX | Sube cuando la bolsa ya cae |

## Qué hacer (en términos del embudo)
- Reducir exposición agregada un escalón aunque el régimen no haya cambiado; sin nuevas posiciones en sectores con carga crédito −1 (discrecional, financiero, inmobiliario).
- Stops revisados en small caps y apalancadas.
- Disparador 400 pb: si lo cruza, reducir de verdad; 500: alerta.

## Qué la resuelve
- HY vuelve a bajar en 2-4 semanas: era un susto de posicionamiento; la bolsa sigue.
- HY sigue subiendo: corrección bursátil (2015, 2018) o techo (2007).

## Episodios
- **Junio-octubre 2007**: HY de 250 a 450 pb; S&P 500 en máximo el 9 de octubre; luego −57 %.
- **Junio-agosto 2015**: HY de 450 a 560 pb (energía); S&P 500 −12 % en agosto.
- **Septiembre-diciembre 2018**: HY de 320 a 540 pb; S&P 500 −20 %.
- **Enero-marzo 2022**: HY de 300 a 400 pb en enero; S&P 500 −13 % en el trimestre.
- **Octubre 2026**: HY +44 pb (268 → 312) con S&P 500 en máximos; disparador a 88 pb.

## Para profundizar
- FRED, HY y CCC (últimos 3 años por API; histórico en gráfico web): https://fred.stlouisfed.org/series/BAMLH0A0HYM2
- HYG y JNK (ETFs de HY) en tiempo real como proxy diario
