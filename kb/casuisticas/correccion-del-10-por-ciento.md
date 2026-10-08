---
tipo: casuistica
id: correccion-del-10-por-ciento
nombre: Corrección del 10 %: susto o inicio de mercado bajista
señales: [^GSPC −10 % desde máximo; distinguir con BAMLH0A0HYM2, ICSA, T10Y2Y y NFCI]
en_el_motor: ^GSPC pierde percentil; VIX suele cruzar 25; la combinación con HY e ICSA decide
relacionados: [^GSPC, ^VIX, BAMLH0A0HYM2, ICSA, T10Y2Y, vix-sobre-25, credito-avisa-antes-que-la-bolsa]
actualizado: 2026-10-09
---

# Corrección del 10 %: susto o inicio de mercado bajista

El S&P 500 cae un 10 % desde máximos aproximadamente una vez al año; cae un 20 % (mercado bajista) una vez cada 4-6 años. La mayoría de las correcciones del 10 % se recuperan en 2-4 meses; las que no, son el principio de caídas del 25-50 %. La diferencia no está en la bolsa sino en lo que la acompaña.

## Cómo identificarla
Tabla de distinción, con los datos del email del día en que el índice marca −10 %:
| Variable | Susto (se recupera) | Mercado bajista (sigue) |
| --- | --- | --- |
| HY | < 450 pb | > 500 pb y subiendo |
| Peticiones (media 4 semanas) | Estables, < 240k | Subiendo, > 260k |
| Curva | Cualquiera | Desinvirtiendo por bull steepening |
| NFCI | < 0 | > 0 y subiendo |
| Revisiones de analistas | Estables | Girando a la baja en todos los sectores |
| Fed | Dispuesta a pausar o recortar | Subiendo o inflación que lo impide |
| Causa | Técnica, posicionamiento, susto (aranceles, carry, Fed) | Beneficios, crédito, recesión |

## Qué significa
Susto: desapalancamiento sin deterioro fundamental; el mercado baja a un precio donde los compradores de largo plazo entran. Mercado bajista: los beneficios van a caer y el mercado lo descuenta por fases (primero múltiplos, luego beneficios).

## Qué hacer (en términos del embudo)
- Susto: no reducir; añadir en calidad conforme el VIX baje del pico; stops normales.
- Bajista: exposición mínima del régimen; defensivos; esperar a tres señales para volver: HY haciendo techo, peticiones dejando de subir, Fed actuando.
- En duda (dos variables de cada columna): mitad de exposición y resolver con el siguiente dato de empleo y el siguiente HY.

## Episodios
- **Sustos**: febrero 2018 (−10 %), diciembre 2018 (−20 %, en el límite), septiembre 2020 (−10 %), agosto 2024 (−8 %), abril 2025 (−19 %): todos con HY < 450 y peticiones estables; todos recuperados en 1-4 meses.
- **Bajistas**: 2000-2002 (−49 %), 2007-2009 (−57 %), 2022 (−25 %): HY > 500 (salvo 2022, 600 en julio), peticiones subiendo (salvo 2022), Fed subiendo (2022) o crédito roto.
- 2022 es el caso intermedio: mercado bajista por múltiplos (tipo real), sin recesión ni crédito roto; se resolvió cuando el tipo real hizo techo.

## Para profundizar
- Yardeni, tabla histórica de correcciones y mercados bajistas del S&P 500: https://www.yardeni.com/
- Ned Davis Research, estadísticas de correcciones (resúmenes gratuitos)
