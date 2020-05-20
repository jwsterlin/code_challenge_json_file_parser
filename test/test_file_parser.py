import unittest
from file_parser.file_parser import FileParser

class TestFileParser(unittest.TestCase):

    def test_parse_file(self):
        fp = FileParser()
        fp.parse_file("input_files/23222DSR.txt")
        self.assertEqual(1, 1)