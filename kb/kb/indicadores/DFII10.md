---
tipo: indicador
id: DFII10
nombre: Tipo real a 10 años (TIPS)
bloque: Tipos
fuente: Tesoro de EE.UU. vía FRED (serie DFII10)
frecuencia: diaria
publicacion: cada día hábil, cierre de mercado EE.UU.
en_el_motor: alerta > 2,0 %; factor "duración" (> 2,0 activo, < 1,0 inverso); peso 3 (invertido) en el score de liquidez
relacionados: [DGS10, T10YIE, prima-de-riesgo, duracion, tipo-real-y-multiplos, bolsa-y-tipo-real-en-maximos]
actualizado: 2026-10-08
---

# Tipo real a 10 años (TIPS)

Es el coste del dinero a largo plazo descontada la inflación esperada, y por tanto la tasa a la que el mercado descuenta los beneficios futuros. Es la variable que más explica los múltiplos de la bolsa.

## Qué mide
Rendimiento de los bonos del Tesoro de EE.UU. a 10 años indexados a la inflación (TIPS). Como el principal se ajusta con el IPC, el rendimiento que cotizan es el tipo "real". Se cumple aproximadamente: tipo nominal a 10 años (DGS10) = tipo real (DFII10) + inflación esperada (T10YIE). Existe desde 1997; antes solo hay estimaciones.

## Cómo se lee
| Nivel | Lectura | Contexto histórico |
| --- | --- | --- |
| < 0 % | Represión financiera; todo activo con flujo futuro vale más | 2012-2013 y 2020-2021 |
| 0-1 % | Neutral | Mayor parte de 2015-2019 |
| 1-2 % | Restrictivo; los múltiplos dejan de expandirse | 2023-2024 |
| > 2 % | Muy restrictivo; el bono compite de frente con la bolsa | 2006-2007, oct-2023, 2026 |

Tendencia: una subida de 50 pb en un mes es un shock (oct-2008, mar-2020, sep-2022, sep-2026). Lo relevante no es solo el nivel sino la velocidad: el mercado absorbe un 2 % si llega en un año, no si llega en dos meses.

## Qué lo mueve
1. Expectativas sobre el tipo de la Fed a medio plazo (el componente principal).
2. Prima de plazo: compensación por incertidumbre, ligada a la oferta de deuda del Tesoro y al déficit.
3. Demanda extranjera y de fondos de pensiones; ventas de reservas (China, Japón) la elevan.
4. Compras o ventas de bonos de la Fed: QE lo baja, QT lo sube.
Retardo: reacciona en minutos a datos de inflación y empleo y a discursos de la Fed.

## Qué mueve
- **Múltiplos de renta variable**: regla orientativa, el PER adelantado del S&P 500 cae en torno a 1 punto por cada 50 pb sostenidos de subida. Afecta más a quien tiene los beneficios más lejos: growth sin beneficios, biotech, software en pérdidas.
- **Oro**: relación inversa muy estable; el oro no paga cupón y su coste de oportunidad es el tipo real. Cuando sube con el tipo real alto (2024-2026) hay otra fuerza: bancos centrales comprando o refugio.
- **Dólar**: relación directa; el diferencial de tipos reales atrae capital.
- **REITs y utilities**: inversa, porque se valoran como un bono con crecimiento.
- **Bancos**: ambigua; alto por crecimiento les favorece, alto por prima de plazo les penaliza por la cartera de bonos.

## Umbrales en el motor
- Alerta en 2,0 %: desde que existen los TIPS, por encima de ese nivel la prima de riesgo de la renta variable ha estado por debajo de su media y los retornos a 12 meses han sido inferiores a la media.
- Factor "duración" activo por encima de 2,0 (carga −1 en inmobiliario, utilities, tecnología y comunicación; −0,5 en discrecional, salud, básico e industriales).
- Peso 3 en el score de liquidez, invertido: es la variable que mejor resume si el dinero ayuda o estorba.

## Casuísticas relacionadas
→ [[bolsa-y-tipo-real-en-maximos]]: cuando ambos están en percentil alto a la vez, la prima de riesgo se comprime y uno de los dos cede.
→ [[tipo-real-sube-por-crecimiento-o-por-prima]]: el mismo nivel significa cosas opuestas según la causa.
→ [[oro-cae-con-inflacion-alta]]: el oro sigue al tipo real, no a la inflación.

## Trampas de lectura
- El tipo real de mercado no es el "ex post" (nominal menos inflación publicada): es nominal menos inflación esperada. Con IPC al 3,7 % y breakeven al 2,4 %, el tipo real ex post es mucho menor que el cotizado.
- Los TIPS tienen una prima de liquidez propia que en crisis (mar-2020) distorsiona la lectura durante semanas.
- Un tipo real alto con GDPNow por encima del 3 % es crecimiento; con GDPNow por debajo del 1 % es prima de plazo, y eso es más peligroso para la bolsa.

## Episodios
- **Mayo-julio 2013 (taper tantrum)**: de −0,7 % a +0,6 % en diez semanas cuando Bernanke insinuó reducir el QE. S&P 500 −6 % en un mes, oro −20 % en el trimestre, emergentes −15 %. La velocidad importa más que el nivel.
- **2022**: de −1,0 % en enero a +1,7 % en octubre. Nasdaq −33 % en el año con beneficios planos: toda la caída fue compresión de múltiplos; software sin beneficios −60/−70 %.
- **Octubre 2023**: cruza el 2,5 % por primera vez desde 2007; el S&P 500 cae un 10 % desde julio y rebota en cuanto la Fed señala el fin de las subidas (noviembre). El pico del tipo real coincide con el suelo de la bolsa.
- **2026**: 2,95 % en octubre con el S&P 500 en máximos; prima de riesgo en torno al 1 %. Caso abierto.

## Para profundizar
- Serie y notas: https://fred.stlouisfed.org/series/DFII10
- Fed de Cleveland, expectativas de inflación y tipos reales (modelo): https://www.clevelandfed.org/indicators-and-data/inflation-expectations
- Damodaran, primas de riesgo históricas (actualizado cada enero): https://pages.stern.nyu.edu/~adamodar/
