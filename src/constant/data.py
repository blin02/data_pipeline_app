from enum import Enum

class DataFormat(Enum):
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"
    ORC = "orc"
    TEXT = "text"
    JDBC = "jdbc"
    LIBSVM = "libsvm"

class WriteMode(Enum):
    ERROR_IF_EXISTS = "errorifexists"
    OVER_WRITE = "overwrite"
    APPEND = "append"
    IGNORE = "ignore"
