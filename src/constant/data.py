from enum import Enum

class DataFormat(Enum):
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"
    ORC = "orc"
    TEXT = "text"
    JDBC = "jdbc"
    LIBSVM = "libsvm"

READ_FORMATS = [
    DataFormat.JSON.value,
    DataFormat.CSV.value,
    DataFormat.PARQUET.value,
    DataFormat.ORC.value,
    DataFormat.TEXT.value,
    DataFormat.JDBC.value,
    DataFormat.LIBSVM.value
]

class WriteMode(Enum):
    ERROR_IF_EXISTS = "errorifexists"
    OVER_WRITE = "overwrite"
    APPEND = "append"
    IGNORE = "ignore"
