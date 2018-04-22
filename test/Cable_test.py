import unittest
import sys
sys.path.append('../src')
from Cable import Cable
from constants import STANDARD, Note, Quality, Interval, Extended

E_MAJ_OPEN = [0, 2, 2, 1, 0, 0]
E_MAJ_9 = [0, 2, 1, 1, 0, 2]
Eb_MAJ_9 = [11, 13, 12, 12, 11, 13]
A_MIN_OPEN = [Note.X, 0, 2, 2, 1, 0]


class CableTest(unittest.TestCase):

    def test_E_MAJ(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, quality=Quality.MAJ)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MAJ_OPEN in results)

    def test_A_MAJ(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.A, quality=Quality.MIN)
        results = list(results)
        print(len(results))
        self.assertTrue(A_MIN_OPEN in results)

    def test_E_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, quality=Quality.MAJ,
                                 extended=Extended.E9)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MAJ_9 in results)

    def test_Eb_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.Eb, quality=Quality.MAJ,
                                 extended=Extended.E9)
        results = list(results)
        print(len(results))
        self.assertTrue(any(filter(lambda x: x[0] == 11 and x[1] == 13,
                                   results)))
        self.assertTrue(Eb_MAJ_9 in results)


if __name__ == '__main__':
    unittest.main()
