# Áreas inundadas por municipio — Frente frío, febrero de 2026

Observatorio geoespacial web **estático**, listo para GitHub Pages. La app incluye el Excel real y su exportación procesada a JSON, filtros, estadísticas ponderadas, ranking, gráficos, tabla descargable y soporte para dos capas GeoJSON. **Los GeoJSON no se suministraron y no están incluidos**: hasta agregarlos el mapa muestra una advertencia, sin inventar polígonos.

## Abrir localmente

1. Descarga y extrae toda la carpeta.
2. Abre una terminal dentro de `inundaciones-colombia`.
3. Ejecuta `python -m http.server 8000` (en Windows también puedes usar `py -m http.server 8000`).
4. Visita `http://localhost:8000`.

No abras `index.html` directamente con doble clic, porque el navegador bloqueará `fetch` de los JSON locales.

Requiere conexión a internet para cargar Leaflet, Chart.js, SheetJS y la cartografía base OSM desde CDN. El proyecto **no exige npm ni un servidor backend**. En GitHub Pages funciona directamente.

## Agregar límites geográficos

Coloca en la carpeta `data/`:

- `municipios.geojson` (FeatureCollection con polígonos municipales).
- `departamentos.geojson` (FeatureCollection con polígonos departamentales).

Se aceptan diversos campos habituales como `MPIO_CNMBR`, `NOM_MPIO`, `Municipio`, `DPTO_CNMBR`, `NOM_DPTO`, `Departamento`, `NAME_1`, `NAME_2`. El sistema utiliza departamento + municipio y usa solo el nombre cuando es único en el conjunto registrado. **Revisa el resumen de coincidencias**; si tu GeoJSON tiene esquemas de columnas distintos, actualiza las listas `MUNIC` y `DEPT` dentro de `app.js`. En el futuro se recomienda incorporar códigos oficiales DANE para enlaces robustos.

## Publicar en GitHub Pages

1. Crea un repositorio público en GitHub (por ejemplo `inundaciones-colombia`).
2. Sube **todo el contenido de esta carpeta**, incluida `.github/workflows/deploy.yml`.
3. En **Settings → Pages → Build and deployment → Source**, selecciona **GitHub Actions**.
4. En **Actions**, verifica que el workflow terminó correctamente.
5. Visita `https://TU-USUARIO.github.io/inundaciones-colombia/`.

Las rutas son relativas, por lo que se adaptan al nombre de cualquier repositorio.

## Actualizar datos del Excel

El archivo de origen es `Areas_Inundadas_Municipios_Frente_Frio.xlsx`, hoja `Orden x dpto`, con columnas `Municipio`, `Departamento`, `Area_Municipio_ha`, `Area_Inundada_ha` y `%_Area_inundada`. Para regenerar el JSON tras reemplazar el Excel:

```bash
pip install artifact-tool
python scripts/preparar_datos.py
```

Luego sube `data/inundaciones.json` y `data/validacion.json` actualizados y haz commit. La compilación de Pages no requiere Python porque publica los datos previamente generados.

**Nota:** el script lee las primeras 999 filas de datos de la hoja; amplía el rango si tu próxima versión excede esa capacidad.

## Criterios y limitaciones

- Se analizaron 180 registros en nueve departamentos y se cuantificaron 285.168,5166 ha inundadas.
- El porcentaje agregado es `100 * sum(Area_Inundada_ha)/sum(Area_Municipio_ha)` sobre los municipios incluidos.
- El histograma utiliza clases exploratorias, no umbrales oficiales de riesgo.
- Los municipios que no figuran en el Excel se muestran como «sin información» y no como inundación cero.
- El mapa usa polígonos administrativos *como coropleta*. No delimita los polígonos reales de inundación.
- Se han implementado y verificado validaciones numéricas del Excel, pero la correspondencia con los GeoJSON solo podrá revisarse cuando se agreguen las capas reales.
- La procedencia institucional y la fecha precisa de obtención del conjunto de datos no fueron especificadas.

## Archivos

- `index.html`: interfaz.
- `style.css`: diseño adaptable y tema oscuro.
- `app.js`: filtros, estadísticas, Leaflet, gráficos y exportaciones.
- `data/inundaciones.json`: 180 filas reales procesadas.
- `data/validacion.json`: informe de calidad numérica.
- `scripts/preparar_datos.py`: conversión y comprobaciones.
- `.github/workflows/deploy.yml`: publicación automática desde la rama `main`.

No se requiere React ni Vite porque la publicación elegida es una aplicación estática sin compilación, lo que simplifica el despliegue en GitHub Pages. Usa Leaflet y Chart.js como dependencias web.


## Capas geográficas integradas

Se incluyen `data/municipios.geojson` (1.122 geometrías, atributos `MpNombre`, `MpCodigo`, `Depto`) y `data/departamentos.geojson` (34 geometrías, atributos `DeNombre`, `DeCodigo`). El cruce exacto normalizado por departamento y municipio coincide con los 180 registros del Excel. Los 34 polígonos departamentales incluyen una entidad territorial especial en litigio, que se conserva tal como aparece en la fuente. Véase `data/validacion_geografica.json`. Los mapas municipales representan estadísticas agregadas y no el contorno efectivo del agua.
