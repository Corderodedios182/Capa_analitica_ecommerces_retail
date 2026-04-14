#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:47:57 2026

@author: carlosrobertofloresluna
"""

import re
import pandas as pd


def split_phone_extension(phone_value):
    if pd.isna(phone_value):
        return None, None

    phone_str = str(phone_value).strip()

    ext_match = re.search(r"(?:ext\.?|extension)\s*(\d+)", phone_str, flags=re.IGNORECASE)
    extension = ext_match.group(1) if ext_match else None

    phone_clean = re.sub(r"(?:ext\.?|extension)\s*\d+", "", phone_str, flags=re.IGNORECASE).strip()
    return phone_clean, extension


def to_datetime_safe(series, dayfirst=False, unit=None):
    return pd.to_datetime(series, errors="coerce", dayfirst=dayfirst, unit=unit)


def normalize_gender(value):
    if pd.isna(value):
        return None
    v = str(value).strip().upper()
    if v in {"M", "F"}:
        return v
    return None


def normalize_active(value):
    if pd.isna(value):
        return 0
    if str(value).strip().lower() in {"true", "1", "yes"}:
        return 1
    return int(float(value)) if str(value).strip().replace(".", "", 1).isdigit() else 0


def normalize_zip(value):
    if pd.isna(value):
        return None
    value_str = str(value).strip()
    if value_str.endswith(".0"):
        value_str = value_str[:-2]
    return value_str


def unify_clientes(df_cdmx, df_gdl_mty, df_resto):
    # -----------------------------
    # clientes_cdmx
    # -----------------------------
    cdmx = df_cdmx.copy()

    cdmx[["telefono", "extension_telefono"]] = cdmx["telefono"].apply(
        lambda x: pd.Series(split_phone_extension(x))
    )

    cdmx["fecha_registro"] = to_datetime_safe(cdmx["fecha_registro"])
    cdmx["genero"] = cdmx["genero"].apply(normalize_gender)
    cdmx["activo_flag"] = cdmx["activo_flag"].apply(normalize_active)
    cdmx["codigo_postal"] = cdmx["codigo_postal"].apply(normalize_zip)

    cdmx["nombre_completo"] = (
        cdmx["nombre"].fillna("").str.strip() + " " +
        cdmx["apellido_paterno_materno"].fillna("").str.strip()
    ).str.strip()

    cdmx["municipio"] = cdmx["alcaldía_municipio"]

    cdmx = cdmx.rename(columns={
        "cliente_id": "cliente_id",
        "nombre": "nombre",
        "apellido_paterno_materno": "apellido",
        "email": "email",
        "genero": "genero",
        "fecha_registro": "fecha_registro",
        "estado": "estado",
        "telefono": "telefono",
        "codigo_postal": "codigo_postal",
        "activo_flag": "activo_flag",
        "source_name": "source_name",
    })

    cdmx = cdmx[
        [
            "cliente_id",
            "nombre",
            "apellido",
            "nombre_completo",
            "email",
            "genero",
            "fecha_registro",
            "estado",
            "telefono",
            "extension_telefono",
            "codigo_postal",
            "activo_flag",
            "municipio",
            "source_name",
        ]
    ]

    # -----------------------------
    # clientes_gdl_mty
    # -----------------------------
    gdl = df_gdl_mty.copy()

    gdl[["phone", "extension_telefono"]] = gdl["phone"].apply(
        lambda x: pd.Series(split_phone_extension(x))
    )

    gdl["registration_date"] = to_datetime_safe(gdl["registration_date"], dayfirst=True)
    gdl["gender"] = gdl["gender"].apply(normalize_gender)
    gdl["is_active"] = gdl["is_active"].apply(normalize_active)
    gdl["zip_code"] = gdl["zip_code"].apply(normalize_zip)

    gdl["nombre_completo"] = (
        gdl["first_name"].fillna("").str.strip() + " " +
        gdl["last_name"].fillna("").str.strip()
    ).str.strip()

    gdl["municipio"] = None

    gdl = gdl.rename(columns={
        "customer_id": "cliente_id",
        "first_name": "nombre",
        "last_name": "apellido",
        "email_address": "email",
        "gender": "genero",
        "registration_date": "fecha_registro",
        "state": "estado",
        "phone": "telefono",
        "zip_code": "codigo_postal",
        "is_active": "activo_flag",
        "source_name": "source_name",
    })

    gdl = gdl[
        [
            "cliente_id",
            "nombre",
            "apellido",
            "nombre_completo",
            "email",
            "genero",
            "fecha_registro",
            "estado",
            "telefono",
            "extension_telefono",
            "codigo_postal",
            "activo_flag",
            "municipio",
            "source_name",
        ]
    ]

    # -----------------------------
    # clientes_resto
    # -----------------------------
    resto = df_resto.copy()

    resto[["telefono", "extension_telefono"]] = resto["telefono"].apply(
        lambda x: pd.Series(split_phone_extension(x))
    )

    resto["fecha_registro"] = to_datetime_safe(resto["fecha_registro"], unit="s")
    resto["genero"] = resto["genero"].apply(normalize_gender)
    resto["activo_flag"] = resto["activo_flag"].apply(normalize_active)
    resto["codigo_postal"] = resto["codigo_postal"].apply(normalize_zip)

    resto["nombre_completo"] = resto["nombre_completo"].astype(str).str.strip()
    resto["nombre"] = resto["nombre_completo"].str.split().str[0]
    resto["apellido"] = resto["nombre_completo"].str.split().str[1:].str.join(" ")
    resto["municipio"] = None

    resto = resto.rename(columns={
        "cliente_id": "cliente_id",
        "email": "email",
        "genero": "genero",
        "fecha_registro": "fecha_registro",
        "estado": "estado",
        "telefono": "telefono",
        "codigo_postal": "codigo_postal",
        "activo_flag": "activo_flag",
        "source_name": "source_name",
    })

    resto = resto[
        [
            "cliente_id",
            "nombre",
            "apellido",
            "nombre_completo",
            "email",
            "genero",
            "fecha_registro",
            "estado",
            "telefono",
            "extension_telefono",
            "codigo_postal",
            "activo_flag",
            "municipio",
            "source_name",
        ]
    ]

    # -----------------------------
    # unión final
    # -----------------------------
    clientes_unificados = pd.concat([cdmx, gdl, resto], ignore_index=True)

    clientes_unificados["cliente_id"] = clientes_unificados["cliente_id"].astype(str).str.strip()
    clientes_unificados["email"] = clientes_unificados["email"].replace({"None": None})
    clientes_unificados["telefono"] = clientes_unificados["telefono"].astype("string")
    clientes_unificados["extension_telefono"] = clientes_unificados["extension_telefono"].astype("string")
    clientes_unificados["codigo_postal"] = clientes_unificados["codigo_postal"].astype("string")
    clientes_unificados["activo_flag"] = clientes_unificados["activo_flag"].fillna(0).astype(int)

    return clientes_unificados
