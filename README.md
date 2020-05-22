# JSON File Parser
## Description
This JSON file parser was created for an interview coding challenge.  The task was to create a JSON file parser that takes several JSON files as input and generates a single combined CSV file of a particular format.  The parser must read these files in parallel, rather than working on them one at a time.  It must also be assumed that these files could be very large (hundreds of megabytes).  Unit tests and build instructions/scripts were also requested.
### Sample Input/Output
Input:
```
{"person":{"first_name":"Rashawn","last_name":"Goldner","address":{"line1":"139 Nicolas Meadows","line2":"Apt. 549","city":"side","state":"ID","zip":"55154"}},"data":{"content":"Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.","date":"2013-02-07T16:10:14.117-06:00"}}
```
Output:

First Name,Last Name,Content,Date
```
Rashawn,Goldner,Eaque eius at. Neque dolorem expedita et est debitis praesentium ipsam. Perspiciatis occaecati quaerat nihil est maiores qui et.,2013-02-07T16:10:14.117-06:00
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
## Assumptions
