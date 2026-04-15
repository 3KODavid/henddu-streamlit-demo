# Henddu MVP Streamlit Demo

This repository contains the initial V1 skeleton for the Henddu air quality and exposure demo.

## Scope

- CIV first
- ADM1 and ADM2 at every geospatial step
- KPIs, choropleths, animated spatio-temporal maps, trends, and exposure views
- Reusable architecture so the logic can later move into the CTO's web application

## Project Layout

- `app/`: Streamlit entrypoint and pages
- `src/config/`: settings and constants
- `src/data/`: S3 client, readers, and schema helpers
- `src/processing/`: spatial, temporal, and indicator preparation logic
- `src/services/`: app-facing service layer
- `tests/`: initial test targets

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and update values if needed.
4. Start the app with `python -m streamlit run app/streamlit_app.py`.
5. Open the local Streamlit URL shown in the terminal.

## First Launch Notes

- The first CAMS request downloads the GRIB file from S3 into `data/cache/`.
- The first load can take noticeably longer than later page loads.
- Current live indicators are `PM2.5`, `PM10`, `NO2`, and `O3`.
- `Temperature` and `Population Exposure Index` are still pending their ERA5 and WorldPop integration steps.

## Next Build Steps

1. Implement live S3 readers for CAMS, ERA5, boundaries, and WorldPop.
2. Extend the current CAMS pipeline to ERA5 temperature.
3. Add WorldPop-based PEI outputs.
4. Add tests around normalization, aggregation, and service outputs.
