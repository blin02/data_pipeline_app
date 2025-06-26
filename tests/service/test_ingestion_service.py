import pytest
import pandera.pandas as pa
import pandas as pd
from pandera.pandas import Column, DataFrameSchema, Check

from constant.schema import DataFrameSchema
from service.donation_ingestion_service import DonationIngestionService

@pytest.fixture
def ingestion_service():

    # The 'yield' keyword is used to pass the object to the test.
    # Code before 'yield' is the setup part.
    print("\n[SETUP] Creating a new DonationIngestionService instance")

    yield DonationIngestionService()

    # Code after 'yield' is the teardown part. It runs after the test is done.
    print("\n[TEARDOWN] Test finished, cleaning up.")

@pytest.fixture
def ingestion_service_by_schema():

    # The 'yield' keyword is used to pass the object to the test.
    # Code before 'yield' is the setup part.
    print("\n[SETUP] Creating a new DonationIngestionService instance with specified schema")

    schema = DataFrameSchema({
        "donor_id": Column(str, required=True, nullable=False),
        "amount": Column(float, Check.in_range(0, 10000), coerce=True, required=True, nullable=False),
        "timestamp": Column(pa.DateTime, required=True, nullable=False)
    })

    yield DonationIngestionService(schema)

    # Code after 'yield' is the teardown part. It runs after the test is done.
    print("\n[TEARDOWN] Test finished, cleaning up.")

def test_valid_donation_data(ingestion_service):
    """
    Test case for valid donation data
    """

    # Sample valid data
    data = [
        {"donor_id": "d1", "campaign_id": "campaign_1", "amount": 100.0, "timestamp": "2024-01-01T12:00:00"},
        {"donor_id": "d2", "campaign_id": "campaign_1", "amount": 300.0, "timestamp": "2024-01-02T10:30:00"},
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    validated_df, errors_df = ingestion_service.validate(df)

    assert errors_df is None
    assert validated_df.shape == (2, 4)

def test_valid_donation_data_with_different_schema(ingestion_service_by_schema):
    """
    Test case for valid donation data
    """

    # Sample valid data
    data = [
        {"donor_id": "d1", "amount": 100.0, "timestamp": "2024-01-01T12:00:00"},
        {"donor_id": "d2", "amount": 300.0, "timestamp": "2024-01-02T10:30:00"},
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    validated_df, errors_df = ingestion_service_by_schema.validate(df)

    assert errors_df is None
    assert validated_df.shape == (2, 3)

def test_invalid_missing_column(ingestion_service):
    """
    Test case for missing 'campaign_id' field
    """

    data = [
        {"donor_id": "d1", "amount": 150.0, "timestamp": "2024-01-01T10:00:00"}
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    _, errors = ingestion_service.validate(df)

    assert errors is not None
    assert "campaign_id" in errors["failure_case"].values

def test_invalid_negative_amount(ingestion_service):
    """
    Test case for negative donation amount
    """

    data = [
        {"donor_id": "d1", "campaign_id": "c1", "amount": -50.0, "timestamp": "2024-01-01T10:00:00"}
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    _, errors = ingestion_service.validate(df)

    assert errors is not None
    assert any(errors["check"].str.contains("in_range"))

def test_invalid_null_donor_id(ingestion_service):
    """
    Test case for Null donor_id
    """
    # Null donor_id
    data = [
        {"donor_id": None, "campaign_id": "c1", "amount": 100.0, "timestamp": "2024-01-01T10:00:00"}
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    _, errors = ingestion_service.validate(df)

    assert errors is not None
    assert "donor_id" in errors["column"].values