import unittest
import sys
sys.path.append('../Cable')
from Cable.constants import Quality, Degree, Note, Interval, Extension


class ConstantsTest(unittest.TestCase):

    def test_interval_to(self):
        self.assertEqual(Note.C.interval_to(Note.G), Interval.PERFECT_FIFTH)

    def test_interval_add(self):
        self.assertEqual(Interval.MINOR_SECOND + Interval.MINOR_SEVENTH,
                         Interval.MAJOR_SEVENTH)

    def test_note_add_interval(self):
        # TODO: implement subtract for intervals?
        self.assertEqual(Note.C + Interval.PERFECT_FIFTH, Note.G)

    def test_subtract_intervals(self):
        self.assertEqual(Interval.PERFECT_FIFTH - Interval.PERFECT_FOURTH,
                         Interval.MAJOR_SECOND)
        self.assertEqual(Interval.PERFECT_FOURTH - Interval.PERFECT_FIFTH,
                         Interval.MINOR_SEVENTH)

    def test_inequality(self):
        self.assertTrue(Interval.PERFECT_FIFTH > Interval.PERFECT_FOURTH)

    def _test_distinguish_intervals(self):
        self.assertFalse(Interval.AUGMENTED_SIXTH in
                         set([Interval.MINOR_SEVENTH]))

    def test_x_false(self):
        self.assertFalse(Note.X)


if __name__ == '__main__':
    unittest.main()
