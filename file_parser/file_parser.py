import logging
import json
import csv

class FileParser:
    def __init__(self):
        pass

    def parse_file(self, input_file_location, output_file_location):
        logging.debug(f"File {input_file_location} will be parsed and output to {output_file_location}")

        with open(output_file_location, "w", newline='') as output_file:
            writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            with open(input_file_location, "r") as input_file:
                for line in input_file:
                    json_line = json.loads(line.rstrip())
                    first_name = json_line["person"]["first_name"]
                    last_name = json_line["person"]["last_name"]
                    content = json_line["data"]["content"]
                    date = json_line["data"]["date"]
                    writer.writerow([first_name, last_name, content, date])
        return "somefile"
