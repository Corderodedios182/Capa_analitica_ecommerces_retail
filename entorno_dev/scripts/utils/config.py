#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Configuración de lectura de archivos.
Entrada al Pipeline

	•   rutas
	•	nombres de archivos
	•	mappings de columnas
	•	regex
	•	constantes

"""
from pathlib import Path
from typing import Dict


BASE_DIR = Path("0_Github/Capa_analitica_ecommerces_retail/entorno_dev").resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
DOCS_DIR = BASE_DIR / "docs"
DBT_PROJECT_DIR = BASE_DIR / "dbt_project" / "mercado"

SOURCES_CONFIG = {
    "clientes_cdmx": {
        "file_name": "clientes_cdmx.csv",
        "path": RAW_DIR / "clientes_cdmx.csv",
        "format": "csv",
        "entity": "clientes",
        "delimiter": ",",
        "encoding": "utf-8",
        "source_partition": "1/3",
        "volume_estimate": 18000,
        "issues": [
            "columnas_en_espanol_con_acentos",
        ],
        "expected_actions": [
            "normalizar_nombres_columnas",
            "remover_acentos",
            "estandarizar_schema_clientes",
        ],
    },
    "clientes_gdl_mty": {
        "file_name": "clientes_gdl_mty.csv",
        "path": RAW_DIR / "clientes_gdl_mty.csv",
        "format": "csv",
        "entity": "clientes",
        "delimiter": ",",
        "encoding": "utf-8",
        "source_partition": "2/3",
        "volume_estimate": 14000,
        "issues": [
            "columnas_en_ingles",
            "tipos_inconsistentes",
        ],
        "expected_actions": [
            "mapear_columnas_a_schema_canonico",
            "corregir_tipos_dato",
            "estandarizar_schema_clientes",
        ],
    },
    "clientes_resto": {
        "file_name": "clientes_resto.parquet",
        "path": RAW_DIR / "clientes_resto.parquet",
        "format": "parquet",
        "entity": "clientes",
        "source_partition": "3/3",
        "volume_estimate": 21000,
        "issues": [
            "telefono_con_extensiones",
            "formato_diferente",
        ],
        "expected_actions": [
            "limpiar_telefono",
            "separar_extension",
            "estandarizar_schema_clientes",
        ],
    },
    "catalogo_productos": {
        "file_name": "catalogo_productos.csv",
        "path": RAW_DIR / "catalogo_productos.csv",
        "format": "csv",
        "entity": "productos",
        "delimiter": ",",
        "encoding": "utf-8",
        "volume_estimate": 4500,
        "issues": [
            "categoria_subcategoria_combinadas",
            "precio_con_simbolo_moneda",
        ],
        "expected_actions": [
            "separar_categoria_subcategoria",
            "limpiar_precio_moneda",
            "convertir_precio_numerico",
        ],
    },
    "ordenes_2022_2023": {
        "file_name": "ordenes_2022_2023.parquet",
        "path": RAW_DIR / "ordenes_2022_2023.parquet",
        "format": "parquet",
        "entity": "ordenes",
        "volume_estimate": 500000,
        "issues": [
            "fechas_en_multiples_formatos",
            "canal_y_estatus_combinados",
        ],
        "expected_actions": [
            "parsear_fechas",
            "separar_canal_estatus",
            "estandarizar_schema_ordenes",
        ],
    },
    "ordenes_2024": {
        "file_name": "ordenes_2024.parquet",
        "path": RAW_DIR / "ordenes_2024.parquet",
        "format": "parquet",
        "entity": "ordenes",
        "volume_estimate": 280000,
        "issues": [
            "schema_modificado",
            "columnas_renombradas",
            "nueva_columna_descuento",
        ],
        "expected_actions": [
            "mapear_a_schema_canonico",
            "alinear_historico",
            "normalizar_descuento",
        ],
    },
    "devoluciones": {
        "file_name": "devoluciones.txt",
        "path": RAW_DIR / "devoluciones.txt",
        "format": "txt",
        "entity": "devoluciones",
        "delimiter": "|",
        "encoding": "utf-8",
        "volume_estimate": 42000,
        "issues": [
            "texto_libre_en_razon_devolucion",
            "requiere_regex",
        ],
        "expected_actions": [
            "parsear_txt_pipe_delimited",
            "clasificar_razon_devolucion",
            "estandarizar_schema_devoluciones",
        ],
    },
}

BUSINESS_RULES = {
    "return_invalidation_days": 30,
    "valid_payment_statuses": [
        "confirmado",
        "confirmed",
        "paid_confirmed",
        "pagado",
    ],
}
