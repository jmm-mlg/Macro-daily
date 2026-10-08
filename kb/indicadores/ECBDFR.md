---
tipo: indicador
id: ECBDFR
nombre: Tipo de la facilidad de depósito del BCE
bloque: Tipos
fuente: Banco Central Europeo vía FRED (ECBDFR)
frecuencia: diaria (cambia en reuniones del Consejo de Gobierno)
publicacion: decisiones a las 14:15 CET, ocho veces al año; rueda de prensa a las 14:45
en_el_motor: solo panel; Europa entra por el IPCA y por las empresas europeas de la watchlist
relacionados: [DFF, CP0000EZ19M086NEST, euribor, bancos-europeos, bce-vs-fed]
actualizado: 2026-10-08
---

# Tipo de la facilidad de depósito del BCE

El tipo de referencia de la zona euro desde 2014 (es el que remunera el exceso de reservas y el que ancla el euríbor). Decide el coste de las hipotecas variables en España, el margen de la banca europea y buena parte del tipo de cambio euro-dólar.

## Qué mide
Tipo al que los bancos depositan su exceso de liquidez en el BCE a un día. De los tres tipos oficiales (depósito, operaciones principales, facilidad marginal) es el relevante porque con exceso de reservas el interbancario cotiza pegado a él. El euríbor a 12 meses suele situarse entre 0 y 50 pb por encima según las expectativas.

## Cómo se lee
- **Frente a la inflación de la eurozona (IPCA)**: con IPCA al 3,2 % y depósito al 2,5 %, el tipo real a corto es negativo: política aún laxa en términos reales pese a la subida.
- **Frente a la Fed**: el diferencial Fed − BCE (3,88 − 2,50 = 138 pb) mueve el euro-dólar; cuando se estrecha, el euro sube.
- **Dirección**: el BCE se mueve en pasos de 25 pb y anuncia con antelación; las sorpresas son raras. Lo informativo son las proyecciones del staff (marzo, junio, septiembre, diciembre) y el tono de la rueda de prensa.

## Qué lo mueve
IPCA subyacente (la variable central), salarios negociados (el BCE publica un indicador propio), expectativas de inflación, y en menor medida el crecimiento y el tipo de cambio. El BCE suele ir detrás de la Fed con 3-6 meses de retardo, salvo en 2024 cuando recortó antes.

## Qué mueve
- **Euríbor** y con él las hipotecas variables (más del 60 % del stock en España): efecto directo en consumo español e italiano.
- **Margen de intermediación de la banca europea**: subidas de tipos elevaron el ROE de los bancos españoles del 8 % al 15 % entre 2022 y 2024.
- **Euro-dólar**, vía diferencial con la Fed.
- **Utilities e inmobiliario europeos**, por duración.
- **Deuda periférica**: spreads Italia-Alemania y España-Alemania se tensan cuando el BCE endurece.

## Umbrales en el motor
Sin umbral: el motor es predominantemente estadounidense. Europa entra por el IPCA (score de inflación, peso 1) y, a través de la watchlist, por las revisiones de analistas y los resultados de las empresas europeas. Una futura versión podría añadir un score de liquidez europeo con este tipo, el Bund a 10 años y el spread Italia-Alemania.

## Casuísticas relacionadas
→ [[bce-sube-con-inflacion-de-costes]]: cuando la inflación europea viene de energía y el BCE sube igual, el daño cae en consumo y periferia.
→ [[divergencia-fed-bce]]: diferencial que se abre o cierra y su efecto en el euro y en las multinacionales europeas.

## Trampas de lectura
- Antes de 2014 el tipo relevante era el de operaciones principales de financiación; las series largas mezclan ambos.
- El BCE tiene un instrumento (TPI) para contener spreads periféricos; su mera existencia cambia la reacción de los mercados a las subidas.
- El tipo real europeo relevante para la bolsa es el del Bund indexado, no este; FRED no lo tiene, el BCE sí en su Data Portal.

## Episodios
- **Julio 2011**: el BCE subió tipos con la crisis de deuda en marcha; tuvo que deshacerlo en noviembre. Caso de manual de subida equivocada.
- **Julio 2022 - septiembre 2023**: de −0,50 % a 4,00 % en catorce meses, el ciclo más rápido de su historia; los bancos europeos subieron un 60 % en el periodo.
- **Junio 2024**: primer recorte, antes que la Fed; euro-dólar bajó de 1,09 a 1,03 en seis meses.
- **Octubre 2026**: 2,50 % tras subir 25 pb, con IPCA al 3,2 % y acelerando.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/ECBDFR
- Decisiones, proyecciones y declaraciones del BCE: https://www.ecb.europa.eu/press/pr/html/index.en.html
- Data Portal del BCE (tipos, Bund real, salarios negociados): https://data.ecb.europa.eu/
- Boletín Económico del Banco de España: https://www.bde.es/wbe/es/publicaciones/analisis-economico-investigacion/boletin-economico/
