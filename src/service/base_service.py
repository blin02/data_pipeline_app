from abc import ABCMeta, abstractmethod
import pandas as pd
from pandas import DataFrame
from constant.data import DataFormat, WriteMode
from typing import List


class BaseService:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def load_file_to_dataframe(self, path: str, file_format: DataFormat) -> DataFrame:
        df = None

        if file_format == DataFormat.JSON:
            df = pd.read_json(path)
        elif file_format == DataFormat.CSV:
            df = pd.read_csv(path, header=0)
        elif file_format == DataFormat.PARQUET:
            df = pd.read_parquet(path)
        else:
            print("Unsupported format")

        return df

    def save_as_parquet(self, df: DataFrame, path: str, write_mode: WriteMode = None, partition_cols: List[str] = None):

        df.to_parquet(path, partition_cols = partition_cols)
