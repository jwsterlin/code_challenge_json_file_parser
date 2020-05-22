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

        with open(input_file_location, "r", newline='') as input_file:
            with open(output_file_location, "w", newline='') as output_file:
                writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for line in input_file:
                    results = self.parse_line(line)
                    if results != None:
                        writer.writerow(results)

    def parse_line(self, line):
        try:
            json_line = json.loads(line.rstrip())
        except Exception as e:
            logging.warn(f"Couldn't translate line to JSON.  Line: {line}.  Error: {e}")
            return

        first_name = json_line.get("person", {}).get("first_name")
        if first_name is None:
            return

        last_name = json_line.get("person", {}).get("last_name")
        if last_name is None:
            return

        content = json_line.get("data", {}).get("content")
        if content is None:
            return

        date = json_line.get("data", {}).get("date")
        if date is None or date == "":
            return

        return [first_name, last_name, content, date]


    def combine_csvs(self, input_csv_file_locs, output_csv_file_loc):
        with open(output_csv_file_loc, "w") as output_csv_file:
            for input_csv_file_loc in input_csv_file_locs:
                with open(input_csv_file_loc, "r") as input_csv_file:
                    shutil.copyfileobj(input_csv_file, output_csv_file)
