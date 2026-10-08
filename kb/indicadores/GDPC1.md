---
tipo: indicador
id: GDPC1
nombre: PIB real de EE.UU.
bloque: Actividad
fuente: BEA vía FRED (GDPC1, encadenado 2017)
frecuencia: trimestral
publicacion: estimación adelantada a finales del mes siguiente al trimestre, 8:30 ET; segunda y tercera estimación en los dos meses siguientes
en_el_motor: variación trimestral anualizada; peso 1 en crecimiento (> 2,5 / < 1,0, tendencia ±0,3); headline
relacionados: [GDPNow, RSAFS, INDPRO, recesion-tecnica, nber, PIB-nominal]
actualizado: 2026-10-08
---

# PIB real de EE.UU.

La medida oficial del tamaño de la economía. Es el dato más completo y el más retrasado: sale un mes después del trimestre, se revisa dos veces, y para cuando se conoce el mercado ya lo ha descontado. Su valor para decidir está en la composición, no en la cifra.

## Qué mide
Valor de todos los bienes y servicios finales producidos en EE.UU., a precios constantes, anualizado. El email muestra la variación trimestral anualizada (la convención americana: un 0,55 % trimestral se publica como 2,2 %). Composición típica: consumo 68 %, inversión 18 %, gasto público 17 %, exportaciones netas −3 %.

## Cómo se lee
| Trimestral anualizado | Lectura |
| --- | --- |
| > 3 % | Por encima del potencial (estimado en 1,8-2,0 %); presión sobre precios |
| 2-3 % | Expansión sólida |
| 1-2 % | Débil; vulnerable |
| 0-1 % | Estancamiento |
| < 0 | Contracción; dos seguidos = "recesión técnica" (no es la definición oficial, que la da el NBER con empleo, renta y producción) |

Más útil que el total: **ventas finales a compradores privados domésticos** (consumo + inversión fija privada), que elimina inventarios, comercio exterior y gasto público, los tres componentes más volátiles. Es la "demanda subyacente".

## Qué lo mueve
Consumo (renta real, empleo, ahorro), inversión empresarial (beneficios, tipos, confianza; en 2024-2026 el capex en centros de datos ha sumado 0,5-1 pp por sí solo), vivienda (hipotecas), gasto público (déficit), inventarios (muy volátiles, pueden sumar o restar 2 pp en un trimestre), exportaciones netas (dólar, demanda global).

## Qué mueve
- Poco el día del dato, salvo sorpresa grande, porque GDPNow lo anticipa.
- Beneficios empresariales agregados: el PIB nominal (real + inflación) crece de forma parecida a las ventas del S&P 500.
- La narrativa de recesión o no recesión, que condiciona el apetito por el riesgo durante semanas.

## Umbrales en el motor
Peso 1, el mínimo, por su retraso. Umbrales 2,5 / 1,0 en torno al potencial. GDPNow (nivel 4 de la guía) es el sustituto en tiempo real.

## Casuísticas relacionadas
→ [[recesion-tecnica-sin-recesion]]: 2022, dos trimestres negativos con el empleo creciendo; qué hizo el mercado.
→ [[pib-fuerte-por-inventarios]]: cuando la cifra engaña; mirar ventas finales.
→ [[capex-de-ia-sostiene-el-pib]]: 2025-2026; concentración del crecimiento en un componente.

## Trampas de lectura
- La estimación adelantada se revisa, a veces mucho (el Q1 2024 pasó de 1,6 % a 1,3 %); el dato que importa es el tercero.
- La anualización multiplica el ruido por cuatro.
- El PIB nominal es lo relevante para beneficios y deuda; con inflación al 3,7 %, un PIB real del 2,2 % es un nominal del 6 %, que sostiene ventas empresariales aunque el real sea mediocre.
- La "renta interior bruta" (GDI) mide lo mismo por el lado de las rentas y a veces discrepa durante trimestres; cuando discrepa, el promedio de ambas es mejor guía.

## Episodios
- **Q2 2020**: −28 % anualizado (−8 % trimestral), la mayor caída de la historia; Q3: +35 %. Las anualizaciones se volvieron absurdas.
- **Q1-Q2 2022**: −1,6 % y −0,6 %, "recesión técnica" sin recesión: el empleo creció 400.000 al mes. El NBER no la declaró. El S&P 500 hizo suelo en octubre.
- **Q3 2023**: +4,9 % con la Fed al 5,5 %; el mercado lo leyó como "tipos más altos por más tiempo" y el 10 años tocó el 5 %.
- **Q2 2026** (dato de octubre): 2,22 %, −0,27, percentil 28; desacelerando pero por encima del 1 %.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/GDPC1 y ventas finales a compradores privados: https://fred.stlouisfed.org/series/LB0000031Q020SBEA
- BEA, publicación trimestral con tablas de contribución por componente: https://www.bea.gov/data/gdp/gross-domestic-product
- GDPNow (Fed de Atlanta): https://www.atlantafed.org/cqer/research/gdpnow
- NBER, comité de fechado de ciclos (la definición oficial de recesión): https://www.nber.org/research/business-cycle-dating
