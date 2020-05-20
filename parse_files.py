import argparse
import concurrent.futures
import glob
import logging

# TODO: Specify log levels
# TODO: Documentation
# TODO: Unit tests
# TODO: Build scripts
# TODO: Try invalid values for all inputs

DEFAULT_WORK_DIR = "work_dir"
DEFAULT_LOG_LOCATION = "parse_files.log"
DEFAULT_NUM_THREADS = 4
DEFAULT_LOG_LEVEL = "INFO"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required=True, help="Location of a directory that contains JSON files to be parsed.")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory location where CSV results will be stored.")
    parser.add_argument(
        "-t",
        "--num_threads",
        required=False,
        default=DEFAULT_NUM_THREADS,
        type=int,
        help=f"Number of concurrent threads to use.  Defaults to {DEFAULT_NUM_THREADS}."
    )
    parser.add_argument(
        "--log_location",
        required=False,
        default=DEFAULT_LOG_LOCATION,
        help=f"Location to use for log output.  Defaults to <current_directory>/{DEFAULT_LOG_LOCATION}."
    )
    parser.add_argument(
        "--log_level",
        required=False,
        default=DEFAULT_LOG_LEVEL,
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "critical", "error", "warning", "info", "debug"],
        help=f"Log level.  Defaults to {DEFAULT_LOG_LEVEL}."
    )
    parser.add_argument(
        "-w",
        "--work_dir",
        required=False,
        default=DEFAULT_WORK_DIR,
        help=f"Directory where temporary CSV results will be stored.  Defaults to <current_directory>/{DEFAULT_WORK_DIR}."
    )
    args = parser.parse_args()

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    numeric_level = getattr(logging, args.log_level.upper(), None)
    logging.basicConfig(filename=args.log_location, level=numeric_level, format=log_format)
    logging.info("Running file parser")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        json_files = glob.glob(args.input_dir + "/*")
        for json_file, work_csv_file in zip(json_files, executor.map(parse_file, json_files)):
            logging.debug(f"Temporary results for {json_file} stored at {work_csv_file}")

def parse_file(file_location):
    logging.debug(f"Parsing file: {file_location}")
    return "somefile"

if __name__ == "__main__":
    main()