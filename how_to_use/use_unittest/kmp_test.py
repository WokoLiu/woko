import unittest
from algorithm.kmp import kmp, overlay


class KmpTest(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')

    @classmethod
    def setUpClass(cls):
        print('setupclass')

    @classmethod
    def tearDownClass(cls):
        print('teardownclass')

    def test_input(self):
        with self.assertRaises(TypeError):
            overlay(234)

    def test_kmp(self):
        self.assertIsInstance(kmp('abaabaabbabaaabaabbabaab', 'abaabbabaab'), int)

    def test_kmp2(self):
        self.assertFalse(kmp('sldfjlskfj', 'skdmfkdkmfk'))


if __name__ == '__main__':
    unittest.main()
