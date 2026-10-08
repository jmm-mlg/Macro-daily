---
tipo: sector
id: discrecional
nombre: Consumo discrecional
gics: 25
peso: "S&P 500 ~10 % · Stoxx 600 ~10 %"
en_el_motor: "matriz: goldilocks +1, reflación 0, estanflación −2, desinflación −1 · factores: petróleo −1, hipoteca −1, crédito −1, duración −0,5"
bellwethers: [AMZN, TSLA, MCD, HD, MC.PA, ITX.MC, VOW3.DE]
relacionados: [RSAFS, UMCSENT, CES0500000003, MORTGAGE30US, CL=F, efecto-riqueza, consumo-fuerte-con-confianza-baja]
actualizado: 2026-10-08
---

# Consumo discrecional

Lo que la gente compra cuando puede, no cuando debe: coches, ropa, restaurantes, viajes, lujo, muebles, comercio electrónico. Es el sector que más depende de la renta real, del crédito y de la confianza, y el que se divide en dos consumidores distintos: el de renta alta (lujo, viajes, Amazon) y el de renta baja (comida rápida, descuento, coches financiados).

## Qué incluye
Automóviles y componentes (Tesla, GM, Volkswagen, Mercedes, Stellantis, Michelin: financiación y precio de la energía), lujo (LVMH, Hermès, Richemont: consumidor chino y renta alta), textil (Nike, Inditex, adidas), restauración y ocio (McDonald's, Starbucks, Booking, IHG), mejora del hogar (Home Depot: vivienda), comercio amplio y e-commerce (Amazon, Zalando). Amazon pesa un 40 % del sector en EE.UU. y su negocio de nube (AWS) no es consumo.

## Drivers macro
| Driver | Efecto | Serie del motor |
| --- | --- | --- |
| Renta real (salarios − inflación) | Capacidad de gasto; con retardo de 2-3 trimestres | CES0500000003, CPIAUCSL |
| Empleo | Miedo al paro reduce gasto antes que el paro | ICSA, PAYEMS |
| Gasolina | Renta disponible del consumidor medio; cada 1 $ en el galón son ~100.000 M$ al año | CL=F |
| Hipotecas y vivienda | Mejora del hogar, muebles, electrodomésticos; efecto cerrojo | MORTGAGE30US, PERMIT |
| Crédito al consumo | Coches, tarjetas; morosidad | BAMLH0A0HYM2 |
| Bolsa (efecto riqueza) | Consumidor de renta alta: lujo, viajes | ^GSPC |
| China | Lujo (30-40 % de las ventas de LVMH) y coches alemanes | fuente externa |

## Métricas que deciden sus resultados
- **Ventas comparables** (same-store sales) y **tráfico frente a ticket**: si el ticket sube y el tráfico baja, es inflación, no demanda.
- **Margen bruto**: la medida de pricing power; los descuentos lo erosionan.
- **Inventarios** frente a ventas: inventarios creciendo más que ventas precede a rebajas (textil, 2022).
- Coches: **unidades**, **incentivos**, **precio medio**, financiación (tipo medio del préstamo).
- Lujo: crecimiento orgánico por región (Asia, Europa, Américas).
- Amazon: AWS aparte; en retail, ventas de terceros y publicidad.

## Comportamiento por régimen
| Régimen | Sesgo base | Qué pasa |
| --- | --- | --- |
| Goldilocks | +1 | Consumo fuerte con crédito barato: el mejor entorno |
| Reflación | 0 | Renta baja retrocede (restauración rápida, descuento lo anuncian), renta alta y lujo aguantan |
| Estanflación | −2 | El peor: costes arriba, demanda abajo |
| Desinflación recesiva | −1 | Demanda débil; solo descuento y valor |
| Mixto | 0 | Consumo en disputa: ventas fuertes pero confianza baja; sensible a petróleo e hipotecas |

## Bellwethers y qué mirar
- **Amazon**: ventas de retail y, sobre todo, AWS y capex; comentario sobre el consumidor.
- **McDonald's**: tráfico de renta baja; cuando McDonald's dice que el cliente de menos de 45.000 $ reduce visitas, el consumo de renta baja está en problemas (2024).
- **Home Depot**: proyectos grandes frente a pequeños; es la lectura de vivienda.
- **LVMH** (solo ventas en Q1 y Q3): consumidor chino y lujo global.
- **Inditex** (cierre enero; resultados mar/jun/sep/dic): el mejor operador textil; ventas en moneda constante.
- **Tesla** y **Volkswagen**: precios, márgenes, China; la transición eléctrica y los aranceles.

## Factores en el motor
Petróleo −1, hipoteca −1, crédito −1, duración −0,5. Es el sector con más cargas negativas: todo lo que encarece la vida o el crédito le resta.

## Trampas de lectura
- "El consumidor aguanta" es una media: el 20 % superior de renta es la mitad del consumo y aguanta por bolsa y vivienda; el 40 % inferior está apretado desde 2023. Mirar McDonald's y Dollar General, no Amazon.
- Las ventas minoristas son nominales; con inflación del 3-4 % un crecimiento del 3 % es cero real.
- Amazon distorsiona el sector: su peso y AWS hacen que el ETF sectorial (XLY) sea en parte una apuesta de nube.
- El lujo es un sector aparte: depende de China y de la riqueza, no del consumo medio.

## Episodios
- **2008**: −35 %; las ventas de coches cayeron de 16 a 9 millones anuales; GM y Chrysler quebraron.
- **2020-2021**: +60 % con los cheques de estímulo y el ahorro forzado; el exceso de ahorro (2 billones) sostuvo el consumo hasta 2023.
- **2022**: −37 %, el peor sector junto a comunicación, por el tipo real y la inflación; Amazon −50 %.
- **Octubre 2026**: sesgo −2 (petróleo, hipoteca, tipo real); ventas minoristas +1,1 % con Michigan en percentil 5 y salarios reales negativos.

## Para profundizar
- Fed de Nueva York, deuda y crédito de los hogares (morosidad por tipo y edad): https://www.newyorkfed.org/microeconomics/hhdc
- Bank of America Institute, datos de gasto con tarjeta (mensual, gratuito): https://institute.bankofamerica.com/
- Censo, ventas minoristas (grupo de control): https://www.census.gov/retail/index.html
