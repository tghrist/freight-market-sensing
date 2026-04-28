# src/config.py

# The target variable the model is predicting
ACTIVE_TARGET = 'trailer_production_volume'

# The champion features used for training and UI rendering
CHAMPION_FEATURES = {
    "cass_shipments": {
        "title": "Cass Freight Shipments",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** Physical freight volume is the ultimate constraint. If freight shipments are dropping, fleets have excess capacity. They will not order new trailers to haul freight that doesn't exist."
    },
    "ppi_heavy_truck_cab_mfg": {
        "title": "PPI: Heavy Truck Cabs",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This acts as the ultimate CapEx constraint. As the absolute cost of truck cabs reaches historic highs, fleets exhaust their capital budgets simply maintaining their power units (tractors). This sticker shock forces them to delay their trailer replacement cycles, driving trailer demand down during peak inflationary periods."
    },
    "industrial_production": {
        "title": "Industrial Production Index",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** A massive percentage of flatbed and dry van freight is tied to heavy manufacturing. This serves as the leading indicator for the industrial sector's demand for physical transportation."
    },
    "consumer_sentiment": {
        "title": "Consumer Sentiment",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** Consumer sentiment is the earliest upstream indicator of retail freight volume. Drops in consumer confidence reliably precede drops in retail inventory restocking, which eventually hits trailer utilization."
    },
    "mfg_inventory_to_sales_ratio": {
        "title": "Mfg Inventory-to-Sales",
        "ui_color": "#1f77b4",
        "logic": "**The Logic:** This captures the **Bullwhip Effect**. When this ratio spikes, it means factories have overproduced and sales have slowed. They stop shipping goods to warehouses, heavily dampening demand for new commercial fleet equipment."
    }
}