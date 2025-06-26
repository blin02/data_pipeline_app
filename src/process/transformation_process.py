import argparse

from constant.data import DataFormat, READ_FORMATS
from constant.pipeline import DONATION_RAW_FILE_NAME, DONATION_PER_CAMPAIGN_PER_DAY_FILE_NAME, \
    DONATION_PER_DAY_FILE_NAME
from service.donation_transformation_service import DonationTransformationService

def transform_process(source_data_path: str, file_type: str, output_dir_path: str):
    """
    Transform raw data and store them to a final storage. Also perform some simple aggregation for analytic purpose
    :param source_data_path: the full path of source data
    :param file_type: the format type of file, ex: json, parquet, etc
    :param output_dir_path: the path of output directory in a stage storage
    :return:
    """
    data_format = DataFormat(DataFormat[str(file_type).upper()])

    service = DonationTransformationService()

    # Load data into dataframe
    df = service.load_file_to_dataframe(source_data_path, data_format)

    # Transform data
    df_transformed = service.transform(df)
    #pprint.pp(df_transformed)
    service.save_as_parquet(df_transformed, f"{output_dir_path}/{DONATION_RAW_FILE_NAME}")

    # aggregate: donation_per_campain_per_day
    df_donation_per_campain_per_day = service.get_donation_per_campain_per_day(df_transformed)
    #pprint.pp(df_donation_per_campain_per_day)
    service.save_as_parquet(df_donation_per_campain_per_day, f"{output_dir_path}/{DONATION_PER_CAMPAIGN_PER_DAY_FILE_NAME}")

    # aggregate: donation_per_day
    df_donation_per_day = service.get_donation_per_day(df_transformed)
    #pprint.pp(df_donation_per_day)
    service.save_as_parquet(df_donation_per_day, f"{output_dir_path}/{DONATION_PER_DAY_FILE_NAME}")


if __name__ == "__main__":

    # Setup expected argument parameters
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument('--source_data_path', required=True, metavar='<source_data_path>')
    arg_parser.add_argument('--output_dir_path', required=True, metavar='<output_dir_path>')
    arg_parser.add_argument('--file_type', required=True, metavar= '<file_type>', choices=READ_FORMATS)
    arg_parser.add_argument('--env', default='local', metavar='<env>')

    # Parse expected argument parameters
    args, unknown = arg_parser.parse_known_args()

    transform_process(args.source_data_path, args.output_dir_path, args.file_type)