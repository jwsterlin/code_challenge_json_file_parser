import argparse
import concurrent.futures
import glob
import logging

# TODO: Specify log levels
# TODO: Documentation
# TODO: Unit tests
# TODO: Build scripts

DEFAULT_WORK_DIR = "work_dir"
DEFAULT_LOG_LOCATION = "parse_files.log"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required=True, help="Location of a directory that contains JSON files to be parsed.")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory location where CSV results will be stored.")
    parser.add_argument("-t", "--num_threads", required=False, default=4, type=int, help="Number of concurrent threads to use.")
    parser.add_argument("-l", "--log_location", required=False, default=DEFAULT_LOG_LOCATION, help="Location to use for log output.")
    parser.add_argument(
        "-w",
        "--work_dir",
        required=False,
        default=DEFAULT_WORK_DIR,
        help="Directory where temporary CSV results will be stored.  Defaults to <current_directory>/" + DEFAULT_WORK_DIR
    )
    args = parser.parse_args()

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