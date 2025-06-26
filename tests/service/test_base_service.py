import shutil

import pytest
import pandas as pd
import pandas.testing as pd_test
import os
from pathlib import Path
from constant.data import DataFormat
from service.base_service import BaseService

@pytest.fixture (scope="module")
def sample_df():
    data = [
        {"donor_id": "d1", "campaign_id": "c1", "amount": 100.0, "timestamp": "2024-01-01T12:00:00"},
        {"donor_id": "d2", "campaign_id": "c1", "amount": 300.0, "timestamp": "2024-01-01T14:00:00"},
        {"donor_id": "d1", "campaign_id": "c2", "amount": 400.0, "timestamp": "2024-01-02T08:00:00"},
    ]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@pytest.fixture (scope="module")
def base_service():
    tests_dir_path = Path(__file__).parent.parent.absolute()
    temp_dir = tests_dir_path / "temp"

    if not temp_dir.is_dir():
        temp_dir.mkdir()

    yield BaseService()

    if temp_dir.is_dir():
        shutil.rmtree(temp_dir)

def test_load_file_to_dataframe(sample_df, base_service):
    dir_path = Path(__file__).parent.parent.absolute()
    df = base_service.load_file_to_dataframe(f"{dir_path}/resources/donations_1.json", DataFormat.JSON)

    assert df.shape == (6, 4)

def test_save_as_parquet(sample_df, base_service):
    dir_path = Path(__file__).parent.parent.absolute()
    file_name = "donations_raw.parquet"

    base_service.save_as_parquet(sample_df, f"{dir_path}/temp/{file_name}")
    df_parquet = base_service.load_file_to_dataframe(f"{dir_path}/temp/{file_name}", DataFormat.PARQUET)

    assert df_parquet.shape == (3, 4)
    pd_test.assert_frame_equal(sample_df, df_parquet)
