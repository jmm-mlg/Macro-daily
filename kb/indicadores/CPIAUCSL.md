---
tipo: indicador
id: CPIAUCSL
nombre: IPC general de EE.UU.
bloque: Inflación
fuente: BLS (Bureau of Labor Statistics) vía FRED (CPIAUCSL, desestacionalizado)
frecuencia: mensual
publicacion: entre el día 10 y el 15 del mes siguiente, 8:30 ET (14:30 España); fechas en bls.gov/schedule
en_el_motor: variación interanual; alerta > 4,0 %; peso 1 en inflación (> 3,5 / < 2,0); disparador < 3,0 %; headline (alerta de evento)
relacionados: [CPILFESL, PCEPILFE, PPIFIS, T10YIE, CES0500000003, ipc-sorprende-al-alza, inflacion-de-costes-vs-demanda]
actualizado: 2026-10-08
---

# IPC general de EE.UU.

El dato de inflación que mueve el mercado el día que sale, aunque no sea el que la Fed usa como objetivo. Mide lo que paga el consumidor por una cesta fija de bienes y servicios, energía y alimentos incluidos.

## Qué mide
Índice de precios de una cesta de consumo urbano (CPI-U), base 1982-84 = 100. El email muestra la variación interanual (a/a). Composición aproximada: vivienda 35 % (de la que dos tercios es "alquiler equivalente del propietario", OER), transporte 17 % (gasolina y coches), alimentación 13 %, servicios médicos 8 %. La vivienda entra con 9-12 meses de retraso respecto a los alquileres de mercado, lo que hace al IPC lento en los giros.

## Cómo se lee
- **Interanual**: > 4 % fuera de control; 3-4 % persistente, la Fed no recorta; 2-3 % tolerable; < 2 % permite recortes.
- **Mensual (m/m)**: el dato que mueve el mercado. 0,2 % mensual anualiza al 2,4 %; 0,4 % anualiza al 5 %. Dos meses seguidos de 0,4 % cambian la política de la Fed.
- **Sorpresa frente al consenso**: lo que importa el día del dato. Una décima por encima del consenso en el subyacente ha movido el S&P 500 un −1 % de media en 2022-2024.
- **Los componentes que mira el mercado**: subyacente sin vivienda ("supercore"), que es el que la Fed cita; OER; y bienes básicos (que han sido deflacionarios desde 2023).

## Qué lo mueve
Energía (gasolina, con dos semanas de retardo respecto al crudo), alimentos, alquileres (con un año de retardo), salarios en servicios, dólar (bienes importados), aranceles (2025: +0,3-0,5 pp sobre bienes).

## Qué mueve
- Expectativas de Fed y el 2 años, en segundos.
- Breakeven (si sube, el mercado cree que es persistente).
- Tipo real, si la Fed reacciona.
- Sectores: un IPC alto por energía favorece a energía y castiga a transporte y consumo; uno alto por servicios castiga a todo porque implica Fed más dura.
- Ajuste de pensiones y de los TIPS.

## Umbrales en el motor
Peso 1, menor que el subyacente (3) y el PCE (3): el general es ruidoso por energía y alimentos. Alerta en 4,0 % (fuera de control). Disparador en 3,0 % a la baja: el nivel que abre la puerta a recortes.

## Casuísticas relacionadas
→ [[ipc-sorprende-al-alza]]: con breakeven estable frente a con breakeven subiendo.
→ [[inflacion-de-costes-vs-demanda]]: IPP > IPC con salarios bajando (octubre 2026) frente a IPC > IPP con salarios subiendo (2022).
→ [[ipc-alto-por-vivienda]]: el componente de alquiler con retardo; la Fed mira a través de él.

## Trampas de lectura
- Interanual arrastra el efecto base: si hace doce meses hubo un mes muy alto, el interanual baja aunque el mensual sea malo. Mirar la anualización a 3 meses.
- El IPC no es el objetivo de la Fed; el PCE lo es, y suele ser 0,3-0,5 pp más bajo por composición (menos vivienda, más salud).
- Las revisiones son pequeñas, pero los factores estacionales se revisan en febrero y pueden cambiar la lectura de los últimos meses.

## Episodios
- **Junio 2022**: 9,1 % interanual, máximo desde 1981; el dato salió el 13 de julio y la Fed subió 75 pb dos semanas después. El S&P 500 hizo suelo en octubre con el IPC aún al 7,7 %: la bolsa anticipa el pico de inflación, no espera al 2 %.
- **10 de noviembre de 2022**: IPC subyacente 0,3 % m/m frente al 0,5 % esperado; el S&P 500 subió un 5,5 % ese día, la mayor subida por un dato de inflación de la historia.
- **Enero-marzo 2024**: tres meses de 0,4 % subyacente; el mercado pasó de descontar seis recortes a dos; el 10 años subió 70 pb.
- **Octubre 2026**: 3,71 %, +0,17 pp, percentil 71; acelerando por IPP y energía.

## Para profundizar
- Serie y componentes: https://fred.stlouisfed.org/series/CPIAUCSL
- BLS, publicación mensual con tablas de componentes y calendario: https://www.bls.gov/cpi/
- Fed de Cleveland, nowcast de inflación (predice el dato antes de que salga): https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting
- Fed de Atlanta, "sticky price CPI" (componentes rígidos frente a flexibles): https://www.atlantafed.org/research/inflationproject/stickyprice
