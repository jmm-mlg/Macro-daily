---
tipo: casuistica
id: bancos-y-curva
nombre: Curva empinando con spreads de crédito subiendo (bancos)
señales: [T10Y2Y +15 pb o más en el mes, BAMLH0A0HYM2 +50 pb o más en el mes]
en_el_motor: factor curva +1 y factor crédito −1 se anulan en financiero; sesgo 0 con "pelea" visible en la columna Por qué
relacionados: [T10Y2Y, BAMLH0A0HYM2, ICSA, curva-y-margen-bancario, credito-a-actividad, curva-se-desinvierte]
actualizado: 2026-10-09
---

# Curva empinando con spreads de crédito subiendo

La curva dice que el margen bancario va a mejorar; el crédito dice que las provisiones van a subir. Para un banco, el margen se cobra trimestre a trimestre y las pérdidas por morosidad llegan de golpe: cuando ambos factores están activos, la historia dice que las provisiones ganan. Por eso el motor deja a financiero en 0 cuando la curva empina y el HY sube a la vez, y por eso un sesgo +1 por curva no vale si el crédito lo contradice.

## Cómo identificarla
- Curva empinando más de 15 pb en el mes (el factor del motor).
- HY subiendo más de 50 pb en el mes o por encima de 450 pb (el otro factor).
- Mejor aún, el tipo de empinamiento: si es bull steepening (2 años cayendo) con HY subiendo, es la combinación de 2007 (recortes de emergencia + crédito rompiéndose). Si es bear steepening con HY subiendo ligeramente desde mínimos (octubre 2026: curva +6, HY +44), es un aviso temprano, no una señal.
- Confirmar con la encuesta SLOOS (estándares de crédito endureciéndose) y con los resultados de los bancos (provisiones, morosidad de tarjetas, "charge-offs").

## Qué significa
El ciclo de crédito está girando: los bancos van a prestar menos y a perder más. El margen de interés, que es lo que el factor curva captura, mejora en el papel, pero los bancos lo usan para provisionar. Los bancos con más exposición a consumo (tarjetas, autos) y a inmobiliario comercial lo notan primero; los de banca de inversión y gestión, después.

## Qué reacciona
| Subsector | Comportamiento |
| --- | --- |
| Bancos regionales (EE.UU.) | Los primeros en caer: inmobiliario comercial y depósitos |
| Finanzas al consumo (Capital One, Synchrony) | Caen con la morosidad; son el adelantado |
| Grandes bancos (JPMorgan, BNP) | Aguantan mejor por diversificación; provisionan antes |
| Aseguradoras | Poco afectadas salvo por cartera de bonos |
| Pagos (Visa, Mastercard) | Siguen al volumen de gasto, no al crédito; aguantan |

## Qué hacer (en términos del embudo)
- Financiero fuera de la lista de candidatas aunque el factor curva sea +1; el conflicto entre factores es un veto, no un empate.
- Si hay posiciones en bancos: stop en el último mínimo relevante y reducir a la mitad si el HY cruza 400.
- Lo que resuelve: los resultados del trimestre (JPMorgan el 13 de octubre de 2026): si las provisiones suben más que el margen, el crédito tenía razón.

## Qué la resuelve
- HY vuelve a bajar con la curva empinada: los bancos suben con fuerza (1995, 2019 segundo semestre).
- HY sigue subiendo: provisiones, caídas del 20-40 % en bancos (2007-2008, 2001).

## Episodios
- **Verano 2007**: curva desinvirtiendo (bull) con HY de 250 a 450 pb; los bancos hicieron máximos en febrero de 2007 y cayeron un 25 % antes de que el índice hiciera techo en octubre.
- **Marzo 2023**: curva plana, HY +100 pb en dos semanas por SVB; regionales −25 %; los grandes recuperaron en tres meses porque el crédito no se rompió (la Fed abrió el BTFP).
- **Octubre 2026**: curva +6 pb (no activa), HY +44 pb (no activa); financiero en 0 "sin factores activos". Vigilar: ambos están a punto.

## Para profundizar
- Fed, SLOOS (encuesta a responsables de préstamos): https://www.federalreserve.gov/data/sloos.htm
- FDIC, Quarterly Banking Profile (margen y morosidad del sistema): https://www.fdic.gov/quarterly-banking-profile
