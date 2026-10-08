---
tipo: indicador
id: JTSJOL
nombre: Vacantes de empleo (JOLTS)
bloque: Empleo
fuente: BLS, Job Openings and Labor Turnover Survey, vía FRED (JTSJOL)
frecuencia: mensual
publicacion: primer martes del mes, 10:00 ET, con datos de dos meses atrás
en_el_motor: nivel; solo panel; en el calendario
relacionados: [UNRATE, PAYEMS, ICSA, CES0500000003, curva-de-beveridge, vacantes-por-parado, tasa-de-renuncias]
actualizado: 2026-10-08
---

# Vacantes de empleo (JOLTS)

Cuántos puestos están sin cubrir. Junto con la tasa de renuncias (quits) del mismo informe, mide la tensión del mercado laboral desde el lado de la demanda, y es el indicador que la Fed usó en 2022-2024 para argumentar que la inflación salarial podía bajar sin subir el paro.

## Qué mide
Número de vacantes abiertas el último día hábil del mes, según encuesta a 21.000 establecimientos. El informe incluye también contrataciones, renuncias voluntarias, despidos y separaciones totales. Las renuncias son el componente más informativo: la gente deja su empleo cuando confía en encontrar otro mejor.

## Cómo se lee
- **Vacantes por parado** (JTSJOL / número de parados): el ratio que cita la Fed. > 1,5 muy tenso (2022: 2,0); 1,0-1,2 equilibrio; < 0,8 holgura.
- **Tasa de renuncias**: > 2,8 % tensión y presión salarial; 2,0-2,3 % normal; < 2,0 % miedo (los trabajadores no se mueven).
- **Despidos** (layoffs): el componente que adelanta a las peticiones; cuando sube de 1,8 a más de 2,0 millones, las peticiones suben un mes después.
- **Tendencia**: vacantes cayendo desde máximos con paro estable es normalización (2023-2024); vacantes cayendo con paro subiendo es deterioro.

## Qué lo mueve
Demanda de trabajo (beneficios, confianza), coste del trabajo, y la facilidad de contratar (en 2022, con falta de candidatos, las vacantes se acumulaban sin cubrir). Las ofertas de empleo en Indeed (diarias) adelantan a JOLTS dos meses.

## Qué mueve
- Salarios, con retardo: la curva de Beveridge (vacantes frente a paro) explica la presión salarial.
- La lectura de la Fed sobre si el mercado laboral se enfría "de forma ordenada" (menos vacantes) o "desordenada" (más paro).

## Umbrales en el motor
Solo panel: llega con dos meses de retraso y su información ya está en las peticiones, las nóminas y los salarios. Se mantiene por la tasa de renuncias y los despidos, que conviene mirar en el informe completo.

## Casuísticas relacionadas
→ [[vacantes-caen-sin-subir-el-paro]]: el "aterrizaje suave" de 2023-2024; por qué funcionó (curva de Beveridge vertical).
→ [[renuncias-en-minimos]]: trabajadores que no se mueven; precede a salarios flojos y consumo cauto.

## Trampas de lectura
- Tasa de respuesta de la encuesta por debajo del 35 % desde 2022; revisiones grandes.
- Las vacantes pueden ser "fantasma" (ofertas publicadas sin intención real de contratar); Indeed y LinkedIn dan una lectura más limpia.
- El dato llega muy tarde: el JOLTS de octubre sale en diciembre.

## Episodios
- **Marzo 2022**: 12,0 millones de vacantes, 2,0 por parado, máximo histórico; renuncias al 3,0 %. El argumento de la Fed para subir sin miedo al paro.
- **2023-2024**: de 10 a 7,5 millones sin que el paro subiera del 3,5 % al 4,2 % hasta mediados de 2024: la curva de Beveridge se movió en vertical, como argumentó Waller (Fed) en 2022.
- **Octubre 2026**: 7,08 millones, −256.000, percentil 36; en torno a 1,0 por parado. Equilibrio, con tendencia a la baja.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/JTSJOL y renuncias: https://fred.stlouisfed.org/series/JTSQUR
- BLS, informe JOLTS completo: https://www.bls.gov/jlt/
- Indeed Hiring Lab, ofertas diarias (adelantado): https://www.hiringlab.org/
- Waller y Figura, "What does the Beveridge curve tell us about the likelihood of a soft landing?" (Fed, 2022): https://www.federalreserve.gov/econres/notes/feds-notes/
