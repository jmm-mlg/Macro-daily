---
tipo: mecanismo
id: insiders-a-retorno
nombre: Compras de insiders → retorno futuro
cadena: "Directivos compran con su dinero → saben algo que el mercado no (o creen que la acción está barata) → retorno anormal positivo a 6-12 meses, sobre todo en clusters y en empresas pequeñas; las ventas no informan"
plazo: "6-12 meses"
series: [micro: Formularios 4 de EDGAR]
sectores: [todos; más potente en small caps]
casuisticas: [cluster-de-insiders, insiders-compran-en-caida]
actualizado: 2026-10-08
---

# Compras de insiders → retorno futuro

Un directivo que compra acciones de su empresa con su propio dinero, fuera de un plan programado, está diciendo que cree que vale más. Como tiene más información que nadie, la señal es informativa, y más si varios directivos compran a la vez (cluster). Las ventas, en cambio, no dicen casi nada: se vende por diversificación, impuestos, divorcio, una casa, o por planes 10b5-1 programados con meses de antelación.

## Cadena
1. Los insiders (consejeros, directivos, accionistas > 10 %) deben comunicar cada operación a la SEC en el Formulario 4 en dos días hábiles.
2. Una compra discrecional (código P, no A de "award" ni M de ejercicio de opciones) indica convicción.
3. Un **cluster** (3 o más insiders distintos comprando en un mes) multiplica la señal: es improbable que tres personas se equivoquen a la vez.
4. El mercado reacciona poco el día de la comunicación (la noticia es pequeña), y el retorno anormal se acumula durante 6-12 meses.
5. En empresas pequeñas y menos cubiertas el efecto es mayor; en Apple o Microsoft es casi nulo.

## Plazo y magnitud
- Cohen, Malloy y Pomorski (2012): las compras "oportunistas" (no rutinarias) predicen un retorno anormal de ~0,8 % mensual (~10 % anual) frente a la nada de las rutinarias; las ventas oportunistas también predicen (negativo), pero son difíciles de distinguir de las rutinarias.
- Seyhun (1998): los clusters superan a las compras individuales; las compras tras caídas fuertes son las más informativas.
- El motor marca cluster con 3+ compradores en 30 días y compras individuales > 100.000 $.

## Evidencia
- Cohen, Malloy y Pomorski, "Decoding Inside Information", Journal of Finance (2012); NBER WP 16454 gratuito.
- Seyhun, "Investment Intelligence from Insider Trading" (1998).
- Lakonishok y Lee (2001): las compras agregadas de insiders predicen retornos del mercado; las ventas no.

## Cuándo falla
- Compras obligatorias por política de retribución (algunos consejos exigen poseer acciones): no son discrecionales.
- Compras simbólicas (un consejero compra 100 acciones para "dar señal"): mirar el importe en relación a su patrimonio o al sueldo.
- Programas de recompra de la empresa: no son insiders.
- Europa: no hay Formulario 4 centralizado; la CNMV y la BaFin publican operaciones de directivos pero con menos detalle y sin API cómoda.

## Qué hacer con ello
- Cluster en una empresa de la watchlist: punto extra en el filtro 3 y permiso para saltarse la comprobación de valoración; aun así, respetar el embudo (sector, disparador, resultados).
- Compra grande del CEO o CFO tras una caída del 20-30 %: la señal individual más fuerte; confirmar que no es parte de un plan.
- Ventas: ignorar, salvo que el CEO venda la mayor parte de su posición fuera de plan en un momento de resultados, que el motor no detecta y hay que leer en el propio Formulario 4.
