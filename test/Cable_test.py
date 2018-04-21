import unittest
import sys
sys.path.append('../src')
import Cable

E_MAJ_OPEN = (0, 2, 2, 1, 0, 0)
A_MIN_OPEN = ('x', 0, 2, 2, 1, 0)


class CableTest(unittest.TestCase):

    def test_E_MAJ(self):
        self.assertTrue(E_MAJ_OPEN in Cable.find('E'))


if __name__ == '__main__':
    unittest.main()
