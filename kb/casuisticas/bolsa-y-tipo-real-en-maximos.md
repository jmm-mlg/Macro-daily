---
tipo: casuistica
id: bolsa-y-tipo-real-en-maximos
nombre: Bolsa y tipo real en percentiles altos a la vez
señales: [^GSPC percentil ≥ 85, DFII10 percentil ≥ 85]
en_el_motor: señal cruzada "coincidencia" (same_direction) entre ^GSPC y DFII10; contribuye a tensión "alta" si liquidez ≤ −1 y riesgo ≥ +1
relacionados: [DFII10, DGS10, prima-de-riesgo, earnings-yield, episodio-2007, episodio-2022]
actualizado: 2026-10-08
---

# Bolsa y tipo real en percentiles altos a la vez

Cuando el S&P 500 y el tipo real a 10 años están los dos cerca de máximos de la década, la prima de riesgo de la renta variable está comprimida: el inversor cobra poco por asumir riesgo de beneficios frente a lo que le paga un bono sin riesgo. Históricamente uno de los dos cede, y en los casos en que ha cedido la bolsa lo ha hecho rápido.

## Cómo identificarla
- Percentil a 10 años del S&P 500 ≥ 85 y del tipo real (DFII10) ≥ 85, el mismo día. El motor lo marca como señal cruzada.
- Prima de riesgo (earnings yield adelantado del S&P 500 menos DFII10) por debajo del 1,5 %. En octubre de 2026: 4,0 % − 2,95 % ≈ 1 %.
- Confirmación: NFCI negativo (condiciones laxas) a pesar del tipo real alto; indica que la bolsa y los spreads están sosteniendo el apetito por el riesgo, no la Fed.

## Qué significa
Que el mercado descuenta crecimiento de beneficios suficiente para compensar un coste de capital alto. Es sostenible mientras los beneficios cumplan (2024-2025 con la IA) y deja de serlo en cuanto las revisiones de analistas giran a la baja o el tipo real da un salto adicional. No es una señal de giro inmediato: es una señal de asimetría. El potencial alcista queda limitado por la valoración y el bajista no.

## Qué reacciona y en qué plazo
| Activo o sector | Reacción típica cuando la tensión se resuelve con caída de la bolsa |
| --- | --- |
| Growth sin beneficios, software en pérdidas, biotech | Primeros y más fuertes: −30/−50 % en 2022 |
| REITs, utilities | −15/−25 %, con retardo de semanas |
| Calidad con caja neta y pricing power | −5/−15 %; recuperan primero |
| Energía, materias primas | Depende de la causa: si el tipo real sube por inflación, aguantan |
| Bonos largos | Suben cuando la bolsa cae por crecimiento; caen si cae por tipos (2022: cayeron los dos) |

Cuando se resuelve con caída del tipo real (la Fed señala recortes, el crecimiento se enfría sin recesión), la bolsa suele seguir subiendo con rotación hacia duración: 2019, noviembre de 2023.

## Qué hacer (en términos del embudo)
- Filtro 1: exposición agregada en la banda baja del régimen; no aumentar aunque un sector concreto esté favorecido.
- Filtro 2 y 3: dentro de los sectores favorecidos, elegir calidad (margen, caja) sobre crecimiento; vetar growth sin beneficios.
- Filtro 4: entradas solo en retrocesos; no perseguir máximos.
- Nivel 6: stops más cercanos (1,5 ATR en lugar de 2) y mitad de tamaño; riesgo abierto total ≤ 3 % en lugar de 5 %.
- Vigilar: el disparador del 10 años (5,50 %) y las revisiones de analistas del S&P 500 agregadas; el giro de las revisiones suele preceder a la resolución.

## Qué la invalida
- Que el tipo real baje de forma ordenada (la Fed abre la puerta a recortes con inflación contenida): la tensión se disuelve sin daño.
- Que los beneficios suban más del 10 % interanual con revisiones al alza: la prima se recompone por el lado del earnings yield.

## Episodios
- **Junio 2007**: S&P 500 en máximos, tipo real al 2,7 %, spread HY en mínimos. Resolución: caída de la bolsa (−57 % hasta marzo de 2009) con el tipo real cayendo por recesión.
- **Enero 2022**: S&P 500 en máximos con tipo real en −1 %: no aplicaba la casuística; fue la subida posterior del tipo real (+270 pb en el año) la que la creó y la resolvió a la vez: −25 % con beneficios planos.
- **Julio-octubre 2023**: S&P 500 en percentil alto, tipo real cruzando el 2,5 %. Resolución: −10 % de la bolsa y luego caída del tipo real cuando la Fed señaló el fin de las subidas; la bolsa recuperó en dos meses.
- **Octubre 2026**: caso abierto. S&P 500 y DFII10 en percentil 100, prima ≈ 1 %, revisiones de analistas aún al alza (Nvidia 43/1, Exxon 6/0). Mientras las revisiones aguanten, la casuística no se resuelve.

## Para profundizar
- Damodaran, "Equity Risk Premiums: Determinants, Estimation and Implications" (actualización anual, SSRN, gratuito): https://papers.ssrn.com/ (buscar el título)
- Asness, "Fight the Fed Model" (AQR, 2003; crítica al modelo de la Fed): https://www.aqr.com/Insights/Research
- Fed, Monetary Policy Report, sección de valoraciones (semestral): https://www.federalreserve.gov/monetarypolicy/mpr_default.htm
