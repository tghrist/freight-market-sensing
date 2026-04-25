# Freight Market Sensing: Physics-Based S&OP Capacity Forecasting

## Project Overview
This project implements a machine learning forecasting pipeline designed specifically for the heavy commercial vehicle and trailer manufacturing industries. By filtering out macroeconomic noise and focusing on the physical "lead-lag" reality of the U.S. freight network, this tool predicts the 90-day forward baseline for commercial equipment demand. 

The system acts as an unbiased, data-driven constraint for Sales & Operations Planning (S&OP). It is explicitly designed to identify when internal sales surges are driven by "Borrowed Demand" (regulatory pull-forwards or panic buying) versus true macroeconomic recovery, preventing factories from over-leveraging their cost structures during temporary bubbles.

## The Architecture: The "Category Champion" Strategy
Feeding an XGBoost model dozens of raw, highly correlated economic indicators typically results in "coincident traps" and the memorization of historical anomalies (like the 2020-2021 COVID-19 supply chain crisis). 

To solve this, this pipeline utilizes a **SHAP (SHapley Additive exPlanations) Value Tournament**. 

We organized 25+ macroeconomic indicators into six distinct logical "Categories" that govern supply chain physics. The model evaluates every feature within a category and drafts a single "Champion" indicator—the one that provides the cleanest, most mathematically sound predictive signal without falling into historical traps.

### The 6 S&OP Feature Categories
1. **Equipment Pricing:** The capital bottlenecks (cost to build and buy).
2. **Raw Materials:** The upstream input costs.
3. **Physical Output:** The actual volume of goods manufactured across the U.S.
4. **Supply Chain Bullwhip:** Inventory-to-Sales ratios identifying where freight is trapped.
5. **Macro Sentiment:** The psychological and leading economic indicators.
6. **Carrier Pricing:** The dynamics of the transportation spot and contract markets.

## The Feature Roster
After running the SHAP tournament and applying a Pearson Correlation filter to eliminate multicollinearity (e.g., stripping out redundant inflation signals), the model relies on these highly independent, foundational pillars of the economy:

| Category | Champion Feature | FRED Series ID | Predictive Role |
| :--- | :--- | :--- | :--- |
| **Physical Output** | Industrial Production | `INDPRO` | The broad Macro Anchor |
| **Carrier Pricing** | Cass Freight Shipments | `FRGSHPUSM649NCIS` | The Physical Volume Driver |
| **Equipment Pricing** | PPI: Heavy Truck Cabs | `PCU336120336120` | The Capital Cost Constraint |
| **Supply Chain Bullwhip** | Mfg Inventory-to-Sales | `MNFCTRIRSA` | The Supply Chain Choke Point |
| **Macro Sentiment** | Consumer Sentiment | `UMCSENT` | The Psychological Leading Proxy |

## Target Variable & The "Delta" Fix
**Target:** `IPG336212S` (Industrial Production: Truck Trailer Manufacturing)
*Note: This is a Seasonally Adjusted Index where 2017 = 100, measuring relative market velocity rather than absolute unit counts.*

**The Extrapolation Problem:** Tree-based models (like XGBoost) cannot extrapolate to predict unprecedented market lows or highs if they haven't seen them in the training data. 
**The Delta Solution:** Instead of predicting absolute volume, the engine time-shifts the data and predicts the **90-Day Forward Percentage Change (Delta)**. It then reconstructs that percentage back into the 2017 baseline index. This allows the model to accurately forecast massive market crashes and recoveries based on the *rate of change* in the Champion Features.

## Technical Implementation
- **Data Engineering:** Automated ETL pipeline using `fredapi` and `pandas`.
- **Feature Selection:** Iterative SHAP value analysis and Pearson correlation matrices.
- **Machine Learning Engine:** `xgboost.XGBRegressor` utilizing chronological training splits to prevent data leakage (time travel).
- **Time-Shifting:** Built-in 90-day target lagging to transform the model from a "Nowcast" into a true predictive S&OP tool. 

---
*Developed to bridge the gap between macroeconomic data and physical manufacturing reality.*