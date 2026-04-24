SERIES_MAP = {
    # ==========================================
    # 1. Capital Equipment Pricing
    # ==========================================
    'PCU336120336120':   {'name': 'ppi_heavy_truck_cab_mfg', 'category': 'Equipment Pricing', 'source': 'FRED'},
    'PCU336212336212':   {'name': 'ppi_truck_trailer_mfg', 'category': 'Equipment Pricing', 'source': 'FRED'},
    'PCU33633363':       {'name': 'ppi_motor_vehicle_parts', 'category': 'Equipment Pricing', 'source': 'FRED'},
    'WPU111':            {'name': 'ppi_general_machinery', 'category': 'Equipment Pricing', 'source': 'FRED'},
    'PCU333924333924':   {'name': 'ppi_material_handling_equip', 'category': 'Equipment Pricing', 'source': 'FRED'},

    # ==========================================
    # 2. Raw Materials & Operating Expenses
    # ==========================================
    'PALUMUSDM':         {'name': 'global_aluminum_price', 'category': 'Raw Materials', 'source': 'FRED'},
    'WPU102501':         {'name': 'ppi_aluminum_shapes', 'category': 'Raw Materials', 'source': 'FRED'},
    'WPU101':            {'name': 'ppi_iron_steel', 'category': 'Raw Materials', 'source': 'FRED'},
    'GASDESW':           {'name': 'diesel_price', 'category': 'Raw Materials', 'source': 'FRED'},

    # ==========================================
    # 3. Physical Output & Freight Volume
    # ==========================================
    'INDPRO':            {'name': 'industrial_production', 'category': 'Physical Output', 'source': 'FRED'},
    'TSIFRGHT':          {'name': 'freight_tsi', 'category': 'Physical Output', 'source': 'FRED'},
    'RAILFRTINTERMODAL': {'name': 'rail_intermodal', 'category': 'Physical Output', 'source': 'FRED'},
    'ADXTNO':            {'name': 'durable_goods_ex_transport', 'category': 'Physical Output', 'source': 'FRED'},
    'DGORDER':           {'name': 'durable_goods_orders', 'category': 'Physical Output', 'source': 'FRED'},
    'HOUST':             {'name': 'housing_starts', 'category': 'Physical Output', 'source': 'FRED'},
    'MANEMP':            {'name': 'mfg_employment', 'category': 'Physical Output', 'source': 'FRED'},

    # ==========================================
    # 4. Supply Chain Health & Inventory
    # ==========================================
    'RETAILIRSA':        {'name': 'retail_inventory_to_sales_ratio', 'category': 'Supply Chain Bullwhip', 'source': 'FRED'},
    'ISRATIO':           {'name': 'total_inventory_to_sales_ratio', 'category': 'Supply Chain Bullwhip', 'source': 'FRED'},
    'WHLSLRIRSA':        {'name': 'wholesale_inventory_to_sales_ratio', 'category': 'Supply Chain Bullwhip', 'source': 'FRED'},
    'MNFCTRIRSA':        {'name': 'mfg_inventory_to_sales_ratio', 'category': 'Supply Chain Bullwhip', 'source': 'FRED'},
    'IPG3363S':          {'name': 'production_motor_vehicle_parts', 'category': 'Supply Chain Bullwhip', 'source': 'FRED'},

    # ==========================================
    # 5. Macro Sentiment & Market Chaos
    # ==========================================
    'VIXCLS':            {'name': 'vix_volatility', 'category': 'Macro Sentiment', 'source': 'FRED'},
    'T10Y2Y':            {'name': 'yield_curve_spread', 'category': 'Macro Sentiment', 'source': 'FRED'},
    'WEI':               {'name': 'weekly_economic_index', 'category': 'Macro Sentiment', 'source': 'FRED'},
    'UMCSENT':           {'name': 'consumer_sentiment', 'category': 'Macro Sentiment', 'source': 'FRED'},
    'ICSA':              {'name': 'initial_jobless_claims', 'category': 'Macro Sentiment', 'source': 'FRED'},
    'DJTA':              {'name': 'dow_jones_transportation_avg', 'category': 'Macro Sentiment', 'source': 'FRED'},

    # ==========================================
    # 6. Carrier Pricing & Spot Rates
    # ==========================================
    'PCU4841214841212':  {'name': 'target_ppi_dry_van', 'category': 'Carrier Pricing', 'source': 'FRED'},
    'PCU484122484122':   {'name': 'target_ppi_ltl_reefer', 'category': 'Carrier Pricing', 'source': 'FRED'},
    'PCU484230484230':   {'name': 'target_ppi_flatbed', 'category': 'Carrier Pricing', 'source': 'FRED'},
    'FRGEXPUSM649NCIS':  {'name': 'cass_expenditures', 'category': 'Carrier Pricing', 'source': 'FRED'},
    'FRGSHPUSM649NCIS':  {'name': 'cass_shipments', 'category': 'Carrier Pricing', 'source': 'FRED'},

    # ==========================================
    # Targets
    # ==========================================
    'IPG336212S':        {'name': 'trailer_production_volume', 'category': 'Targets', 'source': 'FRED'},
    'HTRUCKSSAAR':       {'name': 'heavy_truck_sales', 'category': 'Targets', 'source': 'FRED'},
}
