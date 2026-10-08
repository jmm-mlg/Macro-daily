---
tipo: indicador
id: UNRATE
nombre: Tasa de paro
bloque: Empleo
fuente: BLS, encuesta a hogares (CPS), vía FRED (UNRATE)
frecuencia: mensual
publicacion: con las nóminas, primer viernes, 8:30 ET
en_el_motor: nivel; solo panel y disparador > 4,5 % (regla de Sahm); headline
relacionados: [PAYEMS, ICSA, JTSJOL, regla-de-sahm, participacion, nairu]
actualizado: 2026-10-08
---

# Tasa de paro

Porcentaje de la población activa que busca empleo y no lo encuentra. Es el indicador más retrasado del ciclo (sube cuando la recesión ya ha empezado) y a la vez el más fiable para confirmarla: la regla de Sahm, basada en él, no ha fallado desde 1970 salvo, probablemente, en 2024.

## Qué mide
Parados (sin empleo, disponibles y buscando activamente en las últimas cuatro semanas) sobre población activa (ocupados más parados), según la encuesta mensual a 60.000 hogares. No cuenta a quien ha dejado de buscar (eso lo recoge la tasa de participación) ni a quien trabaja a tiempo parcial por no encontrar jornada completa (eso está en la U-6).

## Cómo se lee
- **Nivel frente al NAIRU** (paro de equilibrio, estimado por la CBO en torno al 4,2-4,4 %): por debajo, mercado laboral tenso e inflación salarial; por encima, holgura.
- **Regla de Sahm**: media de tres meses de la tasa de paro 0,5 pp por encima del mínimo de los doce meses anteriores. Señal de recesión en curso (no futura) con acierto perfecto 1970-2020. En 2024 se activó por una décima (4,3 % en julio) sin recesión posterior, probablemente por el aumento de la oferta de trabajo por inmigración, que sube el paro sin destrucción de empleo.
- **Velocidad**: el paro sube despacio en expansión (una décima cada varios meses) y rápido en recesión (una décima al mes o más). Tres subidas consecutivas de una décima son señal de alarma.

## Qué lo mueve
Destrucción de empleo (con retardo respecto a las peticiones), participación (más gente buscando sube el paro sin que empeore el empleo), inmigración, y la estacionalidad de graduaciones (junio-julio).

## Qué mueve
- La Fed: el lado del empleo de su mandato se mide con esta tasa; las proyecciones del FOMC dan la senda que tolera.
- Consumo con retardo: el miedo al paro reduce el gasto antes que el paro mismo.
- Políticamente, todo.

## Umbrales en el motor
Sin peso en los scores: es demasiado retrasado para sumar información a las peticiones y las nóminas. Disparador en 4,5 %: con el mínimo de 12 meses en torno al 4,0 %, es el nivel que activa la regla de Sahm en 2026.

## Casuísticas relacionadas
→ [[regla-de-sahm-activada]]: qué ha pasado en las ocho veces anteriores y la excepción de 2024.
→ [[paro-sube-por-participacion]]: cuando sube sin destrucción de empleo; menos grave.
→ [[nominas-debiles-con-peticiones-bajas]].

## Trampas de lectura
- Una décima es ruido (error estándar ±0,2 pp); la media de tres meses es la que vale.
- La U-6 (que incluye subempleo y desanimados) suele ser 3-4 pp mayor y adelanta al giro.
- Encuesta a hogares y a empresas discrepan en los giros; en 2007 el paro subió del 4,4 % al 5,0 % mientras las nóminas aún eran positivas.

## Episodios
- **Marzo-abril 2020**: de 3,5 % a 14,7 % en dos meses; vuelta al 4 % en dos años.
- **Abril 2023**: 3,4 %, mínimo desde 1969.
- **Julio 2024**: 4,3 %; Sahm activada (0,53); recortes de la Fed desde septiembre; el paro se estabilizó en 4,1-4,2 % sin recesión.
- **Octubre 2026**: 4,2 %, +0,1; a 0,3 pp del disparador.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/UNRATE y la regla de Sahm calculada: https://fred.stlouisfed.org/series/SAHMREALTIME
- Sahm, "Recession Ready" (Brookings, 2019, PDF gratuito): https://www.brookings.edu/ (buscar "Sahm rule recession ready")
- CBO, estimaciones del NAIRU: https://www.cbo.gov/data/budget-economic-data
