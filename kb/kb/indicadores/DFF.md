---
tipo: indicador
id: DFF
nombre: Tipo efectivo de los fondos federales
bloque: Tipos
fuente: Reserva Federal de Nueva York vía FRED (DFF)
frecuencia: diaria
publicacion: cada día hábil a las 9:00 ET con el dato del día anterior
en_el_motor: solo panel; la política monetaria entra por el 2 años, el tipo real y el NFCI
relacionados: [DGS2, ECBDFR, WALCL, tipo-neutral, fomc, fed-funds-futures]
actualizado: 2026-10-08
---

# Tipo efectivo de los fondos federales

El tipo al que los bancos se prestan reservas a un día, y el instrumento con el que la Fed ejecuta su política. Es el dato que menos sorprende (se conoce la decisión del FOMC) y el que más condiciona todo lo demás.

## Qué mide
Media ponderada por volumen de las operaciones a un día entre bancos en el mercado de fondos federales. La Fed fija un rango objetivo (por ejemplo, 3,75-4,00 %) y el efectivo se sitúa dentro, normalmente cerca del tipo que paga sobre reservas (IORB). Cambia solo cuando el FOMC decide (ocho reuniones al año) o por tensiones puntuales de liquidez.

## Cómo se lee
- **Frente al tipo neutral** (el que ni estimula ni frena, estimado por la Fed en torno al 3 % nominal con inflación al 2 %): por encima, política restrictiva; por debajo, expansiva. Con DFF al 3,88 % e inflación subyacente al 2,8 %, el tipo real a corto está en torno al 1 %: ligeramente restrictivo.
- **Frente al 2 años**: la distancia dice qué espera el mercado (ver DGS2).
- **Dirección del último movimiento**: la bolsa reacciona más a la dirección que al nivel. El primer recorte tras un ciclo de subidas ha coincidido con suelos (1995, 1998, 2019, 2024) y con techos (2001, 2007) según si llegó antes o después de la recesión.

## Qué lo mueve
Las decisiones del FOMC, que dependen del doble mandato (inflación al 2 %, máximo empleo), con el PCE subyacente y el paro como variables centrales. Los miembros con voto comunican su sesgo en discursos entre reuniones (ver la sección de bancos centrales del email).

## Qué mueve
Toda la curva de tipos a corto, el coste de los préstamos a tipo variable (tarjetas, pymes, hipotecas a tipo variable en Europa a través del BCE), la remuneración del efectivo (fondos monetarios, que compiten con la bolsa cuando superan el 4-5 %), el dólar y los flujos a emergentes.

## Umbrales en el motor
Ninguno directo: lo que importa para la bolsa es el tipo real (DFII10), las condiciones financieras (NFCI) y las expectativas (DGS2), que ya están en el score de liquidez. DFF se muestra para contextualizar.

## Casuísticas relacionadas
→ [[primer-recorte-del-ciclo]]: suelo o techo según el estado del empleo cuando llega.
→ [[pausa-de-la-fed]]: históricamente el mejor periodo para la bolsa es entre la última subida y el primer recorte.
→ [[mercado-descuenta-mas-subidas-que-la-fed]].

## Trampas de lectura
- El tipo nominal sin la inflación no dice nada: un 5 % con inflación al 8 % es expansivo; un 4 % con inflación al 2,5 % es restrictivo.
- La Fed no es la única fuente de restricción: el QT (balance) y los tipos largos pueden endurecer sin que DFF se mueva. Por eso el motor mira NFCI.
- Las reuniones con proyecciones (marzo, junio, septiembre, diciembre) mueven más el mercado por el dot plot que por la decisión.

## Episodios
- **2004-2006**: 17 subidas de 25 pb consecutivas, de 1,00 % a 5,25 %; la bolsa subió durante todo el ciclo porque las subidas eran previsibles ("measured pace").
- **2022**: de 0,25 % a 4,50 % en nueve meses, con cuatro subidas de 75 pb; el ciclo más rápido desde 1980. S&P 500 −25 % hasta octubre.
- **Septiembre 2024**: primer recorte (50 pb) con la bolsa en máximos y paro al 4,2 %; la bolsa siguió subiendo porque el recorte llegó sin recesión.
- **2026**: 3,88 % tras una subida de 25 pb en septiembre; el 2 años descuenta más.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/DFF
- Comunicados, proyecciones y calendario del FOMC: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Fed de Nueva York, estimación del tipo neutral (modelo Holston-Laubach-Williams): https://www.newyorkfed.org/research/policy/rstar
