import argparse
import concurrent.futures
import glob
import logging
import os
import sys

from file_parser.file_parser import FileParser

# TODO: Documentation
# TODO: Unit tests
# TODO: Build scripts
# TODO: Try invalid values for all inputs
# TODO: Try invalid lines/values in input files
# TODO: Try special characters in input files
# TODO: Check all exit codes
# TODO: Add comments
# TODO: Try commas in input file contents
# TODO: List assumptions in readme
    # Assume space before Doe not intended, or " Doe" was specified in file
    # Invalid data in any column invalidates the entire row
    # Assume no header, per example
    # Assume trailing newline is unacceptable

DEFAULT_WORK_DIR = "work_dir"
DEFAULT_LOG_LOCATION = "parse_files.log"
DEFAULT_NUM_THREADS = 4
DEFAULT_LOG_LEVEL = "INFO"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", required=True, help="Location of a directory that contains JSON files to be parsed.")
parser.add_argument("-o", "--output_file", required=True, help="Output file location where CSV results will be stored.")
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

def main():
    logging.info("Running file parser")
    create_work_directory(args.work_dir)
    json_files = glob.glob(args.input_dir + "/*")
    csv_files = [f"{args.work_dir}/{os.path.basename(x)}.tmp.csv" for x in json_files]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for json_file, csv_file in zip(json_files, executor.map(parse_file, zip(json_files, csv_files))):
            logging.debug(f"Temporary results for {json_file} stored at {csv_file}")

    fp = FileParser()
    fp.combine_csvs(csv_files, args.output_file)

def create_work_directory(work_dir):
    try:
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
    except OSError as e:
        print(f"Creation of work directory {work_dir} failed: {e}")
        sys.exit(1)

def parse_file(file_locations):
    input_file_location, output_file_location = file_locations
    fp = FileParser()
    fp.parse_file(input_file_location, output_file_location)
    return output_file_location

if __name__ == "__main__":
    main()