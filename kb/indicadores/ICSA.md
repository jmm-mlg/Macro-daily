---
tipo: indicador
id: ICSA
nombre: Peticiones iniciales de subsidio de desempleo
bloque: Empleo
fuente: Departamento de Trabajo (ETA) vía FRED (ICSA, desestacionalizada)
frecuencia: semanal
publicacion: jueves, 8:30 ET (14:30 España), con datos de la semana que termina el sábado anterior
en_el_motor: nivel; alerta > 300.000; peso 3 (invertido) en crecimiento (percentil ≥ 70 / ≤ 30, tendencia ±10.000); disparador > 240.000; en el calendario
relacionados: [PAYEMS, UNRATE, CCSA, JTSJOL, nominas-debiles-con-peticiones-bajas, peticiones-superan-umbral]
actualizado: 2026-10-08
---

# Peticiones iniciales de desempleo

Cuántas personas han pedido por primera vez el subsidio de paro esa semana: es decir, cuántos despidos ha habido. Es el dato más adelantado y más frecuente del mercado laboral, y por eso pesa más que las nóminas en el motor.

## Qué mide
Solicitudes iniciales de subsidio estatal de desempleo, suma de los 50 estados, desestacionalizada. Semanal, con una semana de retraso. Se publica junto a las peticiones continuadas (CCSA: cuántos siguen cobrando), que miden la dificultad de encontrar empleo nuevo.

## Cómo se lee
| Nivel (media de 4 semanas) | Lectura |
| --- | --- |
| < 220.000 | Mercado laboral muy tenso; mínimos históricos (2022-2023: 190.000-210.000) |
| 220.000-260.000 | Normal en expansión |
| 260.000-300.000 | Deterioro; despidos en aumento |
| > 300.000 | Recesión en marcha (históricamente, cada recesión ha superado los 350.000) |
| > 400.000 | Recesión profunda |

Con la media de 4 semanas, nunca con el dato aislado. Y mirando **continuadas**: si las iniciales están bajas pero las continuadas suben (2024-2026), hay pocos despidos pero cuesta encontrar empleo; es la "economía congelada" (low hire, low fire).

## Qué lo mueve
Despidos, que dependen de los beneficios empresariales con 1-2 trimestres de retardo y de la confianza empresarial. Distorsiones: semanas con festivo, clima extremo (huracanes, tormentas de nieve), huelgas (los huelguistas no cuentan pero los afectados indirectos sí), fraude estatal (2023, Ohio), y cambios en los factores estacionales.

## Qué mueve
- La lectura de la Fed sobre el empleo entre informes mensuales.
- El 2 años el jueves a las 14:30, cuando sorprende.
- Es el dato que marca el giro de régimen de "no contratan" a "despiden".

## Umbrales en el motor
Peso 3 en crecimiento, el máximo, invertido (más peticiones = peor). Umbrales por percentil (≥ 70 negativo, ≤ 30 positivo) porque el nivel "normal" ha cambiado con el tamaño de la población activa. Disparador en 240.000 (desde los 197.000 actuales, un +20 % es el cambio de fase) y alerta en 300.000 (recesión).

## Casuísticas relacionadas
→ [[nominas-debiles-con-peticiones-bajas]]: la situación de 2026; cómo se resuelve históricamente.
→ [[peticiones-superan-umbral]]: cruce de 240.000-260.000 desde mínimos; plazo hasta la recesión.
→ [[continuadas-suben-con-iniciales-estables]]: economía congelada; implicaciones para consumo.

## Trampas de lectura
- Un dato semanal es ruido; la media de 4 semanas es la señal.
- Las semanas de Acción de Gracias, Navidad y 4 de julio tienen ajustes estacionales grandes y a menudo fallan.
- El nivel en 2022-2026 ha sido anormalmente bajo por la escasez de trabajadores tras la pandemia; el umbral de recesión podría ser más bajo que el histórico de 350.000.

## Episodios
- **Marzo 2020**: de 211.000 a 3,3 millones en una semana y 6,6 millones a la siguiente, según se publicó (la serie revisada por factores estacionales muestra 2,9 y 5,9 millones); la serie no había superado los 700.000 nunca.
- **Septiembre 2007**: la media de 4 semanas pasó de 310.000 a 330.000; la recesión empezó en diciembre. Las peticiones avisaron tres meses antes que las nóminas.
- **Julio 2024**: pico de 250.000 (huracán Beryl, Texas) que contribuyó al pánico de la regla de Sahm; volvió a 230.000 en tres semanas.
- **Octubre 2026**: 197.000, percentil 1, estables: las empresas no despiden a pesar de las nóminas débiles.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/ICSA y continuadas: https://fred.stlouisfed.org/series/CCSA
- Departamento de Trabajo, publicación semanal con detalle por estado: https://www.dol.gov/ui/data.pdf
