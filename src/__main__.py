'''
A CLI to customize files and reservoir size, it imports the custom class JsonConverterToXML which is able to read
a json file, split it into test and training data and saves that data in two separate XML files.
It also creates a txt file to save logs of the amount of elements in the json, train and test file.

To run the program, change directory to the exercise folder and run a similar command as: 
python3 src/___main__.py --json_file files/review_large.json --xml_train files/train.xml --xml_test files/test.xml --number 3000
'''

############## Imports##########
import argparse
from converter import JsonConverterToXML
################################

def test_pos_number(number: int) -> None:
    """
    This function checks if a number is positive.

    Args:
        number (int): number
    """
    if number < 0:
        raise ValueError("Reservoir size needs to be at least 0")


def main():
    # The ArgumentParser object is defined, which includes the description. 
    # It used to include the program's name as sys.argv[0] yet that used some additional memory so I removed that part
    parser = argparse.ArgumentParser(description='This program creates a CLI with argparse to convert a given json file into a xml file.')

    # All the required arguments are added and the types of the arguments are defined.
    # Required arguments are saved as such
    parser.add_argument(
        '-jf', '--json_file', type=str, help='Absolute path to the Json file that is to be converted into XML', required=True)
    parser.add_argument(
        '-xtest', '--xml_test', type=str, help='Absolute path to the test XML that is to be created by writing the json-files content into it', required=True)
    parser.add_argument(
        '-xtrain', '--xml_train', type=str, help='Absolute path to the train XML that is to be created by writing the json-files content into it', required=True)
    parser.add_argument(
        '-n', '--number', type=int, help='Reservoir size for the test data xml', required=True)
    args = parser.parse_args()

    # The -n flag is checked to see if it is positive if not then an error is raised.
    test_pos_number(args.number)

    # An object of the class JsonConverterToXML is created where the paths and the reservoir number are added
    json_converted_object = JsonConverterToXML(args.json_file, args.xml_train, args.xml_test, args.number)
    logger = json_converted_object.set_logger()

    # Test data is split with the reservoir sampling method and returned and the training data is defined in a generator function
    test_data = json_converted_object.test_data_split(logger)
    training_data = (element for element in json_converted_object.is_weekend(logger) if element not in test_data)

    # Since we have a training data iterable and a test data list, they are written into two different xml files
    json_converted_object.write_xml(test_data, args.xml_test, logger)
    json_converted_object.write_xml(training_data, args.xml_train, logger)
    

if __name__ == '__main__':
    main()