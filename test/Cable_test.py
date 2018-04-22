import unittest
import sys
sys.path.append('../src')
import chordUtils as cu
from Cable import Cable
from constants import STANDARD, Note, Quality, Interval, Extended

E_MAJ_OPEN = [0, 2, 2, 1, 0, 0]
E_MAJ_7 = [0, 2, 1, 1, 0, 0]
E_MAJ_9 = [0, 2, 1, 1, 0, 2]
E_MIN_7_b13 = [0, 2, 0, 0, 1, 0]
Eb_MAJ_9 = [11, 13, 12, 12, 11, 13]
A_MIN = [Note.X, 0, 2, 2, 1, 0]
A_MIN_7 = [Note.X, 0, 2, 0, 1, 0]


class CableTest(unittest.TestCase):

    def test_E_MAJ(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, quality=Quality.MAJ)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MAJ_OPEN in results)

    def test_A_MIN(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.A, quality=Quality.MIN)
        results = list(results)
        print(len(results))
        self.assertTrue(A_MIN in results)

    def test_A_MIN_7(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(
            Note.A, quality=Quality.MIN, extended=Extended.E7)
        results = list(results)
        print(len(results))
        self.assertTrue(A_MIN_7 in results)

    def test_E_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, quality=Quality.MAJ,
                                 extended=Extended.E9)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MAJ_9 in results)

    def test_E_MIN_7_b13(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, Interval.b13, quality=Quality.MIN,
                                 extended=Extended.E7, )
        results = list(results)
        print(len(results))
        self.assertTrue(E_MIN_7_b13 in results)

    def test_Eb_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.Eb, quality=Quality.MAJ,
                                 extended=Extended.E9)
        self.assertTrue(any(filter(lambda x: x[0] == 11 and x[1] == 13,
                                   results)))
        self.assertTrue(Eb_MAJ_9 in results)

    def test_intervals(self):
        # self.interval_helper(Note.Eb, Quality.MAJ, extended=Extended.E9)
        self.interval_helper(Note.A, Quality.MIN,
                             Interval.b13, extended=Extended.E7)
        # self.interval_helper(Note.E, Quality.MAJ)

    def interval_helper(self, note, quality, *add, extended=None):
        cable = Cable(STANDARD, 3)
        results = cable.generate(
            note, quality=quality, extended=extended, *add)
        intervals = set(cu.get_intervals(None, note, quality, extended, *add))
        result_intervals = list(map(lambda x: cu.get_intervals_from_fingering(
            STANDARD, note, x), results))
        result_set = set(map(frozenset, result_intervals))
        print(result_set)

        self.assertTrue(all(map(lambda x: intervals == x, result_intervals)))


if __name__ == '__main__':
    unittest.main()
