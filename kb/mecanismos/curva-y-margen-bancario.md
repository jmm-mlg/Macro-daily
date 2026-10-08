---
tipo: mecanismo
id: curva-y-margen-bancario
nombre: Pendiente de la curva → margen bancario → crédito
cadena: "Curva empina → margen de intermediación sube → bancos prestan más y ganan más → crédito fluye → actividad; curva invertida → lo contrario"
plazo: "2-3 trimestres del cambio de pendiente al margen; 2-4 trimestres del crédito a la actividad"
series: [T10Y2Y, DFF, BAMLH0A0HYM2, NFCI]
sectores: [financiero, inmobiliario, discrecional]
casuisticas: [curva-se-desinvierte, bancos-y-curva]
actualizado: 2026-10-08
---

# Pendiente de la curva → margen bancario → crédito

Los bancos ganan dinero tomando prestado a corto (depósitos, mercado interbancario) y prestando a largo (hipotecas, empresas). La pendiente de la curva es su margen bruto. Cuando la curva se invierte, prestar deja de ser rentable, el crédito se contrae y la economía se frena: es el canal por el que la inversión de la curva se convierte en recesión, y la razón por la que el factor "curva" del motor carga +1 en financiero.

## Cadena
1. La Fed sube el tipo corto más que lo que sube el largo → la curva se aplana o invierte.
2. El coste de los depósitos y la financiación mayorista sube; el rendimiento de la cartera de préstamos (muchos a tipo fijo) sube despacio → el **margen de interés neto** se comprime con retardo de 2-3 trimestres.
3. Los bancos endurecen las condiciones de préstamo (se ve en la encuesta SLOOS de la Fed, trimestral) → menos crédito a pymes, consumo e inmobiliario.
4. La actividad sensible al crédito cae con 2-4 trimestres de retardo: vivienda, coches, capex de pymes.
5. Al revés cuando la curva se empina por recortes de la Fed: margen sube, crédito fluye, recuperación.

## Plazo y magnitud
- Del empinamiento al NII: 2-3 trimestres (los bancos reprecian el activo con retardo).
- Del endurecimiento de condiciones (SLOOS) a la caída del crédito: 1-2 trimestres; a la actividad, 2-4.
- Magnitud: en 2022-2024 la curva estuvo invertida 26 meses y los estándares de crédito se endurecieron como en 2008, pero el crédito no se contrajo tanto porque empresas y hogares habían refinanciado a tipos bajos en 2020-2021.

## Evidencia
- Estrella y Mishkin (1996), Harvey (1988): la curva como predictor de recesión; el canal bancario es una de las explicaciones.
- Fed, Senior Loan Officer Opinion Survey: la correlación entre el porcentaje neto de bancos que endurecen y el crecimiento del crédito a 2 trimestres es alta.
- Gilchrist y Zakrajšek (2012): los spreads de crédito (el precio del crédito) anticipan la actividad.

## Cuándo falla
- Con exceso de reservas y depósitos "pegajosos" (2022-2023): los bancos no pagaron los depósitos al ritmo del tipo oficial y el margen subió pese a la curva invertida, hasta que SVB mostró el límite.
- Con crédito no bancario (fondos de deuda privada, bonos): si las empresas se financian fuera de los bancos, el canal se debilita.
- Bear steepening (la curva se empina porque el 10 años sube por prima de plazo): el margen mejora pero el coste del crédito a largo sube; ambiguo para la actividad.

## Qué hacer con ello
- Sesgo positivo a bancos cuando la curva se empina por bajada del corto (bull steepening tras el pivot) y los spreads de crédito están estables; es la combinación de 1995 y 2019.
- Cuidado con bancos cuando la curva se empina a la vez que el HY sube: el margen mejora pero las provisiones vienen detrás.
- La encuesta SLOOS (enero, abril, julio, octubre) es la fuente externa que cierra el circuito; conviene mirarla el día que sale.
