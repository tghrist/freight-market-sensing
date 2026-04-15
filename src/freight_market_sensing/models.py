import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from features import FeatureStore


class EquipmentDemandForecaster:
    def __init__(self):
        print("Initializing Tier 1 Equipment Forecaster...")
        store = FeatureStore()
        self.df = store.build_master_matrix()

        # The new Tier 1 Target Variable: Factory floor output of commercial trailers
        self.target_col = 'trailer_production_volume'

        # The Top 5 features identified by our XGBoost ranking
        self.top_features = [
            'heavy_truck_sales',
            'ppi_heavy_truck_cab_mfg',
            'target_ppi_dry_van',
            'global_aluminum_price',
            'mfg_employment'
        ]

    def build_model(self, forecast_horizon_weeks=12):
        """Trains the XGBoost model to predict [X] weeks into the future."""
        print("-" * 50)
        print(f"Building {forecast_horizon_weeks}-Week Advance Forecasting Model...")

        # 1. THE TIME MACHINE: Shift the target backwards
        # A negative shift moves future production data up to align with current economic data
        ml_df = self.df.copy()
        ml_df['future_target'] = ml_df[self.target_col].shift(-forecast_horizon_weeks)

        # Because we shifted the data, the most recent 12 weeks won't have a "future" target yet.
        # We must drop these empty rows specifically for the TRAINING phase.
        train_df = ml_df.dropna(subset=['future_target'])

        X = train_df[self.top_features]
        y = train_df['future_target']

        # Time-Series Split: Hold out the last year of available shifted data for testing
        split_index = len(train_df) - 52

        X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
        y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

        # Train the Model
        self.model = xgb.XGBRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )
        self.model.fit(X_train, y_train)

        # Evaluate performance
        predictions = self.model.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, predictions)
        print(f"Validation MAPE (Predicting {forecast_horizon_weeks} weeks out): {mape:.2%}")

        return X_train, y_train, X_test, y_test, predictions

    def generate_forecast(self, forecast_horizon_weeks=12):
        """Predicts future trailer production based on today's leading indicators."""
        # Grab the absolute latest economic data we have (the stuff we dropped during training)
        latest_data = self.df[self.top_features].iloc[-1:]
        latest_date = latest_data.index[0].strftime('%Y-%m-%d')

        prediction = self.model.predict(latest_data)[0]

        print("-" * 50)
        print(f"LIVE TIER 1 FORECAST:")
        print(f"Based on economic data from: {latest_date}")
        print(f"Predicted Trailer Production Index in {forecast_horizon_weeks} weeks: {prediction:.2f}")
        print("-" * 50)


if __name__ == "__main__":
    forecaster = EquipmentDemandForecaster()
    X_train, y_train, X_test, y_test, test_preds = forecaster.build_model()
    forecaster.generate_forecast()