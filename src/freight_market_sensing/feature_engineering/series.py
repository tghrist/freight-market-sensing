# src/freight_market_sensing/feature_engineering/series.py

SERIES_MAP = {
    # ==========================================
    # 1. Capital Equipment Pricing (Inflationary -> Velocity)
    # ==========================================
    'PCU336120336120': {
        'name': 'ppi_heavy_truck_cab_mfg',
        'category': 'Equipment Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'PCU336212336212': {
        'name': 'ppi_truck_trailer_mfg',
        'category': 'Equipment Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'PCU33633363': {
        'name': 'ppi_motor_vehicle_parts',
        'category': 'Equipment Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'WPU111': {
        'name': 'ppi_general_machinery',
        'category': 'Equipment Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'PCU333924333924': {
        'name': 'ppi_material_handling_equip',
        'category': 'Equipment Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },

    # ==========================================
    # 2. Raw Materials & Operating Expenses (Inflationary Costs -> Velocity)
    # ==========================================
    'PALUMUSDM': {
        'name': 'global_aluminum_price',
        'category': 'Raw Materials',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'WPU102501': {
        'name': 'ppi_aluminum_shapes',
        'category': 'Raw Materials',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'WPU101': {
        'name': 'ppi_iron_steel',
        'category': 'Raw Materials',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'GASDESW': {
        'name': 'diesel_price',
        'category': 'Raw Materials',
        'source': 'FRED',
        'transformation': 'velocity'
    },

    # ==========================================
    # 3. Physical Output & Freight Volume (Physical Reality -> Absolute)
    # ==========================================
    'INDPRO': {
        'name': 'industrial_production',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'TSIFRGHT': {
        'name': 'freight_tsi',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'RAILFRTINTERMODAL': {
        'name': 'rail_intermodal',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'ADXTNO': {
        'name': 'durable_goods_ex_transport',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'DGORDER': {
        'name': 'durable_goods_orders',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'HOUST': {
        'name': 'housing_starts',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'MANEMP': {
        'name': 'mfg_employment',
        'category': 'Physical Output',
        'source': 'FRED',
        'transformation': 'absolute'
    },

    # ==========================================
    # 4. Supply Chain Health & Inventory (Mean-Reverting Ratios -> Absolute)
    # ==========================================
    'RETAILIRSA': {
        'name': 'retail_inventory_to_sales_ratio',
        'category': 'Supply Chain Bullwhip',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'ISRATIO': {
        'name': 'total_inventory_to_sales_ratio',
        'category': 'Supply Chain Bullwhip',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'WHLSLRIRSA': {
        'name': 'wholesale_inventory_to_sales_ratio',
        'category': 'Supply Chain Bullwhip',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'MNFCTRIRSA': {
        'name': 'mfg_inventory_to_sales_ratio',
        'category': 'Supply Chain Bullwhip',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'IPG3363S': {
        'name': 'production_motor_vehicle_parts',
        'category': 'Supply Chain Bullwhip',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'ENG_SPREAD': {
        'name': 'feature_retail_inventory_spread',
        'category': 'Supply Chain Bullwhip',
        'source': 'Engineered',
        'transformation': 'absolute'
    },

    # ==========================================
    # 5. Macro Sentiment & Market Chaos (Bounded/Indices vs Unbounded)
    # ==========================================
    'VIXCLS': {
        'name': 'vix_volatility',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'T10Y2Y': {
        'name': 'yield_curve_spread',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'WEI': {
        'name': 'weekly_economic_index',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'UMCSENT': {
        'name': 'consumer_sentiment',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'ICSA': {
        'name': 'initial_jobless_claims',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'DJTA': {
        'name': 'dow_jones_transportation_avg',
        'category': 'Macro Sentiment',
        'source': 'FRED',
        'transformation': 'velocity'
    },

    # ==========================================
    # 6. Carrier Pricing & Spot Rates (Rates/Prices -> Velocity, except Physical Shipments)
    # ==========================================
    'PCU4841214841212': {
        'name': 'target_ppi_dry_van',
        'category': 'Carrier Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'PCU484122484122': {
        'name': 'target_ppi_ltl_reefer',
        'category': 'Carrier Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'PCU484230484230': {
        'name': 'target_ppi_flatbed',
        'category': 'Carrier Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'FRGEXPUSM649NCIS': {
        'name': 'cass_expenditures',
        'category': 'Carrier Pricing',
        'source': 'FRED',
        'transformation': 'velocity'
    },
    'FRGSHPUSM649NCIS': {
        'name': 'cass_shipments',
        'category': 'Carrier Pricing',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'ENG_CASS_RATE': {
        'name': 'target_cass_inferred_rate',
        'category': 'Carrier Pricing',
        'source': 'Engineered',
        'transformation': 'velocity'
    },

    # ==========================================
    # 7. Targets (Must remain absolute for baseline predictions)
    # ==========================================
    'IPG336212S': {
        'name': 'trailer_production_volume',
        'category': 'Targets',
        'source': 'FRED',
        'transformation': 'absolute'
    },
    'HTRUCKSSAAR': {
        'name': 'heavy_truck_sales',
        'category': 'Targets',
        'source': 'FRED',
        'transformation': 'absolute'
    }
}