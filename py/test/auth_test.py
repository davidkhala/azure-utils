import unittest
from auth import get_credential

class MyTestCase(unittest.TestCase):
    def test_credential(self):
        cred = get_credential()


if __name__ == '__main__':
    unittest.main()
