"""
Unit tests for the util module responsible for handling json files
"""

from pathlib import Path

from quafel_simulators.tests.util import TestCase
from quafel_simulators.util.json_handler import (
    read_dict,
    write_json_file,
    read_json_file,
)


class TestJsonHandler(TestCase):
    """
    Test the json_handler module
    """

    def test_read_dict_without_file(self):
        """
        Test if the read_dict method creates a file if it does not exist
        """

        # assure the file is not existent
        Path("test.json").unlink(missing_ok=True)

        # read the dict
        read = read_dict("test.json")

        # check if the dict is empty
        assert read == {}

    def test_write_and_read_dict(self):
        """
        Test if the write and read of a dict works
        """

        # write the dict
        write_json_file("test.json", {"test": "test"})

        # read the dict
        read = read_json_file("test.json")

        # check if the dict is correct
        assert read == {"test": "test"}

    def test_write_and_read_list(self):
        """
        Test if the write and read of a list works
        """

        # write the list
        write_json_file("test.json", ["test", "test"])

        # read the list
        read = read_json_file("test.json")

        # check if the list is correct
        assert read == ["test", "test"]
