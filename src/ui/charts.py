"""Chart builders used by the Streamlit demo pages."""

from __future__ import annotations

import json

import geopandas as gpd
import pandas as pd
import plotly.express as px


def _get_unit_label(metrics: pd.DataFrame) -> str:
    if "unit" in metrics.columns and not metrics["unit"].dropna().empty:
        return str(metrics["unit"].dropna().iloc[0])
    return "value"


def _build_hover_data(metrics: pd.DataFrame, animation: bool = False) -> dict[str, object]:
    hover_data: dict[str, object] = {}
    if "admin_code" in metrics.columns:
        hover_data["admin_code"] = True
    if "value" in metrics.columns:
        hover_data["value"] = ":.2f"
    if "unit" in metrics.columns:
        hover_data["unit"] = True
    if animation:
        if "animation_frame" in metrics.columns:
            hover_data["animation_frame"] = True
    elif "date" in metrics.columns:
        hover_data["date"] = True
    return hover_data


def build_choropleth_figure(boundaries: gpd.GeoDataFrame, metrics: pd.DataFrame, title: str):
    if boundaries.empty or metrics.empty:
        return None

    unit_label = _get_unit_label(metrics)
    hover_data = _build_hover_data(metrics, animation=False)
    geojson = json.loads(boundaries[["admin_code", "geometry"]].to_json())
    figure = px.choropleth_mapbox(
        metrics,
        geojson=geojson,
        locations="admin_code",
        featureidkey="properties.admin_code",
        color="value",
        hover_name="admin_name",
        hover_data=hover_data,
        mapbox_style="carto-positron",
        center={"lat": 7.54, "lon": -5.55},
        zoom=5.2,
        opacity=0.7,
        title=title,
        labels={"value": f"Value ({unit_label})"},
    )
    return figure


def build_animation_figure(boundaries: gpd.GeoDataFrame, metrics: pd.DataFrame, title: str):
    if boundaries.empty or metrics.empty:
        return None

    unit_label = _get_unit_label(metrics)
    animation_metrics = metrics.copy()
    animation_metrics["animation_frame"] = animation_metrics["date"].astype(str)
    hover_data = _build_hover_data(animation_metrics, animation=True)
    geojson = json.loads(boundaries[["admin_code", "geometry"]].to_json())
    figure = px.choropleth_mapbox(
        animation_metrics,
        geojson=geojson,
        locations="admin_code",
        featureidkey="properties.admin_code",
        color="value",
        hover_name="admin_name",
        hover_data=hover_data,
        animation_frame="animation_frame",
        mapbox_style="carto-positron",
        center={"lat": 7.54, "lon": -5.55},
        zoom=5.2,
        opacity=0.7,
        title=title,
        labels={"value": f"Value ({unit_label})"},
    )
    return figure


def build_timeseries_figure(metrics: pd.DataFrame, title: str):
    if metrics.empty:
        return None
    unit_label = _get_unit_label(metrics)
    return px.line(
        metrics.sort_values("date"),
        x="date",
        y="value",
        color="admin_name",
        title=title,
        markers=True,
        labels={"value": f"Value ({unit_label})", "date": "Date"},
    )


def build_top_regions_figure(metrics: pd.DataFrame, title: str):
    if metrics.empty:
        return None
    unit_label = _get_unit_label(metrics)
    return px.bar(
        metrics,
        x="mean_value",
        y="admin_name",
        orientation="h",
        title=title,
        labels={"mean_value": f"Mean value ({unit_label})", "admin_name": "Region"},
    )
