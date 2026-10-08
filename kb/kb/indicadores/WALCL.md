---
tipo: indicador
id: WALCL
nombre: Balance de la Reserva Federal (activos totales)
bloque: Tipos
fuente: Reserva Federal, informe H.4.1, vía FRED (WALCL)
frecuencia: semanal
publicacion: jueves a las 16:30 ET con datos del miércoles
en_el_motor: variación % mensual; peso 1 en liquidez (> +0,5 % expansivo, < −0,5 % contractivo)
relacionados: [DFF, DFII10, NFCI, liquidez, QE-QT, reservas-bancarias]
actualizado: 2026-10-08
---

# Balance de la Reserva Federal

Cuánto ha comprado la Fed en bonos y otros activos. Cuando crece (QE), inyecta reservas y liquidez; cuando se reduce (QT), las retira. Es la "segunda palanca" de la política monetaria, menos visible que los tipos y con efectos más lentos.

## Qué mide
Activos totales del balance consolidado de la Fed, en millones de dólares. Los componentes principales son Treasuries y bonos hipotecarios (MBS). El email muestra la variación porcentual mensual, no el nivel (en 2026 ronda los 6,5-7 billones).

## Cómo se lee
- **Tendencia**: en QE sube de forma regular (2020-2022: +120.000 M$ al mes); en QT baja (2022-2024: hasta −95.000 M$ al mes, luego −60.000).
- **Variación mensual**: entre −0,5 % y +0,5 % es mantenimiento; fuera de ese rango, hay un programa activo o una intervención de emergencia.
- **Saltos puntuales**: subidas bruscas sin programa anunciado son rescates (mar-2020, mar-2023 con la ventanilla BTFP por SVB).

## Qué lo mueve
Decisiones del FOMC sobre programas de compra o reducción; vencimientos no reinvertidos; emergencias de liquidez. Cambia lentamente salvo en crisis.

## Qué mueve
- Reservas bancarias y por tanto facilidad de crédito; cuando las reservas bajan de un nivel "amplio" los tipos a un día se tensan (sep-2019, repo).
- Tipo real a largo plazo: el QE lo comprime (estimaciones de −50 a −100 pb por cada 10 % del PIB comprado); el QT lo eleva lentamente.
- Valoraciones de activos de riesgo: la correlación entre balance y S&P 500 en 2009-2021 fue muy alta, aunque parte es coincidencia con el ciclo.

## Umbrales en el motor
Peso 1, el menor del score de liquidez, porque sus efectos son lentos y porque desde 2022 la Fed ha dejado claro que el balance es "piloto automático": la señal está en los tipos. Umbrales ±0,5 % mensual distinguen programa activo de mantenimiento.

## Casuísticas relacionadas
→ [[fin-del-qt]]: cuando la Fed anuncia el fin de la reducción, suele ser por tensiones en el mercado de repos; positivo para liquidez.
→ [[balance-sube-sin-programa]]: rescate en curso; mirar spreads y bancos.

## Trampas de lectura
- Un balance que no cambia con inflación alta es restrictivo en términos reales (el PIB nominal crece y el balance no).
- El balance del BCE y del Banco de Japón importan tanto como el de la Fed para la liquidez global; el carry del yen en 2024 lo demostró.
- Los MBS vencen más lento que los Treasuries; el ritmo de QT efectivo suele ser menor que el anunciado.

## Episodios
- **Septiembre 2019**: el QT redujo las reservas hasta que el tipo repo saltó al 10 % en un día; la Fed volvió a comprar letras. Final del primer QT.
- **Marzo 2020**: +3 billones en tres meses; el mayor QE de la historia. Suelo de la bolsa el 23 de marzo, el mismo día del anuncio de compras ilimitadas.
- **Junio 2022 - 2024**: QT de −95.000 M$ al mes, luego −60.000; el balance pasó de 9 a 7 billones. La bolsa subió en 2023-2024 pese al QT: la señal no estaba ahí.

## Para profundizar
- Serie y componentes: https://fred.stlouisfed.org/series/WALCL
- Informe H.4.1 completo (semanal): https://www.federalreserve.gov/releases/h41/
- Fed de Nueva York, operaciones de mercado abierto y SOMA: https://www.newyorkfed.org/markets/domestic-market-operations
