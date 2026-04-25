# Freight Market & Equipment Demand Feature Glossary

This document serves as the data dictionary for the Machine Learning forecasting pipeline. It defines the macroeconomic indicators, engineered features, and target variables used to predict S&OP demand cycles for commercial freight equipment.

## Targets (The "What")
These are the primary metrics the pipeline is designed to forecast.

* **`trailer_production_volume`** (FRED: IPG336212S)
    * **Definition:** The Industrial Production Index for Truck Trailer Manufacturing (2017=100). Measures the relative physical volume of commercial trailers rolling off U.S. assembly lines.
    * **S&OP Context:** The ultimate "Ground Truth" for Tier 1 trailer component demand.
* **`heavy_truck_sales`** (FRED: HTRUCKSSAAR)
    * **Definition:** Heavy Weight Truck Retail Sales (Annualized). Tracks the volume of Class 8 tractors sold.
    * **S&OP Context:** The primary indicator for tractor component demand and overall carrier fleet expansion.

## 1. Equipment Pricing (The "Capital Bottlenecks")
These indicators track the capital expenditure required to operate a freight network. In cost-push environments, these dictate carrier behavior more than actual freight demand.

* **`ppi_heavy_truck_cab_mfg`** (FRED: PCU336120336120)
    * **Definition:** Producer Price Index for Heavy Duty Truck Manufacturing. The inflationary cost to build the tractor/cab.
    * **S&OP Context:** A massive leading indicator. If cabs are too expensive or constrained by supply chains, carriers cannot expand fleets, which suppresses trailer demand.
* **`ppi_truck_trailer_mfg`** (FRED: PCU336212336212)
    * **Definition:** Producer Price Index for Truck Trailer Manufacturing. The inflationary cost of the trailer itself.
    * **S&OP Context:** Tracks the pricing power of the OEMs. High PPI here often correlates with severe supply/demand imbalances.
* **`ppi_motor_vehicle_parts`** (FRED: PCU33633363)
    * **Definition:** Producer Price Index for Motor Vehicle Parts Manufacturing.
    * **S&OP Context:** Tracks inflationary cost pressures deeper within the Tier 1 and Tier 2 supply base.
* **`ppi_general_machinery`** (FRED: WPU111)
    * **Definition:** Producer Price Index for General Purpose Machinery and Equipment.
    * **S&OP Context:** A broader proxy for industrial capital equipment inflation across the U.S. economy.
* **`ppi_material_handling_equip`** (FRED: PCU333924333924)
    * **Definition:** Producer Price Index for Material Handling Equipment (e.g., forklifts, conveyors).
    * **S&OP Context:** Tracks the cost of expanding physical warehouse infrastructure, which heavily correlates with distribution center capacity and trailer storage needs.

## 2. Raw Materials (The "Inputs")
Commodity indices that impact both the cost to build equipment and the cost to move it.

* **`global_aluminum_price`** (FRED: PALUMUSDM)
    * **Definition:** Global price of Aluminum. 
    * **S&OP Context:** Broader global check against U.S. domestic PPI.
* **`ppi_aluminum_shapes`** (FRED: WPU102501)
    * **Definition:** Producer Price Index for Aluminum Extruded Shapes.
    * **S&OP Context:** Leading indicator for OEM manufacturing costs, particularly for dry van and reefer construction.
* **`ppi_iron_steel`** (FRED: WPU101) 
    * **Definition:** Producer Price Index for Iron and Steel.
    * **S&OP Context:** Core structural cost indicator for heavy manufacturing.
* **`diesel_price`** (FRED: GASDESW)
    * **Definition:** U.S. No 2 Diesel Retail Prices.
    * **S&OP Context:** The primary variable operating expense for carriers. Highly correlated with freight rates due to fuel surcharge pass-throughs.

## 3. Physical Output (The "Physical Engine")
These metrics track the actual physical goods moving through the U.S. economy, stripping away the noise of inflation and pricing.

* **`industrial_production`** (FRED: INDPRO)
    * **Definition:** The Industrial Production Index. Measures real output for all facilities located in the United States manufacturing, mining, and electric/gas utilities.
    * **S&OP Context:** A broad health check on the physical economy. 
* **`freight_tsi`** (FRED: TSIFRGHT)
    * **Definition:** The Freight Transportation Services Index. Measures the month-to-month change in the volume of services performed by the for-hire transportation sector (tons/miles).
    * **S&OP Context:** Pure physical volume. A high TSI means equipment is actively being utilized and will eventually require replacement.
* **`rail_intermodal`** (FRED: RAILFRTINTERMODAL)
    * **Definition:** Intermodal traffic (shipping containers/trailers on flatcars).
    * **S&OP Context:** The primary substitute for over-the-road trucking. Drops in intermodal volume often mean freight is spilling over onto the highway network.
* **`durable_goods_ex_transport`** (FRED: ADXTNO)
    * **Definition:** Manufacturers' New Orders for Durable Goods (Excluding Transportation). 
    * **S&OP Context:** Tracks orders for long-lasting physical products without the volatile swings of commercial aircraft or auto fleet orders. The bedrock of flatbed and heavy-haul freight demand. 
* **`durable_goods_orders`** (FRED: DGORDER)
    * **Definition:** Manufacturers' New Orders for Durable Goods (Total).
    * **S&OP Context:** The aggregate physical demand, inclusive of heavy transportation equipment.
* **`housing_starts`** (FRED: HOUST)
    * **Definition:** New Privately-Owned Housing Units Started.
    * **S&OP Context:** Housing is extremely freight-intensive (lumber, drywall, appliances). A leading indicator for flatbed and dry van demand.
* **`mfg_employment`** (FRED: MANEMP)
    * **Definition:** All Employees, Manufacturing. 
    * **S&OP Context:** Factories do not hire unless they have sustained order backlogs. A highly reliable, slow-moving indicator of sustained physical output.

## 4. Supply Chain Bullwhip (The "Warehouse Health")
These metrics help identify where freight is physically sitting in the supply chain, dictating the flow of future freight.

* **`retail_inventory_to_sales_ratio`** (FRED: RETAILIRSA)
    * **Definition:** How many months of inventory retailers are holding compared to their current monthly sales pace.
* **`wholesale_inventory_to_sales_ratio`** (FRED: WHLSLRIRSA)
    * **Definition:** The inventory ratio for merchant wholesalers. The "middle-man" of the supply chain.
* **`mfg_inventory_to_sales_ratio`** (FRED: MNFCTRIRSA)
    * **Definition:** The inventory ratio at the factory level.
    * **S&OP Context:** The ultimate leading indicator of supply chain chokes. If this spikes, factories are over-producing relative to demand, leading to sudden, violent production cuts downstream.
* **`total_inventory_to_sales_ratio`** (FRED: ISRATIO)
    * **Definition:** The aggregate inventory ratio across the entire supply chain (Manufacturing + Wholesale + Retail).
* **`production_motor_vehicle_parts`** (FRED: IPG3363S)
    * **Definition:** Industrial Production Index for Motor Vehicle Parts.
    * **S&OP Context:** Tracks the physical velocity of the Tier 1/Tier 2 supply base.
* **`feature_retail_inventory_spread`** (Engineered Feature)
    * **Definition:** `retail_inventory_to_sales_ratio` minus `total_inventory_to_sales_ratio`.
    * **S&OP Context:** Identifies severe Bullwhip Effects. When distribution centers become bloated, carriers use trailers as temporary storage yards, driving up artificial demand for new trailers.

## 5. Macro Sentiment (The "Broad Economy")
General economic and psychological health metrics. 

* **`vix_volatility`** (FRED: VIXCLS)
    * **Definition:** CBOE Volatility Index. Market fear/uncertainty.
* **`yield_curve_spread`** (FRED: T10Y2Y)
    * **Definition:** 10-Year Treasury Constant Maturity minus 2-Year Treasury. 
    * **S&OP Context:** The classic recession indicator. An inverted curve (negative spread) often precedes capital expenditure freezes by large fleets.
* **`weekly_economic_index`** (FRED: WEI)
    * **Definition:** An index of 10 daily/weekly indicators of real economic activity.
* **`consumer_sentiment`** (FRED: UMCSENT)
    * **Definition:** University of Michigan Consumer Sentiment Index. A highly predictive leading indicator for future retail freight movement.
* **`initial_jobless_claims`** (FRED: ICSA)
    * **Definition:** First-time filings for unemployment insurance.
* **`dow_jones_transportation_avg`** (FRED: DJTA)
    * **Definition:** Dow Jones Transportation Average. 
    * **S&OP Context:** Because stock prices reflect expected future earnings, major