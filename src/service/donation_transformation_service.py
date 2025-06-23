import pprint
import pandas as pd
from pandas import DataFrame

from constant.data import DataFormat
from service.base_service import BaseService


class DonationTransformationService(BaseService):

    def __init__(self):
        super().__init__()


    def transform(self, df: DataFrame) -> DataFrame:

        df["donation_date"] = df["timestamp"].dt.date

        #pprint.pp(df)

        return df

    def get_donation_per_campain_per_day(self, df: DataFrame) -> DataFrame:

        # 3. Group by the date column and sum the 'amount'
        # Method A.1: Group by the new 'transaction_day' column
        df_result = df.groupby(by=["campaign_id", "donation_date"])['amount'].sum().reset_index()

        return df_result

    def get_donation_per_day(self, df: DataFrame) -> DataFrame:

        # 3. Group by the date column and sum the 'amount'
        # Method A.1: Group by the new 'transaction_day' column
        df_result = df.groupby('donation_date')['amount'].sum().reset_index()

        return df_result

if __name__ == "__main__":
    service = DonationTransformationService()

    stage_output_path = "../temp/data/stage/donation_1_output.parquet"
    df = service.load_file_to_dataframe(stage_output_path, DataFormat.PARQUET)

    df_transformed = service.transform(df)
    pprint.pp(df_transformed)

    df_result = service.get_donation_per_campain_per_day(df_transformed)
    pprint.pp(df_result)

    df_result2 = service.get_donation_per_day(df_transformed)
    pprint.pp(df_result2)

    service.save_as_parquet(df_transformed, "../temp/data/final/donation_1_raw.parquet")
    service.save_as_parquet(df_result, "../temp/data/final/donation_1_donation_per_campain_per_day.parquet")
    service.save_as_parquet(df_result2, "../temp/data/final/donation_1_donation_per_day.parquet")
