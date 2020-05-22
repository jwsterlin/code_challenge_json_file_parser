import argparse
import concurrent.futures
import glob
import logging
import os
import sys

from file_parser.file_parser import FileParser

# TODO: Documentation
# TODO: Build scripts
# TODO: Try invalid values for all flag inputs
# TODO: Check all exit codes
# TODO: Add comments
# TODO: List assumptions in readme
    # Assume space before Doe not intended, or " Doe" was specified in file
    # Invalid data in any column invalidates the entire row
    # Assume no header, per example
    # Assume trailing newline is unacceptable (more processing required)
    # Assume total input size ~ several GB to tens of GB.  Recommend trying golang as we move toward terabyte scale.
    # No advanced validation on names and dates
    # Incoming double quotes will be escaped as \" in the JSON input file

DEFAULT_WORK_DIR = "work_dir"
DEFAULT_LOG_LOCATION = "parse_files.log"
DEFAULT_LOG_LEVEL = "INFO"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", required=True, help="Location of a directory that contains JSON files to be parsed.")
parser.add_argument("-o", "--output_file", required=True, help="Output file location where CSV results will be stored.")
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

try:
    logging.basicConfig(filename=args.log_location, level=numeric_level, format=log_format)
except Exception as e:
    print(f"Could not create a log file at {args.log_location}.  Exiting.")
    sys.exit(1)

def main():
    logging.info("Running file parser")
    create_work_directory(args.work_dir)
    json_files = glob.glob(args.input_dir + "/*")
    if len(json_files) == 0:
        logging.fatal(f"Did not find any input files at {args.input_dir}.  Exiting.")
        sys.exit(1)

    try:
        open(args.output_file, "w")
    except Exception as e:
        logging.fatal(f"Could not create an output file at {args.output_file}.  Error: {e}")
        sys.exit(1)

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