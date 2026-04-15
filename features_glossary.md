# Freight Market & Equipment Demand Feature Glossary

This document serves as the data dictionary for the Machine Learning forecasting pipeline. It defines the macroeconomic indicators, engineered features, and target variables used to predict S&OP demand cycles for commercial freight equipment.

## 1. Core Target Variables (The "What")
These are the primary metrics the pipeline is designed to forecast, depending on the specific S&OP business question being asked.

* **`trailer_production_volume`** (FRED: IPG336212S)
    * **Definition:** The Industrial Production Index for Truck Trailer Manufacturing. Measures the physical volume of commercial trailers (dry vans, flatbeds, reefers) rolling off U.S. assembly lines.
    * **S&OP Context:** The ultimate "Ground Truth" for Tier 1 trailer component demand.
* **`heavy_truck_sales`** (FRED: HTRUCKSSAAR)
    * **Definition:** Heavy Weight Truck Retail Sales (Annualized). Tracks the volume of Class 8 tractors sold.
    * **S&OP Context:** The primary indicator for tractor component demand and overall carrier fleet expansion.
* **`target_cass_inferred_rate`** (Engineered Feature)
    * **Definition:** Calculated by dividing `cass_expenditures` (total dollars spent by shippers) by `cass_shipments` (total physical volume moved). 
    * **S&OP Context:** Represents the "spot rate" or average cost to move a load of freight. Often used as a proxy for carrier profitability, though heavily influenced by inflation and fuel surcharges.

## 2. Equipment & Capital Costs (The "Bottlenecks")
These indicators track the capital expenditure required to operate a freight network. In cost-push environments, these dictate carrier behavior more than actual freight demand.

* **`ppi_heavy_truck_cab_mfg`** (FRED: PCU336120336120)
    * **Definition:** Producer Price Index for Heavy Duty Truck Manufacturing. The inflationary cost to build the tractor/cab.
    * **S&OP Context:** A massive leading indicator. If cabs are too expensive or constrained by supply chains, carriers cannot expand fleets, which subsequently suppresses trailer demand (The Complementary Good Effect).
* **`ppi_truck_trailer_mfg`** (FRED: PCU336212336212)
    * **Definition:** Producer Price Index for Truck Trailer Manufacturing. The inflationary cost of the trailer itself.
    * **S&OP Context:** Tracks the pricing power of the OEMs. High PPI here often correlates with severe supply/demand imbalances on the factory floor.

## 3. Manufacturing & Volume Indicators (The "Physical Engine")
These metrics track the actual physical goods moving through the U.S. economy, stripping away the noise of inflation and pricing.

* **`freight_tsi`** (FRED: TSIFRGHT)
    * **Definition:** The Freight Transportation Services Index. Measures the month-to-month change in the volume of services performed by the for-hire transportation sector (tons/miles).
    * **S&OP Context:** Pure physical volume. A high TSI means equipment is actively being utilized, wearing out, and will eventually require replacement.
* **`durable_goods_ex_transport`** (FRED: ADXTNO)
    * **Definition:** Manufacturers' New Orders for Durable Goods (Excluding Transportation). Tracks orders for long-lasting physical products (appliances, machinery) without the volatile swings of commercial aircraft or auto fleet orders.
    * **S&OP Context:** The bedrock of flatbed and heavy-haul freight demand. 
* **`industrial_production`** (FRED: INDPRO)
    * **Definition:** The Industrial Production Index. Measures real output for all facilities located in the United States manufacturing, mining, and electric/gas utilities.
    * **S&OP Context:** A broad health check on the physical economy. 
* **`mfg_employment`** (FRED: MANEMP)
    * **Definition:** All Employees, Manufacturing. 
    * **S&OP Context:** Factories do not hire unless they have sustained order backlogs. A highly reliable, slow-moving indicator of sustained physical output.

## 4. Inventory & Bullwhip Metrics (The "Warehouse Health")
These metrics help identify where freight is physically sitting, which impacts whether carriers are moving goods or using trailers as temporary storage.

* **`retail_inventory_to_sales_ratio`** (FRED: RETAILIRSA)
    * **Definition:** How many months of inventory retailers are holding compared to their current monthly sales pace.
* **`total_inventory_to_sales_ratio`** (FRED: ISRATIO)
    * **Definition:** The aggregate inventory ratio across the entire supply chain (Manufacturing + Wholesale + Retail).
* **`feature_retail_inventory_spread`** (Engineered Feature)
    * **Definition:** `retail_inventory_to_sales_ratio` minus `total_inventory_to_sales_ratio`.
    * **S&OP Context:** Identifies severe Bullwhip Effects. When retail inventory spikes while wholesale/manufacturing drops, distribution centers become bloated. This often forces carriers to use trailers as temporary storage yards, driving up artificial demand for new trailers.

## 5. Raw Materials & Pass-Through Costs (The "Inputs")
Commodity indices that impact both the cost to build equipment and the cost to move it.

* **`diesel_price`** (FRED: GASDESW)
    * **Definition:** U.S. No 2 Diesel Retail Prices.
    * **S&OP Context:** The primary variable operating expense for carriers. Highly correlated with freight rates due to fuel surcharge pass-throughs.
* **`ppi_iron_steel`** (FRED: WPU101) & **`ppi_aluminum_shapes`** (FRED: WPU102501)
    * **Definition:** Producer Price Indices for base metals.
    * **S&OP Context:** Leading indicators for OEM manufacturing costs. Spikes in these commodities will inevitably push `ppi_truck_trailer_mfg` higher.
* **`global_aluminum_price`** (FRED: PALUMUSDM)
    * **Definition:** Global price of Aluminum. 
    * **S&OP Context:** Broader global check against U.S. domestic PPI.

## 6. Macroeconomic & Sentiment Indicators (The "Broad Economy")
General economic health metrics. While popular in media, XGBoost often drops these in favor of more specific manufacturing metrics.

* **`yield_curve_spread`** (FRED: T10Y2Y)
    * **Definition:** 10-Year Treasury Constant Maturity minus 2-Year Treasury. 
    * **S&OP Context:** The classic recession indicator. An inverted curve (negative spread) often precedes capital expenditure freezes by large fleets.
* **`housing_starts`** (FRED: HOUST)
    * **Definition:** New Privately-Owned Housing Units Started.
    * **S&OP Context:** Housing is extremely freight-intensive (lumber, drywall, appliances). A leading indicator for flatbed and dry van demand.
* **`weekly_economic_index`** (FRED: WEI)
    * **Definition:** An index of 10 daily/weekly indicators of real economic activity.
* **`vix_volatility`** (FRED: VIXCLS)
    * **Definition:** CBOE Volatility Index. Market fear/uncertainty.
* **`initial_jobless_claims`** (FRED: ICSA)
    * **Definition:** First-time filings for unemployment insurance.
* **`consumer_sentiment`** (FRED: UMCSENT)
    * **Definition:** University of Michigan Consumer Sentiment Index.

## 7. Carrier Pricing & Alternatives (The "Freight Specifics")
Metrics specifically related to the transportation market's internal dynamics.

* **`rail_intermodal`** (FRED: RAILFRTINTERMODAL)
    * **Definition:** Intermodal traffic (shipping containers/trailers on flatcars).
    * **S&OP Context:** The primary substitute for over-the-road trucking. Drops in intermodal volume often mean freight is spilling over onto the highway network.
* **`target_ppi_dry_van`**, **`target_ppi_ltl_reefer`**, **`target_ppi_flatbed`**
    * **Definition:** Producer Price Indices for specific modes of truck transportation.
    * **S&OP Context:** Mode-specific pricing data. Useful for isolating which specific equipment type (e.g., flatbed vs. reefer) is currently experiencing capacity constraints.