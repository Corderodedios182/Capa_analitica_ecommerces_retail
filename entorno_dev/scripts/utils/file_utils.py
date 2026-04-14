#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrip con funciones de apoyo para lectura.
"""

from pathlib import Path
from typing import Dict

import pandas as pd

from scripts.utils.config import SOURCES_CONFIG


def file_exists(file_path: Path) -> bool:
    return file_path.exists()


def validate_source_exists(source_name: str) -> None:
    if source_name not in SOURCES_CONFIG:
        raise KeyError(f"Fuente no configurada: {source_name}")

    file_path = SOURCES_CONFIG[source_name]["path"]

    if not file_exists(file_path):
        raise FileNotFoundError(
            f"No se encontró el archivo para la fuente '{source_name}': {file_path}"
        )


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def read_csv_file(source_config: Dict) -> pd.DataFrame:
    return pd.read_csv(
        source_config["path"],
        delimiter=source_config.get("delimiter", ","),
        encoding=source_config.get("encoding", "utf-8"),
    )


def read_parquet_file(source_config: Dict) -> pd.DataFrame:
    return pd.read_parquet(source_config["path"])


def read_txt_file(source_config: Dict) -> pd.DataFrame:
    return pd.read_csv(
        source_config["path"],
        delimiter=source_config.get("delimiter", "|"),
        encoding=source_config.get("encoding", "utf-8"),
    )


def read_source(source_name: str) -> pd.DataFrame:
    validate_source_exists(source_name)

    source_config = SOURCES_CONFIG[source_name]
    file_format = source_config["format"]

    if file_format == "csv":
        df = read_csv_file(source_config)

    elif file_format == "parquet":
        df = read_parquet_file(source_config)

    elif file_format == "txt":
        df = read_txt_file(source_config)

    else:
        raise ValueError(
            f"Formato no soportado para la fuente '{source_name}': {file_format}"
        )

    df = normalize_columns(df)
    df["source_name"] = source_name

    return df


