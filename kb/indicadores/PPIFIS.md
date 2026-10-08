---
tipo: indicador
id: PPIFIS
nombre: Índice de precios de producción, demanda final
bloque: Inflación
fuente: BLS vía FRED (PPIFIS)
frecuencia: mensual
publicacion: el día siguiente al IPC, 8:30 ET
en_el_motor: variación interanual; peso 2 en inflación (> 3,0 / < 1,0, tendencia ±0,3); en el calendario
relacionados: [CPIAUCSL, CL=F, HG=F, DX-Y.NYB, margenes-empresariales, inflacion-de-costes-vs-demanda]
actualizado: 2026-10-08
---

# Índice de precios de producción (demanda final)

Lo que cobran los productores por sus bienes y servicios antes de llegar al consumidor. Es la "tubería" de la inflación: adelanta al IPC en 2-4 meses en bienes, y su relación con el IPC dice quién se está quedando con el margen.

## Qué mide
Precios recibidos por los productores domésticos por bienes, servicios y construcción vendidos para demanda final (consumo, inversión, exportación, gobierno). Desde 2014 incluye servicios (dos tercios del índice); antes era solo bienes. Dentro de servicios pesa mucho el "margen comercial" (lo que ganan mayoristas y minoristas), que puede subir sin que suban los costes.

## Cómo se lee
- **Interanual**: > 3 % presión de costes; 1-3 % normal; < 1 % o negativo, deflación en la tubería (2015, 2020, 2023).
- **IPP frente a IPC**: la lectura más útil.
  - IPP > IPC y subiendo (octubre 2026: 5,4 % frente a 3,7 %): los costes suben más que los precios finales; los márgenes de las empresas se comprimen salvo que tengan poder de fijación de precios. Malo para consumo básico, industriales de bajo margen, transporte.
  - IPC > IPP (2023-2024): los precios finales suben más que los costes; los márgenes se expanden. Es el entorno que explica los beneficios récord de 2024.
- **Componentes**: bienes (energía y alimentos pesan mucho, de ahí la volatilidad) frente a servicios; y los "intermedios" (PPI de etapas previas) que adelantan aún más.

## Qué lo mueve
Petróleo y gas (energía es el 20 % de bienes), metales, fletes, dólar (importaciones), aranceles (de forma directa: en 2025 los bienes del IPP subieron antes que los del IPC), salarios en servicios, márgenes comerciales.

## Qué mueve
- IPC de bienes, con 2-4 meses de retardo.
- Márgenes empresariales: la variable que conecta la macro con los resultados; se contrasta con el margen bruto de las empresas de la watchlist en cada temporada de resultados.
- PCE: la BEA usa componentes del IPP (sanidad, servicios financieros, transporte aéreo) para calcularlo, por eso el mercado estima el PCE el día del IPP.

## Umbrales en el motor
Peso 2, por debajo de subyacente y PCE: adelanta, pero es volátil. Umbral alto en 3,0 %, bajo en 1,0 %, zona muerta de ±0,3 pp porque un mes de energía puede moverlo medio punto.

## Casuísticas relacionadas
→ [[inflacion-de-costes-vs-demanda]]: IPP > IPC con salarios flojos (costes) frente a IPC > IPP con salarios fuertes (demanda); implicaciones sectoriales opuestas.
→ [[ipp-sube-por-aranceles]]: 2025; quién lo absorbe y quién lo traslada.
→ [[margenes-en-maximos]]: cuando IPC > IPP durante dos años, los márgenes están en máximos y las revisiones al alza tienen techo.

## Trampas de lectura
- Antes de 2014 la serie era solo bienes; las comparaciones largas no son homogéneas.
- Los márgenes comerciales dentro del IPP de servicios pueden caer en un mes de rebajas y hacer que el IPP parezca deflacionario sin que lo sea.
- El IPP no incluye importaciones; los precios de importación (BLS, serie separada) son otro adelantado del IPC de bienes.

## Episodios
- **Marzo 2022**: 11,7 % interanual, máximo histórico de la serie; el IPC llegó al 9,1 % en junio. El IPP marcó el pico tres meses antes.
- **2023**: cayó del 6 % al 1 % mientras el IPC seguía al 3-4 %: fue el año de expansión de márgenes del S&P 500 (de 11 % a 12,5 % de margen neto).
- **Octubre 2026**: 5,41 %, +0,61 pp, percentil 76, por encima del IPC: compresión de márgenes en marcha salvo en energía y materiales.

## Para profundizar
- Serie: https://fred.stlouisfed.org/series/PPIFIS
- BLS, publicación mensual con detalle por etapa y componente: https://www.bls.gov/ppi/
- BLS, precios de importación y exportación: https://www.bls.gov/mxp/
