# Entorno de Desarrollo — Prueba Técnica Analytics Engineer

Este entorno es **completamente opcional**. Si prefieres trabajar en tu propio setup local,
eres libre de hacerlo — solo asegúrate de incluir en tu README las instrucciones para
reproducir tu entorno.

Si decides usarlo, tendrás listo en minutos un ambiente con todas las herramientas
configuradas y los datasets disponibles, sin necesidad de instalar nada manualmente.

---

## ¿Qué incluye?

| Herramienta     | Versión  | Para qué                                      |
|-----------------|----------|-----------------------------------------------|
| Python          | 3.11     | Scripts, limpieza, EDA                        |
| pandas          | 2.2      | Manipulación de datos                         |
| PySpark         | 3.5      | Procesamiento del dataset grande de órdenes   |
| DuckDB          | 1.0      | Data Warehouse local                          |
| dbt-duckdb      | 1.8      | Modelado de capas analíticas                  |
| Jupyter Lab     | 4.2      | Notebooks de EDA                              |
| matplotlib / seaborn / plotly | — | Visualizaciones                 |

---

## Requisitos previos

Solo necesitas tener instalado en tu máquina:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows / Mac / Linux)
- Git (opcional, para clonar el repositorio)

---

## Inicio rápido — 3 pasos

### 1. Coloca los datasets en la carpeta correcta

Copia los 7 archivos de datos que recibiste dentro de la carpeta `data/raw/`:

```
entorno_dev/
└── data/
    └── raw/
        ├── clientes_cdmx.csv
        ├── clientes_gdl_mty.csv
        ├── clientes_resto.parquet
        ├── catalogo_productos.csv
        ├── ordenes_2022_2023.parquet
        ├── ordenes_2024.parquet
        └── devoluciones.txt
```

### 2. Construye la imagen (solo la primera vez)

```bash
docker compose build
```

> ⏱ Este paso tarda entre 5 y 10 minutos la primera vez porque descarga e instala
> todas las dependencias. Las siguientes veces el arranque es inmediato.

### 3. Levanta el entorno

```bash
docker compose up
```

Abre tu navegador en **http://localhost:8888** y tendrás Jupyter Lab listo.

---

## Estructura de carpetas de trabajo

```
entorno_dev/
├── data/
│   ├── raw/               ← Datasets originales (solo lectura)
│   └── warehouse/         ← Aquí se genera el archivo mercado.duckdb
├── notebooks/             ← Tus notebooks de EDA van aquí
├── scripts/               ← Tus scripts .py van aquí
├── sql/                   ← Tus archivos .sql van aquí
└── dbt_project/           ← Tu proyecto dbt va aquí
```

Todo lo que escribas en estas carpetas **persiste en tu máquina** aunque apagues
o destruyas el contenedor.

---

## Usar dbt dentro del contenedor

Abre una terminal dentro del contenedor:

```bash
docker compose exec workspace bash
```

El proyecto dbt ya está pre-inicializado en `/workspace/dbt_project/mercado/`.
**No ejecutes `dbt init`** — el perfil y la estructura ya están listos.

Desde ahí puedes ejecutar cualquier comando dbt:

```bash
# Primer paso: verificar que la conexión a DuckDB funciona
cd /workspace/dbt_project/mercado
dbt debug

# Ejecutar modelos
dbt run

# Ejecutar tests
dbt test

# Generar y servir documentación (http://localhost:8080)
dbt docs generate && dbt docs serve --port 8080
```

---

## Usar PySpark dentro del contenedor

PySpark está listo para usarse sin configuración adicional.
En cualquier script o notebook:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MercadoAnalytics") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read.parquet("/workspace/data/raw/ordenes_2022_2023.parquet")
df.printSchema()
```

---

## Variables de negocio configurables

El archivo `profiles.yml` incluye las variables de negocio clave de la prueba.
Puedes modificarlas sin tocar ningún modelo:

```yaml
vars:
  plazo_devolucion_dias: 30          # Regla 1: plazo para invalidar orden por devolución
  ventana_cliente_activo_meses: 12   # Regla 4: ventana para considerar cliente activo
  umbral_recompra_dias: 7            # Regla 7: días mínimos entre órdenes para recompra
```

Para pasar estas variables al ejecutar dbt:

```bash
dbt run --vars '{"plazo_devolucion_dias": 15}'
```

---

## Apagar el entorno

```bash
# Detener sin borrar nada
docker compose down

# Detener y limpiar la imagen (si quieres liberar espacio en disco)
docker compose down --rmi all
```

---

## Preguntas frecuentes

**¿Puedo usar VS Code en lugar de Jupyter?**
Sí. VS Code con la extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
puede conectarse directamente al contenedor. Tu código seguirá persistiendo en las
mismas carpetas.

**¿El contenedor tiene acceso a internet?**
Sí, puedes instalar librerías adicionales con `pip install` desde dentro del contenedor.
Si necesitas que persistan, agrégalas a `requirements.txt` y reconstruye con `docker compose build`.

**¿Qué pasa si el puerto 8888 ya está ocupado en mi máquina?**
Cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "9999:8888"   # Accede desde http://localhost:9999
```

**¿Funciona en Windows?**
Sí, con Docker Desktop para Windows. Asegúrate de tener habilitada la virtualización
en tu BIOS y WSL 2 activado.

---

## Tamaño estimado

| Componente            | Tamaño aprox. |
|-----------------------|---------------|
| Imagen Docker base    | ~800 MB       |
| Datasets en `data/raw`| ~60 MB        |
| Warehouse generado    | Crece según tu trabajo |

> Si el tamaño de la imagen es un inconveniente, contacta al equipo de reclutamiento
> para recibir la imagen pre-construida vía Sharepoint en lugar de construirla tú mismo.

---

*Cualquier duda técnica sobre el entorno, escríbenos antes de que se agote tu tiempo.
No queremos que la configuración te quite horas de las 72 disponibles.*
