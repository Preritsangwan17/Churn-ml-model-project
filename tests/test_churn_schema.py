import pandas as pd
import pytest
from churn.pipeline import prepare


def test_blank_totalcharges_and_id_exclusion():
    X, _ = prepare(
        pd.DataFrame(
            {
                "customerID": ["one"],
                "Unnamed: 0": [0],
                "TotalCharges": [" "],
                "Contract": ["Monthly"],
            }
        )
    )
    assert "customerID" not in X and "Unnamed: 0" not in X
    assert X["TotalCharges"].isna().all()


def test_invalid_totalcharges():
    with pytest.raises(ValueError, match="TotalCharges"):
        prepare(pd.DataFrame({"TotalCharges": ["bad"]}))
