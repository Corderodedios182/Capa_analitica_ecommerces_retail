#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:49:12 2026

@author: carlosrobertofloresluna
"""

import pandas as pd


def to_datetime_multi(series):
    parsed = pd.to_datetime(series, errors="coerce", format="mixed")
    return parsed


def normalize_text(value):
    if pd.isna(value):
        return None
    return str(value).strip().lower()


def split_canal_estatus(value):
    if pd.isna(value):
        return None, None

    value_str = str(value).strip()

    if "|" in value_str:
        parts = value_str.split("|", 1)
        canal = normalize_text(parts[0])
        estatus = normalize_text(parts[1])
        return canal, estatus

    return normalize_text(value_str), None


def normalize_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def unify_ordenes(df_2022_2023, df_2024):
    # -----------------------------
    # ordenes_2022_2023
    # -----------------------------
    hist = df_2022_2023.copy()

    hist[["canal_venta", "estatus_pago"]] = hist["canal_estatus"].apply(
        lambda x: pd.Series(split_canal_estatus(x))
    )

    hist["fecha_orden"] = to_datetime_multi(hist["fecha_orden"])
    hist["fecha_actualizacion"] = to_datetime_multi(hist["fecha_actualizacion"])
    hist["monto_total"] = normalize_numeric(hist["monto_total"])
    hist["cantidad"] = normalize_numeric(hist["cantidad"])
    hist["descuento_aplicado"] = 0.0

    hist = hist.rename(columns={
        "order_id": "order_id",
        "id_cliente": "cliente_id",
        "sku_producto": "sku_producto",
        "direccion_entrega": "direccion_entrega",
        "source_name": "source_name",
    })

    hist = hist[
        [
            "order_id",
            "cliente_id",
            "sku_producto",
            "canal_venta",
            "estatus_pago",
            "fecha_orden",
            "monto_total",
            "cantidad",
            "direccion_entrega",
            "descuento_aplicado",
            "fecha_actualizacion",
            "source_name",
        ]
    ]

    # -----------------------------
    # ordenes_2024
    # -----------------------------
    current = df_2024.copy()

    current["canal_venta"] = current["canal_venta"].apply(normalize_text)
    current["estatus_pago"] = current["estatus_pago"].apply(normalize_text)
    current["fecha_orden"] = to_datetime_multi(current["fecha_compra"])
    current["fecha_actualizacion"] = to_datetime_multi(current["fecha_modificacion"])
    current["monto_total"] = normalize_numeric(current["monto"])
    current["cantidad"] = normalize_numeric(current["cantidad_unidades"])
    current["descuento_aplicado"] = normalize_numeric(current["descuento_aplicado"])

    current = current.rename(columns={
        "orden_id": "order_id",
        "cliente_id": "cliente_id",
        "producto_sku": "sku_producto",
        "domicilio_entrega": "direccion_entrega",
        "source_name": "source_name",
    })

    current = current[
        [
            "order_id",
            "cliente_id",
            "sku_producto",
            "canal_venta",
            "estatus_pago",
            "fecha_orden",
            "monto_total",
            "cantidad",
            "direccion_entrega",
            "descuento_aplicado",
            "fecha_actualizacion",
            "source_name",
        ]
    ]

    # -----------------------------
    # unión final
    # -----------------------------
    ordenes_unificadas = pd.concat([hist, current], ignore_index=True)

    ordenes_unificadas["order_id"] = ordenes_unificadas["order_id"].astype(str).str.strip()
    ordenes_unificadas["cliente_id"] = ordenes_unificadas["cliente_id"].astype(str).str.strip()
    ordenes_unificadas["sku_producto"] = ordenes_unificadas["sku_producto"].astype(str).str.strip()
    ordenes_unificadas["canal_venta"] = ordenes_unificadas["canal_venta"].astype("string")
    ordenes_unificadas["estatus_pago"] = ordenes_unificadas["estatus_pago"].astype("string")
    ordenes_unificadas["direccion_entrega"] = ordenes_unificadas["direccion_entrega"].astype("string")
    ordenes_unificadas["monto_total"] = ordenes_unificadas["monto_total"].astype(float)
    ordenes_unificadas["cantidad"] = ordenes_unificadas["cantidad"].astype("Int64")
    ordenes_unificadas["descuento_aplicado"] = ordenes_unificadas["descuento_aplicado"].fillna(0.0).astype(float)

    return ordenes_unificadas
