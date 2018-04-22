import unittest
import sys
sys.path.append('../src')
import chordUtils as cu
from constants import Quality, Degree, Note, Interval, Extension


class ChordUtilsTest(unittest.TestCase):

    def test_quality_intervals(self):
        intervals = set(cu.get_intervals(Note.A, Quality.MAJ, None))
        self.assertTrue(len(intervals) == 3)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_THIRD in intervals)
        self.assertTrue(Interval.PERFECT_FIFTH in intervals)

    def test_extension_intervals(self):
        intervals = set(cu.get_intervals(Note.A, Quality.MAJ, Extension.E9))
        self.assertTrue(len(intervals) == 5)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_SEVENTH in intervals)
        self.assertTrue(Interval.MAJOR_SECOND in intervals)

    def test_extension_intervals_minor(self):
        intervals = set(cu.get_intervals(Note.A, Quality.MIN, Extension.E7))
        self.assertTrue(len(intervals) == 4)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MINOR_THIRD in intervals)
        self.assertTrue(Interval.PERFECT_FIFTH in intervals)
        self.assertTrue(Interval.MINOR_SEVENTH in intervals)

    def test_extension_add_intervals(self):
        intervals = set(cu.get_intervals(Note.A, Quality.MAJ, Extension.E9,
                                         Interval.b9))
        self.assertTrue(len(intervals) == 5)
        self.assertTrue(Interval.ROOT in intervals)
        self.assertTrue(Interval.MAJOR_SEVENTH in intervals)
        self.assertTrue(Interval.b9 in intervals)

    def test_get_relative_interval(self):
        self.assertEqual(cu.get_relative_interval(Note.E, Note.A,
                                                  Interval.PERFECT_FIFTH),
                         Interval.MAJOR_SECOND)
        self.assertEqual(cu.get_relative_interval(Note.E, Note.Cs,
                                                  Interval.PERFECT_FIFTH),
                         Interval.MINOR_SEVENTH)

    def test_13(self):
        intervals = cu.get_intervals(Note.E, None, Extension.E13)
        print(intervals)
        self.assertEqual(len(intervals), 7)

    def test_11(self):
        intervals = cu.get_intervals(Note.E, Quality.MAJ, Extension.E11)
        print(intervals)
        self.assertEqual(len(intervals), 6)


if __name__ == '__main__':
    unittest.main()
