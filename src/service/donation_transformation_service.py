import pprint
import pandas as pd
from pandas import DataFrame

from constant.data import DataFormat
from service.base_service import BaseService


class DonationTransformationService(BaseService):
    """
    Transform raw data and store them to a final storage. Also perform some simple aggregation for analytic purpose
    """

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

