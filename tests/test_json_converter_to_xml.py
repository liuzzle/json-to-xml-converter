####Imports####
import pytest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
import logging
import json
from src.converter import JsonConverterToXML
###############

# To have a class object to work with i use this decorator to be able to use this in the tests
@pytest.fixture
def settingup_converter():
    json_file = "files/review.json"
    xml_train_path = "train.xml"
    xml_test_path = "test.xml"
    reservoir_size = 3
    converter = JsonConverterToXML(json_file, xml_train_path, xml_test_path, reservoir_size)
    return converter

def test_initialization(settingup_converter):
    converter = settingup_converter
    assert converter.json_file == "files/review.json"
    assert converter.xml_train_path == "train.xml"
    assert converter.xml_test_path == "test.xml"
    assert converter.reservoir_size == 3

def test_set_logger(settingup_converter):
    logger = settingup_converter.set_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

def test_get_date(settingup_converter):
    element = {"date": "2020-01-12 12:12:12"}
    expected_object = datetime(2020, 1, 12, 12, 12, 12)
    assert settingup_converter.get_date(element) == expected_object

def test_find_file_name(settingup_converter):
    file_path = "files/review.json"
    assert settingup_converter.find_file_name(file_path) == "review.json"

def test_is_weekend(settingup_converter):
    element_weekend = {'date': '2024-05-11 08:30:00'}
    element_weekday = {'date': '2024-05-09 08:30:00'}
    elements = [element_weekend, element_weekday]
    json_data = json.dumps(elements)

    # Here I had to as ChatGPT to find out how to test opening a json file and testing if it is a weekend
    with patch("builtins.open", mock_open(read_data=json_data)), \
        patch("ijson.items", return_value=iter(elements)):
        logger = settingup_converter.set_logger()
        weekend_elements = list(settingup_converter.is_weekend(logger))
        assert len(weekend_elements) == 1
        assert weekend_elements[0] == element_weekend

# I wrote these two tests with the help of ChatGPT since I didnt know how to simulate a xml and test the writing
# Some parts are were changed
# Prompt: "How do I write a test for constructing a XML, setting up a logger and writing it into a XML file with pytest"
def test_test_data_split(settingup_converter):
    elements = [
        {"date": "2023-05-14 12:34:56"},
        {"date": "2023-05-13 12:34:56"},
        {"date": "2023-05-07 12:34:56"},
        {"date": "2023-05-06 12:34:56"}
    ]
    json_data = json.dumps(elements)

    with patch("builtins.open", mock_open(read_data=json_data)), patch("ijson.items", return_value=iter(elements)):
        logger = settingup_converter.set_logger()
        test_data = settingup_converter.test_data_split(logger)
        assert len(test_data) == settingup_converter.reservoir_size

@patch("lxml.etree.Element")
@patch("lxml.etree.SubElement")
@patch("lxml.etree.xmlfile")
def test_write_xml(mock_xmlfile, mock_subelement, mock_element, settingup_converter):
    elements = [{
        "review_id": "1", "user_id": "u1", "business_id": "b1",
        "stars": 5, "useful": 0, "funny": 0, "cool": 0,
        "text": "Good", "date": "2023-05-14 12:34:56"
    }]
    logger = settingup_converter.set_logger()

    # Simulate XML writing context
    mock_context_manager = MagicMock()
    mock_xmlfile.return_value.__enter__.return_value = mock_context_manager

    settingup_converter.write_xml(elements, settingup_converter.xml_test_path, logger)

    mock_xmlfile.assert_called_once_with(settingup_converter.xml_test_path, encoding='utf-8')
    assert mock_subelement.call_count == 6



