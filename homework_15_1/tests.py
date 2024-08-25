from django.test import TestCase

# Create your tests here.
import json
import os
import unittest


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test.json'
        self.test_data = {
            "name": "Test",
            "age": 30,
            "city": "New York"
        }

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read_file(self):
        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)

        with open(self.test_file, 'r') as f:
            data = json.load(f)

        self.assertEqual(data, self.test_data)
        self.assertIsInstance(data['name'], str)
        self.assertIsInstance(data['age'], int)
        self.assertIsInstance(data['city'], str)

    def test_write_and_read_empty_file(self):
        empty_data = {}
        with open(self.test_file, 'w') as f:
            json.dump(empty_data, f)

        with open(self.test_file, 'r') as f:
            data = json.load(f)

        self.assertEqual(data, empty_data)

    def test_read_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            with open('nonexistent.json', 'r') as f:
                json.load(f)

    def test_write_bad_data_into_file(self):
        bad_data = set([1, 2, 3])
        with self.assertRaises(TypeError):
            with open(self.test_file, 'w') as f:
                json.dump(bad_data, f)


import unittest

class TestTextProcessing(unittest.TestCase):

    def test_clean_text_removes_non_letters(self):
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("123 ABC!!!"), "abc")

    def test_clean_text_to_lowercase(self):
        self.assertEqual(clean_text("HeLLo WoRLD"), "hello world")

    def test_clean_text_on_empty_string(self):
        self.assertEqual(clean_text(""), "")

    def test_remove_stop_words(self):
        self.assertEqual(remove_stop_words("this is a test", ['this', 'is']), "a test")

    def test_remove_stop_words_no_clean_text(self):
        self.assertEqual(remove_stop_words("this is a test", ['this', 'is']), "a test")

    def test_remove_stop_words_no_stop_words(self):
        self.assertEqual(remove_stop_words("hello world", []), "hello world")
