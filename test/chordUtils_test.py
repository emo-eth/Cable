import unittest
import sys
sys.path.append('../src')
import chordUtils as cu
from constants import Quality, Degree, Note, Interval, Extended, Add


class ChordUtilsTest(unittest.TestCase):

    def test_quality_intervals(self):
        intervals = set(cu.get_intervals(None, 'A', Quality.MAJ, None))
        self.assertTrue(len(intervals) == 3)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_THIRD in intervals)
        self.assertTrue(Interval.PERFECT_FIFTH in intervals)

    def test_extended_intervals(self):
        intervals = set(cu.get_intervals(None, 'A', Quality.MAJ, Extended.E9))
        self.assertTrue(len(intervals) == 5)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_SEVENTH in intervals)
        self.assertTrue(Interval.MAJOR_SECOND in intervals)

    def test_extended_add_intervals(self):
        intervals = set(cu.get_intervals(None, 'A', Quality.MAJ, Extended.E9,
                                         Add.b9))
        self.assertTrue(len(intervals) == 5)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_SEVENTH in intervals)
        self.assertTrue(Add.b9 in intervals)


if __name__ == '__main__':
    unittest.main()
