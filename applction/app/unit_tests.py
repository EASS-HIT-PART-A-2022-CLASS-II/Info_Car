import unittest
import requests
import main
import pymongo

class SmokeTest(unittest.TestCase):
    def test_status_code(self):
        self.assertEqual(requests.get("http://127.0.0.1").status_code, 200)
    


if __name__ == '__main__':
    unittest.main()

