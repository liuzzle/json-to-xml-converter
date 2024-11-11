# JSON to XML Converter

This project provides a command-line interface (CLI) tool to convert JSON files into XML format, dividing the data into training and test datasets based on a customizable reservoir size. It logs processing details and outputs separate XML files for training and testing data. It also includes unit tests for core functions.

### Features

  •	JSON to XML Conversion: Converts a JSON file into XML format.
  
  •	Reservoir Sampling: Splits data into test and train sets using a reservoir sampling technique.
  
  •	Logging: Logs the count of JSON elements, train, and test data in a text file.
  
•	Weekend Filter: Filters data to include only entries created on weekends.

## Getting Started

### Prerequisites

  •	Python 3.x
	•	Required packages: argparse, ijson, lxml, datetime, logging, random, pytest

### Installation

  1.	Clone this repository.
	2.	Navigate to the project directory:

  `$cd path/to/project`

  3.	Install dependencies:

  `$pip install -r requirements.txt`



### Usage

From the root directory, use the following command to run the converter:

  `$python3 src/__main__.py --json_file path/to/input.json --xml_train path/to/train.xml --xml_test path/to/test.xml --number RESERVOIR_SIZE`

Example:

  `$python3 src/__main__.py --json_file files/review_large.json --xml_train files/train.xml --xml_test files/test.xml --number 3000`

### Command-Line Arguments

  •	--json_file: Path to the JSON file to be converted.
	•	--xml_train: Path for the output training XML file.
	•	--xml_test: Path for the output test XML file.
	•	--number: Reservoir size (integer) determining the number of test samples.

## Project Structure

  •	src/__main__.py: CLI interface to convert JSON to XML with test/train split.
	•	src/converter.py: Contains the JsonConverterToXML class responsible for:
	•	Reading JSON data
	•	Filtering weekend entries
	•	Splitting data with reservoir sampling
	•	Writing to XML files
	•	Logging metadata
	•	tests/Test_json_converter_to_xml.py: Unit tests for JsonConverterToXML functions using pytest.

### Logging

Logs are saved in files/converter_logs.txt with the following details:

  •	Total JSON elements processed
	•	Elements written in test and train XML files

### Testing

To run the tests:

  `$pytest tests/Test_json_converter_to_xml.py`

### Author

This project was created with guidance and optimization suggestions from ChatGPT.
