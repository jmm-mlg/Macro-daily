---
tipo: indicador
id: PAYEMS
nombre: Nóminas no agrícolas (variación mensual)
bloque: Empleo
fuente: BLS, encuesta a establecimientos (CES), vía FRED (PAYEMS)
frecuencia: mensual
publicacion: primer viernes del mes, 8:30 ET (14:30 España); se adelanta al jueves si el viernes es festivo
en_el_motor: variación mensual en miles; peso 2 en crecimiento (> 150 / < 50, tendencia ±30); disparador < 0; headline
relacionados: [UNRATE, ICSA, JTSJOL, CES0500000003, regla-de-sahm, nominas-debiles-con-peticiones-bajas, informe-de-empleo]
actualizado: 2026-10-08
---

# Nóminas no agrícolas

El dato macro más seguido del mes: cuántos puestos de trabajo ha creado o destruido la economía de EE.UU. Marca el tono de la primera semana de cada mes y es el principal insumo de la Fed para el lado del empleo de su mandato.

## Qué mide
Variación mensual del número de empleados en nómina de empresas y administraciones (excluye agricultura, autónomos y empleo doméstico), según una encuesta a unos 120.000 establecimientos. El nivel absoluto es de unos 159 millones; lo que importa es la variación. Se publica junto con la tasa de paro (que viene de otra encuesta, a hogares), los salarios por hora y las horas trabajadas.

## Cómo se lee
| Variación mensual | Lectura |
| --- | --- |
| > 250k | Expansión fuerte; presión salarial (2021-2022) |
| 150-250k | Expansión sana |
| 50-150k | Economía al ralentí; cerca del "breakeven" (el ritmo que mantiene el paro estable, que con la inmigración actual se estima en 50-100k) |
| 0-50k | Estancamiento; la Fed se pone nerviosa |
| < 0 | Recesión probable; dos meses seguidos negativos han coincidido con recesión siempre desde 1950 |

Siempre con dos matices: la **revisión de los dos meses anteriores** (puede valer más que el dato nuevo: en 2024 las revisiones acumuladas restaron 800.000 empleos) y la **sorpresa frente al consenso** (que mueve el 2 años y la bolsa en los primeros minutos).

## Qué lo mueve
La demanda de trabajo (que depende de la demanda de bienes y servicios con 1-2 trimestres de retardo), la oferta (inmigración, participación), y factores estadísticos: el modelo de "nacimiento y muerte" de empresas, que infla el dato en los giros a la baja, y los ajustes estacionales.

## Qué mueve
- Expectativas de Fed y 2 años, en segundos.
- Renta disponible agregada (empleo × horas × salario) y por tanto el consumo.
- Sectores: un dato fuerte favorece a cíclicos y bancos; uno débil, a defensivos y bonos. Un dato muy fuerte puede ser malo para la bolsa si implica Fed más dura ("buenas noticias son malas noticias").

## Umbrales en el motor
Peso 2 en crecimiento: coincidente, no adelantado (las peticiones pesan 3 por eso). Umbrales 150k / 50k. Disparador en 0: la primera lectura negativa es el giro de ciclo.

## Casuísticas relacionadas
→ [[nominas-debiles-con-peticiones-bajas]]: no contratan, no despiden; octubre 2026.
→ [[buenas-noticias-son-malas-noticias]]: cuándo un dato fuerte hunde la bolsa.
→ [[revisiones-negativas-acumuladas]]: la señal lenta de 2024; el modelo de nacimiento y muerte.

## Trampas de lectura
- Error estándar de ±130.000: un dato de +29k y uno de +150k no son estadísticamente distintos. Mirar la media de 3 meses.
- Huelgas, huracanes y clima mueven el dato en decenas de miles un mes y lo devuelven al siguiente.
- La encuesta a empresas (nóminas) y la encuesta a hogares (paro) pueden decir cosas distintas durante meses; en los giros, la de hogares suele adelantarse.
- La revisión anual de referencia (benchmark, en febrero, preliminar en agosto) puede cambiar el año entero: la de agosto de 2024 restó 818.000.

## Episodios
- **Febrero 2020**: +273k; marzo: −700k; abril: −20,5 millones, la mayor destrucción de la historia. Cambio de régimen en un mes.
- **Enero 2023**: +517k frente a +185k esperados; el 2 años subió 20 pb en el día; la Fed subió en marzo pese a SVB.
- **Agosto 2024**: dato de julio de +114k con paro al 4,3 %: activó la regla de Sahm por una décima, el S&P 500 cayó un 6 % en tres sesiones y el Nikkei un 12 % en un día (deshacer del carry del yen). No hubo recesión; la regla dio su primer falso positivo probable.
- **Octubre 2026**: +29k (de +133k), percentil 12, con paro al 4,2 % y peticiones al percentil 1.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/PAYEMS
- BLS, informe de empleo completo y calendario: https://www.bls.gov/ces/
- Fed de Atlanta, "Jobs Calculator" (cuántos empleos mantienen el paro estable): https://www.atlantafed.org/chcs/calculator
- BLS, modelo de nacimiento y muerte de empresas: https://www.bls.gov/web/empsit/cesbd.htm
