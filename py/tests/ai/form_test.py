import unittest
from pathlib import Path

from davidkhala.azure.ai.form import Recognizer
from davidkhala.azure.ci import credentials

credential = credentials()


class DocumentIntelligence(unittest.TestCase):

    def setUp(self):
        endpoint = 'https://davidkhala-form-recognizer.cognitiveservices.azure.com/'
        self.client = Recognizer(endpoint, credential)

    def test_entire(self):
        file = Path(__file__).parent.parent / "fixtures" / "transcript.png"
        r = self.client.extract_entities(file)
        print(r)
    def test_focus(self):
        file = Path(__file__).parent.parent / "fixtures" / "transcript.png"
        focus = ['Student','DateOfBirth' ] # 'Date of Birth' will throw error
        r = self.client.extract_entities(file, focus)
        self.assertListEqual([{'DateOfBirth': 'Oct 27, 1910', 'Student': 'Teddy Roosevelt'}], r)


if __name__ == '__main__':
    unittest.main()
