import pandas as pd
from pandas import DataFrame
import json
import pprint
from typing import List, Tuple
import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

from constant.data import DataFormat, WriteMode
from constant.schema import DONATION_DEFAULT_SCHEMA
from service.base_service import BaseService


class DonationIngestionService(BaseService):

    def __init__(self, schema: DataFrameSchema = None):
        super().__init__()

        # Define donation data schema
        if schema:
            self.schema = schema
        else:
            self.schema = DONATION_DEFAULT_SCHEMA


    def validate(self, df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """
        Validate a DataFrame object based on the Schema specified by the service class.
        Return a tuple object (validated DataFrame, errors DataFrame)
        :param df: a DataFrame object to be validated
        :return: tuple(validated DataFrame, errors DataFrame)
        """
        df_errors = None
        df_validated = None

        try:
            df_validated = self.schema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as err:
            df_errors = err.failure_cases

        return (df_validated, df_errors)


if __name__ == "__main__":

    service = DonationIngestionService()

    file_input_path = "../resources/donations_1.json"
    df = service.load_file_to_dataframe(file_input_path, DataFormat.JSON)

    df_validated, df_errors = service.validate(df)

    pprint.pp(df_validated)

    stage_output_path = "../temp/data/stage/donation_1_output.parquet"
    service.save_as_parquet(df_validated, stage_output_path)


