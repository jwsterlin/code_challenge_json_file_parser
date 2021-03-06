import argparse
import concurrent.futures
import glob
import logging
import os
import shutil
import sys

from file_parser.file_parser import FileParser

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
        fail_and_exit(f"Did not find any input files at {args.input_dir}.  Exiting.")

    try:
        open(args.output_file, "w")
    except Exception as e:
        fail_and_exit(f"Could not create an output file at {args.output_file}.  Error: {e}")

    csv_files = [f"{args.work_dir}/{os.path.basename(x)}.tmp.csv" for x in json_files]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for json_file, csv_file in zip(json_files, executor.map(parse_file, zip(json_files, csv_files))):
            logging.debug(f"Temporary results for {json_file} stored at {csv_file}")

    fp = FileParser()
    fp.combine_csvs(csv_files, args.output_file)

    remove_work_directory(args.work_dir)
    logging.info(f"File parsing complete.  Result file can be found at {args.output_file}")
    sys.exit(0)

def fail_and_exit(exit_message):
    logging.fatal(exit_message)
    remove_work_directory(args.work_dir)
    sys.exit(1)

def create_work_directory(work_dir):
    try:
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
    except OSError as e:
        fail_and_exit(f"Creation of work directory {work_dir} failed: {e}")

def remove_work_directory(work_dir):
    logging.debug(f"Removing work directory {work_dir}")
    try:
        shutil.rmtree(work_dir, ignore_errors=True)
    except Exception as e:
        logging.fatal(f"Removal of work directory {work_dir} failed: {e}")
        sys.exit(1)

def parse_file(file_locations):
    input_file_location, output_file_location = file_locations
    fp = FileParser()
    fp.parse_file(input_file_location, output_file_location)
    return output_file_location

if __name__ == "__main__":
    main()