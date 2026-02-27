import requests
import pandas as pd

class CDCFluViewClient:
    """
    Client for fetching CDC FluView data from the Delphi Epidata API.
    API Documentation: https://cmu-delphi.github.io/delphi-epidata/api/fluview.html
    """
    BASE_URL = "https://api.delphi.cmu.edu/epidata/fluview/"

    def __init__(self):
        pass

    def fetch_ili_data(self, regions, epiweeks_range, auth=None):
        """
        Fetches Influenza-like Illness (ILI) data.

        Args:
            regions (str or list): Region(s) to fetch data for.
                                   Examples: 'nat' (National), 'hhs1' (HHS Region 1), 'cen1' (Census Division 1), 'al' (Alabama).
                                   Can be a single string or a list of strings.
            epiweeks_range (str or list): Epiweeks to fetch.
                                          Examples: '202340', '202340-202410'.
                                          Can be a single string (range or single week) or a list/tuple of weeks.
            auth (str, optional): Authentication token if required (mostly for private data).

        Returns:
            pd.DataFrame: DataFrame containing the ILI data.
        """
        if isinstance(regions, list):
            regions = ",".join(regions)

        if isinstance(epiweeks_range, list):
            epiweeks = ",".join([str(w) for w in epiweeks_range])
        else:
            epiweeks = str(epiweeks_range)

        params = {
            "regions": regions,
            "epiweeks": epiweeks,
        }
        if auth:
            params["auth"] = auth

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("result") != 1:
                # API returns result: 1 for success, -2 for no results, etc.
                # If no results, return empty DataFrame or handle accordingly
                if data.get("result") == -2:
                     return pd.DataFrame()
                raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

            df = pd.DataFrame(data.get("epidata", []))
            return df

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def get_national_ili(self, start_week, end_week):
        """
        Helper to fetch national ILI data for a specific range.

        Args:
            start_week (int or str): Start epiweek (e.g., 202340)
            end_week (int or str): End epiweek (e.g., 202410)

        Returns:
            pd.DataFrame: National ILI data.
        """
        return self.fetch_ili_data(regions='nat', epiweeks_range=f"{start_week}-{end_week}")
