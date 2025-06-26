import pytest
import pandas as pd
from service.donation_transformation_service import DonationTransformationService

@pytest.fixture
def sample_df():
    data = [
        {"donor_id": "d1", "campaign_id": "c1", "amount": 100.0, "timestamp": "2024-01-01T12:00:00"},
        {"donor_id": "d2", "campaign_id": "c1", "amount": 300.0, "timestamp": "2024-01-01T14:00:00"},
        {"donor_id": "d1", "campaign_id": "c2", "amount": 400.0, "timestamp": "2024-01-02T08:00:00"},
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def test_transform_adds_donation_date(sample_df):
    service = DonationTransformationService()
    df_transformed = service.transform(sample_df)
    assert "donation_date" in df_transformed.columns
    assert df_transformed["donation_date"].dtype == "object"  # datetime.date

def test_aggregation_per_campaign_day(sample_df):
    service = DonationTransformationService()
    df_transformed = service.transform(sample_df)
    df_result = service.get_donation_per_campain_per_day(df_transformed)

    assert "campaign_id" in df_result.columns
    assert "donation_date" in df_result.columns
    assert "amount" in df_result.columns
    assert len(df_result) >= 1
