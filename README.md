# Resumen del MVP del Pipeline

Este proyecto construye una capa analítica para reporting de ecommerce retail usando una arquitectura modular: **RAW → STAGING → INTERMEDIATE → MARTS**. El MVP actual ya superó la validación de la capa de entrada y evolucionó a una **capa STAGING unificada por dominio**, demostrando que los archivos crudos pueden leerse, homologarse y transformarse en entidades canónicas reutilizables antes de persistirlos.

Componentes implementados:
1. **`config.py`** centraliza rutas, metadatos de fuentes, formatos, delimitadores y reglas de negocio compartidas.
2. **`dbt_project.yml`** define la separación de capas en dbt, materializaciones, tests, snapshots y variables configurables.
3. **`file_utils.py`** valida existencia de archivos, lee CSV/Parquet/TXT, normaliza columnas y agrega metadatos de linaje.
4. **`01_validacion_file_utils.ipynb`** notebook para validar el proceso técnico y los pipelines.
5. **`unify_clientes.py`** unifica múltiples fuentes de clientes en `stg_clientes`.
6. **`unify_ordenes.py`** unifica fuentes históricas y actuales en `stg_ordenes`.
7. **`int_ordenes_validas.py`** implementa la regla de negocio de validez de órdenes en la capa INTERMEDIATE.

La validación en notebook confirmó lecturas exitosas para productos, clientes, devoluciones y órdenes, así como la correcta homologación de **`stg_clientes`**, **`stg_ordenes`** y **`stg_catalogo`**, comprobando que el contrato entre archivos RAW y la capa STAGING es estable.

El siguiente hito del MVP es persistir las entidades canónicas en **SQLite**, exponerlas mediante **dbt sources**, migrar la lógica reusable de **INTERMEDIATE** a modelos dbt y publicar las primeras tablas BI-ready como **`dim_clientes`**, **`dim_productos`** y **`fct_ordenes`**.

Este enfoque incremental prioriza tener un pipeline funcional extremo a extremo primero, para después escalar a dominios más complejos como devoluciones, enriquecimiento de órdenes y marts analíticos ejecutivos.