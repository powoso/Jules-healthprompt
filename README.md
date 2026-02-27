# Health Prediction Market System - Flu Season Severity

This project implements a system for analyzing and predicting flu season severity using CDC FluView data. It serves as a backend component for health prediction markets, answering questions like "Will flu season exceed X hospitalizations?".

## Components

1.  **Data Collection**: Fetches ILI (Influenza-like Illness) data from the Delphi Epidata API (a proxy for CDC FluView).
2.  **Feature Engineering**: Calculates historical baselines and scores current weekly severity using Z-scores and percentile ranks.
3.  **Analysis**: Provides severity assessments (Low, Moderate, High) based on historical context.

## Installation on macOS

### Prerequisites

-   **Python 3.8+**: macOS usually comes with Python, but it's recommended to install a newer version via [Homebrew](https://brew.sh/):
    ```bash
    brew install python
    ```
-   **Git**: To clone the repository.
    ```bash
    xcode-select --install  # Installs Git if not present
    ```

### Step-by-Step Setup

1.  **Clone the Repository**
    Open Terminal and run:
    ```bash
    git clone https://github.com/yourusername/health-prediction-market.git
    cd health-prediction-market
    ```

2.  **Create a Virtual Environment**
    It's best practice to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Demonstration
To run the main analysis script, which fetches historical data and scores the 2023-2024 flu season:

```bash
python main.py
```

**Expected Output:**
```
=== Health Prediction Market System - Flu Season Severity ===
Fetching historical data for baseline (last 5 years)...
Loaded 261 historical records.
Severity Model Initialized. Baselines calculated.
Fetching 'current' season data (202340-202410)...

Analyzing recent trends (23 weeks):
Epiweek    | WILI   | Severity   | Z-Score  | Percentile
------------------------------------------------------------
202340     | 2.28   | Moderate   | 0.92     | 80.0
...
```

### Running Tests
To verify the system components:

```bash
pytest
```

## Project Structure

```
.
├── src/
│   ├── data_collection/
│   │   └── cdc_fluview.py       # API Client
│   └── feature_engineering/
│       └── seasonal_severity.py # Severity Model
├── tests/                       # Unit tests
├── main.py                      # Demo script
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```
