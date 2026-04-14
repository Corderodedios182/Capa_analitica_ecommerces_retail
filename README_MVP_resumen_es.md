# Resumen del MVP del Pipeline

Este proyecto construye una capa analítica para reporting de ecommerce retail usando una arquitectura modular: **RAW → STAGING → INTERMEDIATE → MARTS**. El MVP actual valida la capa de entrada, demostrando que los archivos crudos pueden leerse de forma estandarizada y reutilizable antes de persistirlos.

Componentes implementados:
1. **`config.py`** centraliza rutas, metadatos de fuentes, formatos, delimitadores y reglas de negocio compartidas.
2. **`dbt_project.yml`** define la separación de capas en dbt, materializaciones, tests, snapshots y variables configurables.
3. **`file_utils.py`** valida existencia de archivos, lee CSV/Parquet/TXT, normaliza columnas y agrega metadatos de linaje.

La validación en notebook confirmó lecturas exitosas para productos, clientes, devoluciones y órdenes, comprobando que el contrato entre archivos RAW y utilidades de ingesta es estable.

El siguiente hito del MVP es persistir `catalogo_productos.csv` en **SQLite**, exponerlo mediante **dbt sources**, crear `stg_catalogo_productos` y publicar la primera tabla lista para BI: `dim_productos`.

Este enfoque incremental prioriza tener un pipeline funcional extremo a extremo primero, para después escalar a dominios más complejos como unificación de clientes, clasificación de devoluciones y reglas de validez de órdenes.
