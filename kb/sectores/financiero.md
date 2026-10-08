---
tipo: sector
id: financiero
nombre: Financiero
gics: 40
peso: "S&P 500 ~13 % · Stoxx 600 ~20 %"
en_el_motor: "matriz: goldilocks 0, reflación +1, estanflación −1, desinflación −1 · factores: curva +1, crédito −1"
bellwethers: [JPM, BNP.PA, ALV.DE, V]
relacionados: [T10Y2Y, BAMLH0A0HYM2, DFF, ECBDFR, curva-y-margen-bancario, credito-a-actividad, bancos-y-curva]
actualizado: 2026-10-08
---

# Financiero

Bancos, aseguradoras, gestoras, bolsas y pagos. Es el sector que abre cada temporada de resultados (JPMorgan, el segundo viernes tras el trimestre) y el que mejor lee el crédito: si los bancos aumentan provisiones, el consumidor y las empresas están empezando a fallar.

## Qué incluye
Bancos (margen de interés, provisiones), mercados de capitales (comisiones de banca de inversión y trading, gestión de activos), seguros (primas, siniestralidad, rendimiento de la cartera), pagos (volumen de transacciones) y finanzas al consumo (tarjetas, morosidad). En Europa, bancos y seguros pesan mucho más que en EE.UU.; en EE.UU., pagos y gestoras.

## Drivers macro
| Driver | Efecto | Serie del motor |
| --- | --- | --- |
| Pendiente de la curva | Margen de intermediación: prestan a largo, se financian a corto | T10Y2Y |
| Nivel de tipos cortos | Rendimiento del efectivo y los depósitos; favorable hasta que la morosidad sube | DFF, ECBDFR |
| Spreads de crédito | Provisiones y valor de las carteras de bonos | BAMLH0A0HYM2 |
| Actividad y empleo | Morosidad con 2-4 trimestres de retardo | ICSA, UNRATE |
| Volatilidad | Ingresos de trading (sube con el VIX); banca de inversión (baja con el VIX) | ^VIX |
| Bolsa | Comisiones de gestoras y bolsas; servicios financieros imputados del PCE | ^GSPC |

## Métricas que deciden sus resultados
- **Margen de interés neto (NIM)** y **ingresos netos por intereses (NII)**: la guía de NII para el año es lo que mueve la acción.
- **Provisiones para insolvencias** y **morosidad** (NPL, tarjetas con más de 90 días): el primer aviso del ciclo.
- **CET1** (capital): por encima del 12-13 % permite recompras.
- **Coste del pasivo** (beta de depósitos): cuánto del tipo oficial traslada a los depósitos.
- Aseguradoras: **ratio combinado** (< 100 % = beneficio técnico) y rendimiento de la cartera.
- Pagos: **volumen de pagos** y gasto transfronterizo (lectura de viajes y consumo).

## Comportamiento por régimen
| Régimen | Sesgo base | Qué pasa |
| --- | --- | --- |
| Goldilocks | 0 | Crédito sano, comisiones; sin viento de cola de tipos |
| Reflación | +1 | NII al alza con curva empinando; el riesgo pasa a provisiones |
| Estanflación | −1 | Morosidad sube con la curva aún alta: lo peor para el margen de riesgo |
| Desinflación recesiva | −1 | Curva plana, provisiones altas; esperar al pivot |
| Mixto | 0 | Mandan la curva (margen) y el crédito (provisiones) |

## Bellwethers y qué mirar
- **JPMorgan** (abre la temporada): guía de NII, provisiones de tarjetas, comentario de Dimon sobre el consumidor. Es la lectura macro más citada del trimestre.
- **BNP Paribas** y **Santander**: margen en Europa (BCE), coste de riesgo, exposición a España y Latinoamérica.
- **Allianz**: siniestralidad y catástrofes; rendimiento de la cartera con tipos altos.
- **Visa**: volumen de pagos y transfronterizo; la lectura de consumo global más limpia.
- Para el consumidor de renta baja: **Capital One** (morosidad en tarjetas) y **Wells Fargo**.

## Factores en el motor
Curva +1 (empinamiento > 15 pb en el mes), crédito −1 (HY > 450 pb o +50 pb en el mes). Sin sensibilidad a duración, petróleo, dólar ni cobre.

## Trampas de lectura
- Tipos altos son buenos para los bancos hasta que dejan de serlo: 2023 (SVB) mostró que las carteras de bonos pierden valor y los depósitos se van; 2007 que el crédito puede estallar con tipos altos.
- Las provisiones son discrecionales: los bancos las suben "por prudencia" en buenos tiempos y las liberan en malos (CECL en EE.UU. desde 2020 las hace más procíclicas).
- Los bancos europeos cotizan con descuento estructural sobre valor en libros; el múltiplo no es comparable con EE.UU.

## Episodios
- **2006-2007**: curva invertida, HY en mínimos, beneficios récord; los bancos cayeron un 80 % en 2008.
- **Marzo 2023**: SVB; el KBW Banks cayó un 25 % en dos semanas; los grandes recuperaron, los regionales no.
- **2022-2024**: los bancos europeos subieron un 60 % con el BCE del −0,5 % al 4 %: el mejor ciclo de margen de su historia.
- **Octubre 2026**: sesgo 0 (régimen Mixto), curva empinando +6 pb (no activa el factor), HY +44 pb (tampoco). JPMorgan publica el 13 de octubre.

## Para profundizar
- Fed, informe de supervisión y regulación bancaria (semestral) y resultados del stress test: https://www.federalreserve.gov/publications/supervision-and-regulation-report.htm
- FDIC, Quarterly Banking Profile (margen, morosidad del sistema): https://www.fdic.gov/quarterly-banking-profile
- BCE, encuesta de préstamos bancarios (BLS, trimestral): https://www.ecb.europa.eu/stats/ecb_surveys/bank_lending_survey/html/index.en.html
