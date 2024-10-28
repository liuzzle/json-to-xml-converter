'''
The JsonConverterToXML class creates instances of an existing json path, a train and test xml path in which the json data will be written and a reservoir size. 
The class reads the json file, splits it into test and training data according to the customizable reservoir size. 
Finally, the two containers with data are written into two xml files.
'''

############## Imports##########
import ijson
from lxml import etree as ET
from datetime import datetime
import logging
import random
from typing import Iterable
###############################


class JsonConverterToXML:
    # To be able to keep track of how many time the is_weekend() function gets called, I created this class function. I had the problem that the logging was done each time this function was called.
    # Thus, with this variable, i can keep track of the calles and only log the json element count ones.
    is_weekend_function_iteration = 0

    def __init__(self, json_file: str, xml_train_path: str, xml_test_path: str, reservoir_size: int) -> None:
        """
        This function initiates the command-line arguments

        Args:
            json_file (str): relative path to the existing json file
            xml_train_path (str): relative path to the goal train xml path
            xml_test_path (str): relative path to the goal test xml path
            reservoir_size (int): reservoir size and also test data size simultaneously
        """
        self.json_file = json_file
        self.xml_train_path =xml_train_path
        self.xml_test_path = xml_test_path
        self.reservoir_size = reservoir_size

    # Here are some static methods that are needed in this class yet need no access to class instances 
    @staticmethod
    def set_logger() -> logging.Logger:
        """
        Sets up a logger with a txt destination and a specific format

        Returns:
            Logger: Logger to then add entries to
        """
        # I set up a Logger
        # Gets logger with the name or creates a new one which is set as the script name
        logger = logging.getLogger('root')
        # Set log level to INFO
        logger.setLevel(logging.INFO)
        # Create file that stores logs, thus the log don't get outputed in the terminal but stored!
        handler = logging.FileHandler("files/converter_logs.txt")
        # Set specific format as instructed
        formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    @staticmethod
    def get_date(element: dict) -> datetime:
        """
        Creates a datetime object from a string representing a date and time and a corresponding format string.

        Args:
            element (dict): dictionary, here in a json file

        Returns:
            datetime: datetime object
        """
        return datetime.strptime(
                        element['date'], '%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def find_file_name(file: str) -> str:
        """
        This function searches

        Args:
            file (str): relative path to a file

        Returns:
            str: file name as string
        """
        filename= file.split('/')[-1]
        if filename:
            return filename
        else:
            raise ValueError(f"Invalid file path {file}")
    
    @staticmethod
    def set_date_attributes(root: str, date: datetime) -> None:
        """
        Extracts date values from datetime objects and stores it as an subelement in an xml file

        Args:
            root (str): root of xml docyment
            date_str (datetime): datetime object
        """
        # I asked ChatGPT how to make this more memory efficient and it recommended using a generator function here too and to then convert it into a dictionary, thus I used this now.
        # Propt: "How can I make this more memory efficient: date_attribute = {'year': str(date.year), 'month': str(date.month), 'day': str(date.day), 'weekday': str(date.strftime('%A'))} ET.SubElement(review_root, 'date',attrib=date_attribute) xml_file.write(review_root, pretty_print=True)"
        date_attributes = (str(getattr(date, attribute)) if attribute != 'weekday' else date.strftime("%A") for attribute in ['year', 'month', 'day', 'weekday'])
        ET.SubElement(root, 'date',
                    attrib=dict(zip(['year', 'month', 'day', 'weekday'], date_attributes)))
        
    def is_weekend(self, logger: logging.Logger) -> Iterable[dict]:
        """
        Iterates through the json file in a memory efficient way and yield the elements that were written on a weekend.
        In the first function call, it also logs the number of json elements in the json file in a txt.

        Args:
            logger (logging.Logger): Logger object to log entries in

        Returns:
            Iterable[dict]: generator with dictionary entry reviews written on a weekend
        """
        # Start json element counter
        json_counter = 0
        # Iterate through the json elements and yield those written on a weekend
        for element in ijson.items(open(self.json_file), 'item'): 
            json_counter += 1
            if self.get_date(element).weekday() >= 5:
                yield element
        # log json element count if the function was called for the first time to avoid duplicates
        if self.is_weekend_function_iteration == 0:
            logger.info(f"Processed {json_counter} reviews from file {self.find_file_name(self.json_file)}")
            self.is_weekend_function_iteration += 1

    def test_data_split(self, logger: logging.Logger) -> list[dict]:
        """
        Iterates through elements that were in a json and splits the content into test data, 
        according to the specified reservoir size.

        Args:
            logger (logging.Logger): Logger object to log entries in

        Returns:
            list[dict]: Test data elements
        """
        test_data = []
        # Iterates through the Iterable and randomly samples n elements to append to the test data list
        for i, element in enumerate(self.is_weekend(logger)):
            if i < self.reservoir_size:
                test_data.append(element)
            else:
                random_number = random.randint(0, i)
                if random_number < self.reservoir_size:
                    test_data[random_number] = element 
        return test_data

    def write_xml(self, iterable: (Iterable[dict]| list[dict]), xml_path: str, logger: logging.Logger) -> None:
        """
        Iterates through the list or iterable and writes the elements hierarchically into a XML file.
        Simultaneously, keeps track of the element count and logs it.

        Args:
            iterable (Iterable[dict] |  list[dict]): Has the elements that were in the json file
            xml_path (str): desired XML goal path
            logger (logging.Logger): Logger object to log entries in
        """
        # Open a XML file in the desired destination and start with a root element
        with ET.xmlfile(xml_path, encoding='utf-8') as xml_file:
            xml_file.write_declaration()
            with xml_file.element('root'):
                # Keep track of the written elements
                xml_counter = 0
                # Iterate through the elements and write their entries as subelements into the XML
                for json_element in iterable:
                    # Increment the xml file element counter
                    xml_counter += 1
                    # Get datetime onject from the dictionary element
                    date = self.get_date(json_element)
                    # Now an XML structure is build for each valid element 
                    review_root = ET.Element('review')
                    ET.SubElement(
                        review_root, 'review_id').text = json_element['review_id']
                    ET.SubElement(
                        review_root, 'user_id').text = json_element['user_id']
                    ET.SubElement(
                        review_root, 'business_id').text = json_element['business_id']
                    ET.SubElement(review_root, 'ratings', stars=str(json_element['stars']), useful=str(
                        json_element['useful']), funny=str(json_element['funny']), cool=str(json_element['cool']))
                    ET.SubElement(
                        review_root, 'text').text = json_element['text']
                    # Use function to set the dates as elements in the xml 
                    self.set_date_attributes(review_root, date)
                    xml_file.write(review_root, pretty_print=True)
                    # The xml-element is always cleared after writing as to not store it into memory
                    review_root.clear()
        # Log the XML element count
        logger.info(f"Processed {xml_counter} reviews from file {self.find_file_name(xml_path)}")