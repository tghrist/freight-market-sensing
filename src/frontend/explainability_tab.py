import streamlit as st


def render_feature_explainability():
    st.subheader("The Supply Chain Physics: Why These Features?")
    st.markdown("""
    Rather than relying on internal sales sentiment, this XGBoost model was trained on dozens of macroeconomic indicators. 
    Through iterative feature tournaments, the model identified these five indicators as the most mathematically significant 
    drivers of OEM trailer production. 

    Here is the business logic behind the math:
    """)

    st.divider()

    st.markdown("""
    **1. Cass Freight Shipments Index** * **The Logic:** Physical freight volume is the ultimate constraint. If freight shipments are dropping, fleets have excess capacity. They will not order new trailers to haul freight that doesn't exist.

    **2. PPI: Heavy Motor Truck Manufacturing** * **The Logic:** This acts as the capital cost constraint. When the Producer Price Index for truck cabs spikes, fleets allocate their capital budgets to highly expensive power units (tractors), delaying their trailer replacement cycles.

    **3. Industrial Production Index** * **The Logic:** A massive percentage of flatbed and dry van freight is tied to heavy manufacturing. This serves as the leading indicator for the industrial sector's demand for physical transportation.

    **4. Consumer Sentiment Index (UMCSENT)** * **The Logic:** Consumer sentiment is the earliest upstream indicator of retail freight volume. Drops in consumer confidence reliably precede drops in retail inventory restocking, which eventually hits trailer utilization.

    **5. Manufacturing Inventory-to-Sales Ratio** * **The Logic:** This captures the **Bullwhip Effect**. When this ratio spikes, it means factories have overproduced and sales have slowed. They stop shipping goods to warehouses, heavily dampening demand for new commercial fleet equipment.
    """)