# JSON File Parser
## Description
This JSON file parser was created for an interview coding challenge.  The task was to create a JSON file parser that takes several JSON files as input and generates a single combined CSV file of a particular format.  The parser must read these files in parallel, rather than working on them one at a time.  It must also be assumed that these files could be very large (hundreds of megabytes).  Unit tests and build instructions/scripts were also requested.
### Sample Input/Output
Input:
```
{"person":{"first_name":"John","last_name":"Doe","address":{"line1":"123 fake street","line2":"Apt. 549","city":"side","state":"ID","zip":"55154"}},"data":{"content":"Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.","date":"2013-02-07T16:10:14.117-06:00"}}
```
Output:

First Name,Last Name,Content,Date
```
John,Doe,Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.,2013-02-07T16:10:14.117-06:00
```

## Installation
Requirements:
* Git
* Python 3

For the purposes of this exercise simply clone this git repository to your local machine
```
git clone https://github.com/jwsterlin/code_challenge_json_file_parser.git
```

## Running the script
You can pass the -h flag to see all possible inputs.

```
Unix: $ python3 parse_files.py -h
Windows: > python.exe parse_files.py -h

usage: parse_files.py [-h] -i INPUT_DIR -o OUTPUT_FILE [--log_location LOG_LOCATION] [--log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG,critical,error,warning,info,debug}] [-w WORK_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Location of a directory that contains JSON files to be parsed.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file location where CSV results will be stored.
  --log_location LOG_LOCATION
                        Location to use for log output. Defaults to <current_directory>/parse_files.log.
  --log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG,critical,error,warning,info,debug}
                        Log level. Defaults to INFO.
  -w WORK_DIR, --work_dir WORK_DIR
                        Directory where temporary CSV results will be stored. Defaults to <current_directory>/work_dir.
```

For example:
```
python3 parse_files.py -i input_files -o output.csv --log_level DEBUG --log_location somelog.log -w myworkdir
```

## Assumptions
Here are some assumptions I made that I would typically bring up with the stakeholder of the project:
* Assumed that the space before Doe in the original example document was present because " Doe" was specified in file, and was not adding the space myself.
* Invalid data in any column invalidates the entire row, causing it not to be printed out.  So, if the input file had invalid JSON, or if any of the parsed fields was not present, that line was skipped.
* Assumed no header desired for the output CSV file.
* No advanced validation desired on names and dates.  "2345" is an acceptable name in this case.  The dates seem to all be of the same format, but I don't want to assume they always will be without outside verification.
* Incoming double quotes will be escaped as \\" in the JSON input file

## Performance
This script takes about a minute to process 3.3G on my home machine.  As we approach tens or hundreds of GB, I would recommend changing to golang or involving other toolsets.  Python was chosen here as it is well known by the interviewing company and best equips me to demonstrate my familiarity with the language.