# src/config.py

# The target variable the model is predicting
ACTIVE_TARGET = 'trailer_production_volume'

# The champion features used for training and UI rendering
CHAMPION_FEATURES = {
    "industrial_production": {
        "title": "Industrial Production Index",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This is the baseline anchor for physical reality. It tracks the raw output of all US factories and mines. Because industrial goods drive flatbed and dry van freight, higher factory output directly dictates the baseline need for commercial trailers."
    },
    "cass_shipments": {
        "title": "Cass Freight Shipments",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** Physical freight volume is the ultimate physical constraint. If total freight shipments are dropping, fleets have excess capacity in their existing networks and will freeze new trailer orders."
    },
    "consumer_sentiment": {
        "title": "Consumer Sentiment",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** The entire freight economy sits downstream of the American consumer. Drops in consumer confidence reliably precede drops in retail inventory restocking, which eventually hits trailer utilization."
    },
    "mfg_inventory_to_sales_ratio": {
        "title": "Mfg Inventory-to-Sales",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This captures the **Bullwhip Effect**. When this ratio spikes, factories have overproduced and warehouses are full. They stop shipping goods to distribution centers, instantly killing the need for freight capacity."
    },
    "ppi_motor_vehicle_parts": {
        "title": "PPI: Motor Vehicle Parts (Velocity)",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This acts as the ultimate Cost of Goods Sold (COGS) constraint. When the cost of core vehicle components (brakes, axles, suspensions) spikes rapidly, OEMs face margin compression and fleets face sticker shock, delaying trailer replacement cycles."
    },
    "durable_goods_ex_transport": {
        "title": "Durable Goods (Ex-Transport)",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This captures the **Crowding Out Effect**. When the rest of the US industrial base (appliances, machinery) is running at absolute peak capacity, trailer OEMs have to fight for raw materials and factory labor, constraining production capabilities."
    }
}