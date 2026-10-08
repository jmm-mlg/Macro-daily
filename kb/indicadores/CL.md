---
tipo: indicador
id: CL=F
nombre: Petróleo WTI (futuro continuo)
bloque: Mercado
fuente: NYMEX vía yfinance (CL=F)
frecuencia: diaria (tiempo real)
publicacion: continuo; inventarios de la EIA los miércoles a las 10:30 ET
en_el_motor: nivel; factor "petróleo" (percentil ≥ 80 caro / ≤ 25 barato; carga +1 en energía, −1 en discrecional, −0,5 en industriales, materiales, básico)
relacionados: [PPIFIS, CPIAUCSL, T10YIE, DX-Y.NYB, energia, inflacion-de-costes-vs-demanda, spread-sube-por-petroleo]
actualizado: 2026-10-08
---

# Petróleo WTI

El precio del crudo de referencia en EE.UU. Es a la vez un coste (para transporte, química, consumo) y un ingreso (para el sector energía, el 4 % del S&P 500 pero el 10 % de sus beneficios en años buenos), y el componente más volátil de la inflación general. Su efecto en la bolsa depende de por qué se mueve: por demanda es bueno, por oferta es malo.

## Qué mide
Precio del futuro de primer vencimiento del West Texas Intermediate en dólares por barril. El Brent (referencia europea y global) cotiza normalmente 2-6 $ por encima. Los futuros ruedan cada mes; el "continuo" encadena vencimientos y puede tener saltos en el cambio de contrato.

## Cómo se lee
| WTI ($/barril, 2020-2026) | Lectura |
| --- | --- |
| < 50 | Barato; estrés en productores de EE.UU. (shale no rentable por debajo de 45-55) |
| 50-70 | Rango cómodo para productores y consumidores |
| 70-90 | Caro; presión en IPC e IPP; margen fuerte para el sector |
| > 90 | Muy caro; destrucción de demanda; recesiones de 1974, 1980, 1990, 2008 precedidas por picos de petróleo |

La **causa** del movimiento: demanda (crecimiento global, China) o oferta (OPEP+, guerra, huracanes, shale). Una subida por demanda acompaña a cobre, bolsa y tipos al alza; una subida por oferta sube el petróleo con el cobre plano y la bolsa cayendo. En octubre de 2026, petróleo en percentil 91 con cobre en percentil 100: lectura de demanda, pero con pedidos de bienes duraderos planos.

**Curva de futuros**: backwardation (contado por encima de futuros) indica escasez física; contango, exceso.

## Qué lo mueve
OPEP+ (cuotas, cumplimiento), producción de EE.UU. (13 millones de barriles al día, el mayor productor), demanda china e india, inventarios (EIA semanal), dólar (inversa), geopolítica (Oriente Medio, Rusia), reserva estratégica (liberaciones de 2022), y posicionamiento especulativo (COT).

## Qué mueve
- IPC general (gasolina es el 3-4 % de la cesta; cada 10 $ en el crudo son ±0,2 pp de IPC en dos meses) y breakeven de inflación.
- IPP y márgenes de transporte, química, aerolíneas, consumo.
- Sector energía: beneficios y recompras; el índice HY (energía pesa un 10-15 % del HY).
- Balanza comercial de Europa, Japón e India; inflación importada.
- Política: gasolina cara es el precio más visible para el consumidor.

## Umbrales en el motor
Factor "petróleo" por percentil (≥ 80 caro). Carga +1 en energía, −1 en consumo discrecional (transporte, viajes, coches), −0,5 en industriales, materiales (química) y consumo básico (costes).

## Casuísticas relacionadas
→ [[petroleo-sube-por-oferta-vs-demanda]]: cómo distinguirlas y qué sectores reaccionan en cada caso.
→ [[spread-sube-por-petroleo]]: 2015-2016; el HY contaminado por energía.
→ [[petroleo-sobre-90-y-consumo]]: destrucción de demanda; retardo de 2-3 trimestres.

## Trampas de lectura
- El futuro continuo salta en los cambios de contrato; el precio de contado es ligeramente distinto.
- Abril de 2020: el futuro de mayo cotizó a −37 $ por falta de almacenamiento; la serie tiene un día absurdo.
- El efecto en la economía de EE.UU. es ambiguo desde 2015: es productor neto, así que un precio alto transfiere renta de consumidores a productores dentro del país, no fuera.

## Episodios
- **Junio 2008**: 147 $, con la recesión ya empezada (diciembre de 2007); cayó a 33 $ en diciembre de 2008.
- **Enero 2016**: 26 $ por el exceso de oferta del shale; spread HY a 890 pb, 100 quiebras de productores en EE.UU.
- **Marzo 2022**: 130 $ tras la invasión de Ucrania; IPC al 8,5 %; la Fed aceleró. El Brent llegó a 139 $.
- **Octubre 2026**: 89,6 $, percentil 91, −1,9 en el mes; caro, con cobre en máximos.

## Para profundizar
- EIA, informe semanal de inventarios y Short-Term Energy Outlook mensual: https://www.eia.gov/petroleum/
- OPEP, informe mensual del mercado del petróleo: https://www.opec.org/opec_web/en/publications/338.htm
- IEA, Oil Market Report (resumen gratuito): https://www.iea.org/reports/oil-market-report
- CFTC, posicionamiento especulativo en crudo (COT): https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
