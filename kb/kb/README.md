# Base de conocimiento del Macro Monitor

Fuente única de conocimiento del sistema: qué mide cada dato del email, cómo se lee, qué mueve, qué casuísticas genera y qué dice la evidencia. Un archivo Markdown por entrada, con cabecera YAML y plantilla fija (`PLANTILLA.md`). Las entradas se enlazan con `[[id]]`.

## Tipos de entrada
| Carpeta | Tipo | Contenido | Estado |
| --- | --- | --- | --- |
| `indicadores/` | Indicador | Las 36 series del email (los 7 factores del motor son series ya cubiertas) | 36 hechas |
| `conceptos/` | Concepto | Régimen, prima de riesgo, duración, pricing power, R, ATR… (~25) | pendiente |
| `mecanismos/` | Mecanismo | Cadenas de transmisión con plazos y evidencia (~15) | pendiente |
| `sectores/` | Sector | Los 11 GICS: drivers, métricas, comportamiento por régimen, bellwethers | pendiente |
| `casuisticas/` | Casuística | "Qué significa y qué hacer cuando…" (~25, creciendo con el motor) | 1 hecha |
| `episodios/` | Episodio | Casos históricos de referencia (2007-08, 2011, 2015-16, 2018, 2020, 2022, 2023) | pendiente |
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
### Casuísticas
- [Bolsa y tipo real en percentiles altos a la vez](casuisticas/bolsa-y-tipo-real-en-maximos.md)
### Biblioteca
- [Fuentes gratuitas por nivel](BIBLIOTECA.md)

## Verificación
`verificacion.yaml` recoge las afirmaciones fechadas de las entradas (65) en forma comprobable; `verificar.py` las contrasta con FRED y yfinance y escribe `_verificacion.md`. Corre el día 1 de cada mes y a mano desde Actions. Toda nueva cifra en una entrada se añade al YAML. Las 10 afirmaciones de mercado se comprobaron en vivo el 2026-10-08 (10/10 OK); las 55 de FRED, en la primera ejecución con clave.

## Cómo se usa
- **Desde el email**: cada serie del panel y cada disparador enlaza a su entrada (`kb_url` en `config.yaml`).
- **Desde Claude**: la carpeta se carga como conocimiento en un Proyecto "Analista senior" para responder preguntas con las entradas como base.
- **Crecimiento**: cuando el motor detecta una casuística sin entrada, genera un borrador en `casuisticas/_borradores/` con los datos del día para revisar el fin de semana (pendiente).
- **Cambios**: toda modificación de un umbral del motor se refleja en la sección "Umbrales en el motor" de la entrada correspondiente, con fecha.
