import argparse
import pprint

from constant.data import DataFormat, READ_FORMATS
from constant.pipeline import DONATION_RAW_FILE_NAME
from service.donation_ingestion_service import DonationIngestionService

def ingestion_process(source_data_path: str, file_type: str, output_dir_path: str):
    """
    Load and validate raw data and ingest them to a stage storage
    :param source_data_path: the full path of source data
    :param file_type: the format type of file, ex: json, parquet, etc
    :param output_dir_path: the path of output directory in a stage storage
    :return:
    """
    data_format = DataFormat(DataFormat[args.file_type.upper()])

    service = DonationIngestionService()

    # Create a dataframe for the data from the specified path
    df = service.load_file_to_dataframe(source_data_path, data_format)

    # Data validation: ex schema validation, data type validation, data requirement rules
    df_validated, df_errors = service.validate(df)
    #pprint.pp(df_validated)

    # save output to staging location
    stage_output_path = f"{output_dir_path}/{DONATION_RAW_FILE_NAME}"
    service.save_as_parquet(df_validated, stage_output_path)


if __name__ == "__main__":

    # Setup expected argument parameters
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument('--source_data_path', required=True, metavar='<source_data_path>')
    arg_parser.add_argument('--output_dir_path', required=True, metavar='<output_dir_path>')
    arg_parser.add_argument('--file_type', required=True, metavar= '<file_type>', choices=READ_FORMATS)
    arg_parser.add_argument('--env', default='local', metavar='<env>')

    # Parse expected argument parameters
    args, unknown = arg_parser.parse_known_args()

    ingestion_process(args.source_data_path, args.file_type, args.output_dir_path)