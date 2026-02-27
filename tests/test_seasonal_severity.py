import pytest
import pandas as pd
import numpy as np
from src.feature_engineering.seasonal_severity import SeasonalSeverityModel

@pytest.fixture
def historical_data():
    # Create simple historical data
    # 2 years of data, just weeks 1, 2, 3 for simplicity
    data = {
        'epiweek': [202201, 202202, 202203, 202301, 202302, 202303],
        'wili': [2.0, 2.5, 2.2, 2.2, 2.7, 2.4]
    }
    return pd.DataFrame(data)

def test_baselines_calculation(historical_data):
    model = SeasonalSeverityModel(historical_data)
    baselines = model.baselines

    # Check shape (3 weeks)
    assert len(baselines) == 3
    assert baselines.index.tolist() == [1, 2, 3]

    # Check mean calculation for Week 1 (2.0 and 2.2) -> 2.1
    assert baselines.loc[1, 'mean'] == pytest.approx(2.1)

    # Check mean calculation for Week 2 (2.5 and 2.7) -> 2.6
    assert baselines.loc[2, 'mean'] == pytest.approx(2.6)

def test_score_epiweek_high_severity(historical_data):
    model = SeasonalSeverityModel(historical_data)

    # Score a week 2 with high wili (above historical max 2.7)
    score = model.score_epiweek(202402, 3.0)

    assert score['epiweek'] == 202402
    assert score['wili'] == 3.0
    assert score['z_score'] > 0
    assert score['severity_level'] == 'High'

def test_score_epiweek_low_severity(historical_data):
    model = SeasonalSeverityModel(historical_data)

    # Score a week 1 with low wili (below historical min 2.0)
    score = model.score_epiweek(202401, 1.5)

    assert score['epiweek'] == 202401
    assert score['wili'] == 1.5
    assert score['z_score'] < 0
    assert score['severity_level'] == 'Low'

def test_missing_columns():
    with pytest.raises(ValueError):
        SeasonalSeverityModel(pd.DataFrame({'a': [1], 'b': [2]}))
