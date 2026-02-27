import pandas as pd
import numpy as np

class SeasonalSeverityModel:
    """
    Model for analyzing and scoring seasonal severity based on historical ILI data.
    """

    def __init__(self, historical_data):
        """
        Args:
            historical_data (pd.DataFrame): DataFrame containing historical ILI data.
                                            Must contain 'epiweek' (int) and 'wili' (float) columns.
        """
        self.history = historical_data.copy()

        # Ensure 'epiweek' is handled as numeric or can be processed for seasonality
        if 'epiweek' in self.history.columns:
            self.history['epiweek'] = self.history['epiweek'].astype(int)
            self.history['week_num'] = self.history['epiweek'] % 100
        else:
             raise ValueError("Data must contain 'epiweek' column.")

        if 'wili' not in self.history.columns:
             raise ValueError("Data must contain 'wili' column.")

        self.baselines = self._calculate_baselines()

    def _calculate_baselines(self):
        """
        Calculates baseline statistics (mean, std, percentiles) for each week of the year
        across all available historical seasons.
        """
        # Group by week number (ignoring year) to get seasonal pattern
        grouped = self.history.groupby('week_num')['wili']

        baselines = pd.DataFrame({
            'mean': grouped.mean(),
            'std': grouped.std(),
            'p25': grouped.quantile(0.25),
            'p50': grouped.median(),
            'p75': grouped.quantile(0.75),
            'p90': grouped.quantile(0.90),
            'p95': grouped.quantile(0.95),
            'max': grouped.max()
        })

        return baselines

    def score_epiweek(self, epiweek, wili):
        """
        Scores the severity of a given epiweek.

        Args:
            epiweek (int): The epiweek (YYYYWW).
            wili (float): The Weighted ILI percentage for that week.

        Returns:
            dict: Severity score metrics.
        """
        week_num = int(str(epiweek)[-2:])

        if week_num not in self.baselines.index:
             # Handle edge case or missing baseline (e.g., week 53)
             # Fallback to nearest neighbor or return None
             return None

        baseline = self.baselines.loc[week_num]

        z_score = (wili - baseline['mean']) / baseline['std'] if baseline['std'] > 0 else 0
        percentile_rank = (wili > self.history[self.history['week_num'] == week_num]['wili']).mean() * 100

        severity_level = "Low"
        if wili > baseline['p95']:
            severity_level = "High"
        elif wili > baseline['p75']:
            severity_level = "Moderate"

        return {
            'epiweek': epiweek,
            'wili': wili,
            'z_score': z_score,
            'percentile_rank': percentile_rank,
            'baseline_mean': baseline['mean'],
            'baseline_p95': baseline['p95'],
            'severity_level': severity_level
        }

    def score_season(self, season_data):
         """
         Scores an entire season based on cumulative severity or peak intensity.

         Args:
             season_data (pd.DataFrame): DataFrame for the season to score.

         Returns:
             dict: Season summary metrics.
         """
         peak_wili = season_data['wili'].max()
         avg_wili = season_data['wili'].mean()

         # Compare peak to historical peaks (simplified)
         # In a real system, we'd calculate historical season peaks first

         return {
             'peak_wili': peak_wili,
             'avg_wili': avg_wili
         }
