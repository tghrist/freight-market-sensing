# Freight Market Sensing: Multi-Modal Nowcasting & Forecasting

## Project Overview
This project implements a two-stage predictive engine designed for the commercial vehicle and manufacturing industries. By bridging the 45-day reporting lag of traditional government economic data, this tool "senses" current market conditions and forecasts spot rate volatility across three distinct transportation modes: Dry Van, Flatbed, and LTL/Specialized.



The system is built to support Sales & Operations Planning (S&OP) by providing actionable intelligence within the critical 90-day industry horizon.

## The Two-Stage Sensing Engine

### 1. The Nowcast (0-30 Days)
Uses high-frequency "Fast" signals (Diesel prices, Weekly Rail Traffic, VIX) to estimate current market indices before official government releases. This solves the "rearview mirror" problem in logistics planning.

### 2. The Near-Term Forecast (60-90 Days)
Utilizes structural leading indicators (Housing Starts, Durable Goods Orders, Yield Curve) to predict the directional trend and volatility for the upcoming quarter.



## Feature Store (Input Variables)
The model consumes 15+ macroeconomic and industrial indicators sourced primarily from the FRED API.

| ID | Description | Category | Lag |
| :--- | :--- | :--- | :--- |
| **WEI** | Weekly Economic Index | Macro Economics | **Fast (Weekly)** |
| **GASDESW** | Diesel Price | Commodity | **Fast (Weekly)** |
| **RAILFRTINTERMODAL** | Rail Freight Intermodal Traffic | Freight | **Fast (Weekly)** |
| **VIXCLS** | CBOE Volatility Index (VIX) | Sentiment | **Fast (Daily)** |
| **T10Y2Y** | 10Yr - 2Yr Interest Rate Spread | Inflation/Cost | **Fast (Daily)** |
| **ICSA** | Initial Unemployment Claims | Labor Market | **Fast (Weekly)** |
| **HOUST** | Housing Starts | Construction | Medium (Leading) |
| **DGORDER** | New Orders (Durable Goods) | Manufacturing | Medium (Leading) |
| **ADXTNO** | New Orders (Excl. Transp) | Manufacturing | Medium (Leading) |
| **MANEMP** | All Employees: Manufacturing | Labor Market | Medium |
| **UMCSENT** | UofM Consumer Sentiment | Sentiment | Medium |
| **PALUMUSDM** | Global Price of Aluminum | Commodity | Medium |
| **HTRUCKSSAAR** | Heavy Truck Sales | Capital Goods | Medium |
| **INDPRO** | Industrial Production | Manufacturing | Slow (30+ days) |
| **TSIFRGHT** | Freight TSI | Freight | Slow (45+ days) |
| **WPU101** | PPI: Iron and Steel | Raw Materials | Slow (Monthly) |
| **WPU102501** | PPI: Aluminum Mill Shapes | Raw Materials | Slow (Monthly) |
| **PCU3362123362** | PPI Truck Manufacturing | Manufacturing | Slow (Monthly) |
| **RETAILSMPCSM** | Sales/Inventories Ratio | S&OP | Slow (Monthly) |

## Validation Framework (Target Variables)
Model performance is validated against four primary "Ground Truth" indicators.

| ID | Description | Source |
| :--- | :--- | :--- |
| **PCU4841214841212** | PPI: Dry Van (Long-Distance) | FRED |
| **PCU484122484122** | PPI: LTL/Temperature Control | FRED |
| **PCU4842304842306** | PPI: Specialized Freight (Flatbed) | FRED |
| **Inferred Rate** | Cass Expenditures / Cass Shipments | Calculated |

## Technical Implementation
- **Data Engineering:** Automated ETL pipeline using `fredapi` and `pandas`.
- **Normalization:** Z-score scaling and Percent Change transforms to align multi-speed time series.
- **Machine Learning:** Comparison of XGBoost and Time-Series Decomposition models.
- **Visualization:** Interactive dashboarding to visualize "Current Pulse" vs. "Forecasted Trend."

---
*Developed for the AI Industrial Revolution to support data-driven S&OP decision-making.*
