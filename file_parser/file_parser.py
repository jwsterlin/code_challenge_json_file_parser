import logging
import json
import csv
import shutil
import io

class FileParser:
    def __init__(self):
        pass

    def parse_file(self, input_file_location, output_file_location):
        logging.debug(f"File {input_file_location} will be parsed and output to {output_file_location}")

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        is_first_line = True
        with open(input_file_location, "r", newline='') as input_file:
            with open(output_file_location, "w", newline='') as output_file:
                for line in input_file:
                    if not is_first_line:
                        output_file.write(output.getvalue().rstrip() + "\n")
                        output.truncate(0)
                        output.seek(0)
                    is_first_line = False
                    json_line = json.loads(line.rstrip())
                    first_name = json_line["person"]["first_name"]
                    last_name = json_line["person"]["last_name"]
                    content = json_line["data"]["content"]
                    date = json_line["data"]["date"]

                    writer.writerow([first_name, last_name, content, date])
                output_file.write(output.getvalue().rstrip())


    def combine_csvs(self, input_csv_file_locs, output_csv_file_loc):
        num_files = len(input_csv_file_locs)
        cur_file = 0
        with open(output_csv_file_loc, "w") as output_csv_file:
            for input_csv_file_loc in input_csv_file_locs:
                cur_file = cur_file + 1
                with open(input_csv_file_loc, "r") as input_csv_file:
                    shutil.copyfileobj(input_csv_file, output_csv_file)
                    if cur_file != num_files:
                        output_csv_file.write("\n")
