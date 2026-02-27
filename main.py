import pandas as pd
from src.data_collection.cdc_fluview import CDCFluViewClient
from src.feature_engineering.seasonal_severity import SeasonalSeverityModel

def main():
    print("=== Health Prediction Market System - Flu Season Severity ===")

    # Initialize Client
    client = CDCFluViewClient()

    # 1. Fetch historical data to build the model (e.g., last 5 years)
    print("Fetching historical data for baseline (last 5 years)...")
    # Using a known range that definitely has data
    history_start = 201801
    history_end = 202252

    try:
        history_df = client.fetch_ili_data("nat", f"{history_start}-{history_end}")

        if history_df.empty:
            print("Error: Could not fetch historical data.")
            return

        print(f"Loaded {len(history_df)} historical records.")

        # 2. Build Model
        model = SeasonalSeverityModel(history_df)
        print("Severity Model Initialized. Baselines calculated.")

        # 3. Fetch "Current" Season Data (simulated "current" as the 2023-2024 season)
        current_season_start = 202340
        current_season_end = 202410
        print(f"Fetching 'current' season data ({current_season_start}-{current_season_end})...")

        recent_df = client.fetch_ili_data("nat", f"{current_season_start}-{current_season_end}")

        if recent_df.empty:
             print("No data available for the specified range.")
             return

        print(f"\nAnalyzing recent trends ({len(recent_df)} weeks):")
        print(f"{'Epiweek':<10} | {'WILI':<6} | {'Severity':<10} | {'Z-Score':<8} | {'Percentile':<10}")
        print("-" * 60)

        for _, row in recent_df.iterrows():
            epiweek = int(row['epiweek'])
            # WILI can sometimes be null? check
            if pd.isna(row['wili']):
                continue

            wili = float(row['wili'])

            score = model.score_epiweek(epiweek, wili)

            if score:
                print(f"{score['epiweek']:<10} | {score['wili']:<6.2f} | {score['severity_level']:<10} | {score['z_score']:<8.2f} | {score['percentile_rank']:<10.1f}")
            else:
                print(f"{epiweek:<10} | {wili:<6.2f} | {'N/A':<10} | {'-':<8} | {'-':<10}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
