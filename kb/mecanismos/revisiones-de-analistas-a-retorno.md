---
tipo: mecanismo
id: revisiones-de-analistas-a-retorno
nombre: Revisiones de estimaciones → retorno relativo
cadena: "Los analistas revisan al alza/baja → el precio se ajusta parcialmente → más revisiones en la misma dirección (son graduales) → el precio sigue ajustándose: retorno relativo positivo durante 1-3 meses"
plazo: "1-3 meses; el efecto se agota a 6"
series: [micro: amplitud de revisiones por sector]
sectores: [todos]
casuisticas: [conflicto-macro-micro, revisiones-giran-a-la-baja-en-maximos]
actualizado: 2026-10-08
---

# Revisiones de estimaciones → retorno relativo

Los analistas revisan sus estimaciones poco a poco (nadie pasa de 5 a 7 dólares de BPA de un día para otro; sube a 5,5, luego a 6…), y el mercado tampoco descuenta la revisión de golpe. El resultado es que las acciones y sectores cuyas estimaciones suben hoy tienden a seguir subiendo en términos relativos durante 1-3 meses. Es una de las anomalías más robustas de la literatura y el fundamento de la capa micro del motor.

## Cadena
1. Una empresa publica resultados o guía mejor de lo esperado; o el sector recibe un viento macro (petróleo para energía).
2. Los analistas revisan al alza, pero de forma escalonada y conservadora ("anclaje").
3. El precio reacciona a la primera revisión; las siguientes (semanas) siguen llegando y el precio sigue subiendo.
4. Las instituciones, que compran por fundamentales, aumentan posición conforme suben las estimaciones.
5. A los 3-6 meses el precio ha incorporado la nueva realidad; la señal se agota y puede revertir.

## Plazo y magnitud
- Chan, Jegadeesh y Lakonishok (1996): la decila de acciones con mejores revisiones bate a la peor en 4-6 % anualizado a 6 meses.
- A nivel sectorial (amplitud: % de empresas con revisiones netas positivas), el efecto a 1-3 meses sobre el retorno relativo al índice es consistente en EE.UU. y Europa.
- El motor mide la amplitud a 30 días por sector y la señala por encima de +0,2 y por debajo de −0,2.

## Evidencia
- Chan, Jegadeesh y Lakonishok, "Momentum Strategies", Journal of Finance (1996).
- Factores "earnings revisions" en los modelos de riesgo (Barra, Axioma) desde los años 90; sigue siendo factor rentable en 2010-2025 aunque menos que antes.

## Cuándo falla
- En giros de mercado bruscos (marzo 2020, octubre 2022): las revisiones llegan tarde y el precio ya ha dado la vuelta; la señal es procíclica.
- Cuando las revisiones son por un hecho ya descontado (una adquisición anunciada).
- Para empresas con pocos analistas (Europa pequeña): ruido.

## Qué hacer con ello
- Sector con sesgo macro ≥ +1 y amplitud > +0,2: combinación prioritaria (filtro 2 de la guía).
- Sector con sesgo macro negativo y amplitud positiva: **conflicto**; el micro suele ganar a semanas y el macro a meses; no abrir hasta que uno ceda.
- Empresa con revisiones extremas (net30 > 0,6 con 3+ analistas) y sin 8-K negativos: candidata válida aunque el resultado ya se haya publicado, mientras las revisiones sigan llegando.
