import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

DONATION_DEFAULT_SCHEMA = DataFrameSchema({
    "donor_id": Column(str, required=True, nullable=False),
    "campaign_id": Column(str, required=True, nullable=False),
    "amount": Column(float, Check.in_range(0, 10000), coerce=True, required=True, nullable=False),
    "timestamp": Column(pa.DateTime, required=True, nullable=False)
})
