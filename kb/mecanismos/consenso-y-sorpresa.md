---
tipo: mecanismo
id: consenso-y-sorpresa
nombre: Consenso → sorpresa → reacción del precio
cadena: "El mercado descuenta el consenso antes del dato → lo que mueve el precio es la diferencia entre dato y consenso → y la reacción del precio dice qué estaba realmente descontado"
plazo: "minutos (reacción inicial); días (reevaluación)"
series: [todas las headline: CPIAUCSL, CPILFESL, PCEPILFE, PAYEMS, UNRATE, GDPC1, RSAFS]
sectores: [todos]
casuisticas: [ipc-sorprende-al-alza, buenas-noticias-son-malas-noticias, dato-bueno-mercado-vende]
actualizado: 2026-10-08
---

# Consenso → sorpresa → reacción del precio

El email dice qué dato ha salido y cómo ha cambiado respecto al anterior. Pero el mercado no opera el dato: opera la **sorpresa**, la diferencia entre el dato y lo que los economistas esperaban (el consenso, que se publica días antes en los calendarios económicos). Y la segunda derivada, la que distingue a un analista de un lector de titulares, es la **reacción del precio**: cómo responde el mercado a una sorpresa dice qué estaba descontado y qué no.

## Cadena
1. Antes del dato: los economistas publican estimaciones; la mediana es el consenso; el mercado se posiciona (los futuros de tipos y la bolsa ya reflejan el consenso).
2. El dato sale a las 14:30: la sorpresa (dato − consenso) mueve el 2 años, el dólar y los futuros del S&P 500 en segundos.
3. Reacción inicial (primeros 30 minutos): algoritmos; suele ser la dirección "obvia".
4. Reevaluación (hasta el cierre y los días siguientes): el mercado lee los componentes (subyacente, revisiones, horas trabajadas) y la interpretación puede cambiar: el "reversal" del 13 de octubre de 2022 (IPC alto, bolsa cae un 2 % y cierra +2,6 %).
5. La reacción final frente a la sorpresa es la información:
   - Sorpresa positiva, precio sube: normal.
   - Sorpresa positiva, precio no sube o cae: el mercado ya lo tenía descontado o mira otra cosa (tipos): **techo cercano**.
   - Sorpresa negativa, precio no cae o sube: el pesimismo ya estaba en precio: **suelo cercano**.
   - "Buenas noticias son malas noticias": datos fuertes hunden la bolsa cuando implican Fed más dura (2022-2023); es un régimen en sí mismo.

## Plazo y magnitud
- Reacción inicial: minutos. Reevaluación: 1-3 sesiones.
- Magnitud (2022-2024): una décima de sorpresa en el IPC subyacente ha movido el S&P 500 un ±1 % y el 2 años ±10 pb el día del dato.
- Los datos que más mueven: IPC, nóminas, FOMC; los que menos: PIB (anticipado por GDPNow), PCE (anticipado por IPC e IPP).

## Evidencia
- Toda la literatura de "event studies" desde Fama (1969).
- Índice de sorpresas económicas de Citi (no gratuito, pero su lógica es esta): cuando las sorpresas se acumulan positivas, los economistas suben el consenso y las sorpresas se agotan: ciclo de sorpresas de 3-6 meses.

## Cuándo falla
- Cuando el consenso está muy disperso (rango amplio de estimaciones): la "sorpresa" es menos informativa.
- En días con dos datos a la vez (nóminas y salarios): la reacción mezcla ambos.
- Cuando el dato se filtra o se revisa mucho (nóminas): la reacción se corrige con la revisión.

## Qué hacer con ello
- Anotar consenso, dato y reacción del sector a cierre en la ficha de cada dato de cabecera (nivel 4 de la guía); es la única forma de aprender qué régimen de reacción hay (buenas = buenas, o buenas = malas).
- Un dato bueno que el mercado vende, en un sector que tienes en cartera, es señal para ajustar el stop; dos seguidos, para reducir.
- Un dato malo que el mercado compra en un sector vetado por el motor es señal de que el pesimismo está en precio; el motor tardará semanas en verlo.
