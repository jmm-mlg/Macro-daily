# Base de conocimiento del Macro Monitor

Fuente única de conocimiento del sistema: qué mide cada dato del email, cómo se lee, qué mueve, qué casuísticas genera y qué dice la evidencia. Un archivo Markdown por entrada, con cabecera YAML y plantilla fija (`PLANTILLA.md`). Las entradas se enlazan con `[[id]]`.

## Tipos de entrada
| Carpeta | Tipo | Contenido | Estado |
| --- | --- | --- | --- |
| `indicadores/` | Indicador | Las 39 series del email (incluye euro-dólar, dólar-yen, dólar-yuan) | 38 hechas |
| `conceptos/` | Concepto | Régimen, prima de riesgo, duración, pricing power, divisas… | 1 hecho |
| `mecanismos/` | Mecanismo | Cadenas de transmisión con plazos y evidencia | 15 hechos |
| `sectores/` | Sector | Los 11 GICS: drivers, métricas, comportamiento por régimen, bellwethers | 11 hechos |
| `casuisticas/` | Casuística | "Qué significa y qué hacer cuando…" (creciendo con el motor) | 80 hechas |
| `episodios/` | Episodio | Casos históricos de referencia (2007-08, 2011, 2015-16, 2018, 2020, 2022, 2023) | pendiente: los episodios están hoy repartidos en las entradas; una entrada por crisis es la siguiente fase |
| `BIBLIOTECA.md` | Biblioteca | Fuentes gratuitas por nivel | hecha |

## Entradas disponibles
### Indicadores · Tipos
- [DFII10 · Tipo real a 10 años (TIPS)](indicadores/DFII10.md)
- [DGS10 · Treasury a 10 años](indicadores/DGS10.md)
- [DGS2 · Treasury a 2 años](indicadores/DGS2.md)
- [T10Y2Y · Pendiente de la curva 10−2](indicadores/T10Y2Y.md)
- [DFF · Fed funds efectivo](indicadores/DFF.md)
- [T10YIE · Breakeven de inflación a 10 años](indicadores/T10YIE.md)
- [WALCL · Balance de la Fed](indicadores/WALCL.md)
- [ECBDFR · Facilidad de depósito del BCE](indicadores/ECBDFR.md)
### Indicadores · Crédito y vivienda
- [BAMLH0A0HYM2 · Spread High Yield](indicadores/BAMLH0A0HYM2.md)
- [BAMLC0A0CM · Spread Investment Grade](indicadores/BAMLC0A0CM.md)
- [NFCI · Condiciones financieras](indicadores/NFCI.md)
- [MORTGAGE30US · Hipoteca a 30 años](indicadores/MORTGAGE30US.md)
### Indicadores · Inflación
- [CPIAUCSL · IPC general](indicadores/CPIAUCSL.md)
- [CPILFESL · IPC subyacente](indicadores/CPILFESL.md)
- [PCEPILFE · PCE subyacente](indicadores/PCEPILFE.md)
- [PPIFIS · IPP demanda final](indicadores/PPIFIS.md)
- [CES0500000003 · Salario medio por hora](indicadores/CES0500000003.md)
- [CP0000EZ19M086NEST · IPCA eurozona](indicadores/CP0000EZ19M086NEST.md)
### Indicadores · Empleo
- [PAYEMS · Nóminas no agrícolas](indicadores/PAYEMS.md)
- [UNRATE · Tasa de paro](indicadores/UNRATE.md)
- [ICSA · Peticiones iniciales de desempleo](indicadores/ICSA.md)
- [JTSJOL · Vacantes JOLTS](indicadores/JTSJOL.md)
### Indicadores · Actividad y vivienda
- [GDPC1 · PIB real](indicadores/GDPC1.md)
- [RSAFS · Ventas minoristas](indicadores/RSAFS.md)
- [INDPRO · Producción industrial](indicadores/INDPRO.md)
- [DGORDER · Pedidos de bienes duraderos](indicadores/DGORDER.md)
- [UMCSENT · Confianza del consumidor (Michigan)](indicadores/UMCSENT.md)
- [PERMIT · Permisos de construcción](indicadores/PERMIT.md)
- [HOUST · Viviendas iniciadas](indicadores/HOUST.md)
### Indicadores · Mercado
- [^GSPC · S&P 500](indicadores/GSPC.md)
- [^VIX · VIX](indicadores/VIX.md)
- [DX-Y.NYB · Índice del dólar](indicadores/DXY.md)
- [CL=F · Petróleo WTI](indicadores/CL.md)
- [HG=F · Cobre](indicadores/HG.md)
- [GC=F · Oro](indicadores/GC.md)
- ^TNX · Treasury 10 años (mercado): ver [DGS10](indicadores/DGS10.md)
- [EURUSD=X · Euro-dólar](indicadores/EURUSD.md) · [JPY=X · Dólar-yen (carry)](indicadores/USDJPY.md) · CNY=X · Dólar-yuan: ver [Divisas](conceptos/divisas.md)
### Conceptos
- [Divisas: cómo leerlas para invertir en acciones](conceptos/divisas.md)
### Sectores (GICS)
- [Financiero](sectores/financiero.md) · [Energía](sectores/energia.md) · [Tecnología de la información](sectores/tecnologia.md) · [Consumo discrecional](sectores/discrecional.md) · [Industriales](sectores/industriales.md) · [Materiales](sectores/materiales.md) · [Consumo básico](sectores/basico.md) · [Salud](sectores/salud.md) · [Servicios de comunicación](sectores/comunicacion.md) · [Utilities](sectores/utilities.md) · [Inmobiliario](sectores/inmobiliario.md)
### Mecanismos de transmisión
- [Tipo real → múltiplos](mecanismos/tipo-real-y-multiplos.md)
- [Curva → margen bancario → crédito](mecanismos/curva-y-margen-bancario.md)
- [Petróleo → inflación → renta real → consumo](mecanismos/petroleo-a-inflacion-y-consumo.md)
- [Dólar → beneficios exteriores y materias primas](mecanismos/dolar-y-beneficios-exteriores.md)
- [Spreads de crédito → refinanciación → actividad](mecanismos/credito-a-actividad.md)
- [Hipotecas → vivienda → ciclo](mecanismos/vivienda-y-ciclo.md)
- [Bolsa y vivienda → riqueza → consumo](mecanismos/efecto-riqueza.md)
- [IPP frente a IPC y salarios → márgenes](mecanismos/inflacion-de-costes-vs-demanda.md)
- [Mercado laboral → salarios → inflación de servicios → Fed](mecanismos/salarios-a-inflacion-de-servicios.md)
- [Decisión de la Fed → economía real: retardos](mecanismos/politica-monetaria-retardos.md)
- [Revisiones de analistas → retorno relativo](mecanismos/revisiones-de-analistas-a-retorno.md)
- [Compras de insiders → retorno futuro](mecanismos/insiders-a-retorno.md)
- [Ciclo de inventarios → producción → cíclicos](mecanismos/ciclo-de-inventarios.md)
- [Liquidez global, dólar y carry → activos de riesgo](mecanismos/liquidez-global-y-carry.md)
- [Consenso → sorpresa → reacción del precio](mecanismos/consenso-y-sorpresa.md)
### Casuísticas
- [Bolsa y tipo real en percentiles altos a la vez](casuisticas/bolsa-y-tipo-real-en-maximos.md)
- [Nóminas débiles con peticiones de desempleo bajas](casuisticas/nominas-debiles-con-peticiones-bajas.md)
- [Consumo fuerte con confianza en mínimos](casuisticas/consumo-fuerte-con-confianza-baja.md)
- [Cobre en máximos con pedidos de bienes de capital cayendo](casuisticas/cobre-sube-con-pedidos-cayendo.md)
- [El oro cae mientras la inflación sube](casuisticas/oro-cae-con-inflacion-alta.md)
- [La pausa de la Fed](casuisticas/pausa-de-la-fed.md)
- [El primer recorte del ciclo: suelo o techo](casuisticas/primer-recorte-del-ciclo.md)
- Tipos y curva: [Subida rápida del 10 años](casuisticas/subida-rapida-del-10-anos.md) · [El bono rinde más que la bolsa](casuisticas/bono-supera-earnings-yield.md) · [La curva se desinvierte](casuisticas/curva-se-desinvierte.md) · [Curva invertida con bolsa en máximos](casuisticas/curva-invertida-con-bolsa-en-maximos.md) · [Curva empinando con spreads subiendo (bancos)](casuisticas/bancos-y-curva.md) · [El mercado descuenta más subidas que la Fed](casuisticas/mercado-descuenta-mas-subidas-que-la-fed.md) · [Tipo real por crecimiento o por prima](casuisticas/tipo-real-sube-por-crecimiento-o-por-prima.md) · [Fin del QT](casuisticas/fin-del-qt.md) · [Balance sube sin programa](casuisticas/balance-sube-sin-programa.md)
- Crédito, riesgo y mercado: [El HY sube con la bolsa en máximos](casuisticas/credito-avisa-antes-que-la-bolsa.md) · [El HY sube y el VIX no](casuisticas/hy-sube-con-vix-bajo.md) · [El HY sube por el petróleo](casuisticas/spread-sube-por-petroleo.md) · [El IG se amplía más que el HY](casuisticas/ig-se-amplia-con-hy-estable.md) · [Ángeles caídos](casuisticas/angeles-caidos.md) · [NFCI sube rápido](casuisticas/nfci-sube-rapido.md) · [La Fed endurece y el NFCI no se mueve](casuisticas/fed-sube-y-el-nfci-no-se-mueve.md) · [VIX sobre 25](casuisticas/vix-sobre-25.md) · [VIX bajo con tipo real alto](casuisticas/vix-bajo-con-tipo-real-alto.md) · [Amplitud estrecha en máximos](casuisticas/amplitud-estrecha-en-maximos.md) · [Corrección del 10 %: susto o bajista](casuisticas/correccion-del-10-por-ciento.md) · [Deshacer del carry](casuisticas/deshacer-del-carry.md)
- Divisas: [Dólar fuerte con materias primas subiendo](casuisticas/dolar-fuerte-y-materias-primas.md) · [El dólar sube mientras la bolsa cae](casuisticas/dolar-sube-con-bolsa-cayendo.md) · [El dólar cae con los tipos subiendo](casuisticas/dolar-cae-con-tipos-subiendo.md) · [Divergencia Fed-BCE](casuisticas/divergencia-fed-bce.md)
- Inflación: [IPC sorprende al alza](casuisticas/ipc-sorprende-al-alza.md) · [IPC alto con breakeven estable](casuisticas/ipc-alto-con-breakeven-estable.md) · [Breakeven sube con el petróleo](casuisticas/breakeven-sube-con-petroleo.md) · [Subyacente baja y general sube](casuisticas/subyacente-baja-y-general-sube.md) · [Supercore acelera](casuisticas/supercore-acelera.md) · [Bienes en deflación, servicios en inflación](casuisticas/bienes-deflacionarios-servicios-inflacionarios.md) · [IPC alto por vivienda](casuisticas/ipc-alto-por-vivienda.md) · [PCE por encima de la proyección del FOMC](casuisticas/pce-por-encima-de-la-proyeccion-del-fomc.md) · [IPC y PCE divergen](casuisticas/ipc-y-pce-divergen.md) · [IPP sube por aranceles](casuisticas/ipp-sube-por-aranceles.md) · [Márgenes en máximos](casuisticas/margenes-en-maximos.md) · [Espiral salarios-precios](casuisticas/espiral-salarios-precios.md) · [Salarios por debajo del IPC](casuisticas/salarios-por-debajo-del-ipc.md) · [Salarios bajan con paro bajo](casuisticas/salarios-bajan-con-paro-bajo.md) · [Expectativas de Michigan desancladas](casuisticas/expectativas-de-inflacion-desancladas-en-michigan.md)
- Empleo y actividad: [Regla de Sahm activada](casuisticas/regla-de-sahm-activada.md) · [Paro sube por participación](casuisticas/paro-sube-por-participacion.md) · [Peticiones cruzan el umbral](casuisticas/peticiones-superan-umbral.md) · [Continuadas suben con iniciales estables](casuisticas/continuadas-suben-con-iniciales-estables.md) · [Vacantes caen sin subir el paro](casuisticas/vacantes-caen-sin-subir-el-paro.md) · [Renuncias en mínimos](casuisticas/renuncias-en-minimos.md) · [Revisiones negativas acumuladas](casuisticas/revisiones-negativas-acumuladas.md) · [Buenas noticias son malas noticias](casuisticas/buenas-noticias-son-malas-noticias.md) · [Recesión técnica sin recesión](casuisticas/recesion-tecnica-sin-recesion.md) · [PIB fuerte por inventarios](casuisticas/pib-fuerte-por-inventarios.md) · [Capex de IA sostiene el PIB](casuisticas/capex-de-ia-sostiene-el-pib.md) · [Capex cae con beneficios en máximos](casuisticas/capex-cae-con-beneficios-en-maximos.md) · [Recesión industrial sin recesión general](casuisticas/recesion-industrial-sin-recesion-general.md) · [Utilización sobre 80 %](casuisticas/utilizacion-sobre-80.md) · [Pedidos de aviones distorsionan](casuisticas/pedidos-de-aviones-distorsionan.md)
- Materias primas: [Petróleo por oferta o demanda](casuisticas/petroleo-sube-por-oferta-vs-demanda.md) · [Petróleo sobre 90 y consumo](casuisticas/petroleo-sobre-90-y-consumo.md) · [Cobre sube por oferta](casuisticas/cobre-sube-por-oferta.md) · [Cobre con producción plana](casuisticas/cobre-sube-con-produccion-plana.md) · [Ratio cobre/oro y 10 años](casuisticas/cobre-oro-y-10-anos.md) · [Oro sube con tipo real alto](casuisticas/oro-sube-con-tipo-real-alto.md) · [Oro y bolsa suben a la vez](casuisticas/oro-y-bolsa-suben-a-la-vez.md)
- Vivienda y consumo: [Hipoteca cara con precios altos](casuisticas/hipoteca-cara-con-precios-altos.md) · [Diferencial hipotecario anormal](casuisticas/diferencial-hipotecario-anormal.md) · [Permisos caen tres meses](casuisticas/permisos-caen-tres-meses.md) · [Permisos sin inicios](casuisticas/permisos-sin-inicios.md) · [Inicios multifamiliares en máximos](casuisticas/inicios-multifamiliares-en-maximos.md) · [Multifamiliar se desploma](casuisticas/multifamiliar-se-desploma.md) · [Ventas suben por gasolina](casuisticas/ventas-nominales-suben-por-gasolina.md) · [Consumo financiado con crédito](casuisticas/consumo-financiado-con-credito.md) · [Confianza en mínimos como señal contraria](casuisticas/confianza-en-minimos-como-senal-contraria.md)
- Europa: [BCE sube con inflación de costes](casuisticas/bce-sube-con-inflacion-de-costes.md) · [Inflación europea por energía](casuisticas/inflacion-europea-por-energia.md)
### Biblioteca
- [Fuentes gratuitas por nivel](BIBLIOTECA.md)

## Verificación
`verificacion.yaml` recoge las afirmaciones fechadas de las entradas (65) en forma comprobable; `verificar.py` las contrasta con FRED y yfinance y escribe `_verificacion.md`. Corre el día 1 de cada mes y a mano desde Actions. Toda nueva cifra en una entrada se añade al YAML. Primera ejecución completa el 2026-10-08: 53 OK, 6 desviaciones (corregidas en las entradas y en el YAML ese mismo día), 7 sin dato (series ICE BofA, en diagnóstico). Regla desde entonces: los episodios distinguen el valor **publicado** del **revisado** en series que se revisan (nóminas, peticiones, paro, PCE).

## Cómo se usa
- **Desde el email**: cada serie del panel y cada disparador enlaza a su entrada (`kb_url` en `config.yaml`).
- **Desde Claude**: la carpeta se carga como conocimiento en un Proyecto "Analista senior" para responder preguntas con las entradas como base.
- **Crecimiento**: cuando el motor detecta una casuística sin entrada, genera un borrador en `casuisticas/_borradores/` con los datos del día para revisar el fin de semana (pendiente).
- **Cambios**: toda modificación de un umbral del motor se refleja en la sección "Umbrales en el motor" de la entrada correspondiente, con fecha.
