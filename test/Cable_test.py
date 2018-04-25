import unittest
import sys
sys.path.append('../src')
import chordUtils as cu
from Cable import Cable
from constants import STANDARD, Note, Quality, Interval, Extension
from util import min_max
from chordUtils import Chord

E_MAJ_OPEN = [0, 2, 2, 1, 0, 0]
E_MAJ_7 = [0, 2, 1, 1, 0, 0]
E_MAJ_9 = [0, 2, 1, 1, 0, 2]
E_MIN_7_b13 = [0, 2, 0, 0, 1, 0]
Eb_MAJ_9 = [6, 5, 3, 3, 4, 3]
ALT_Eb_MAJ_9 = [3, 5, 3, Note.X, 4, 6]
A_MIN = [Note.X, 0, 2, 2, 1, 0]
A_MIN_7 = [Note.X, 0, 2, 0, 1, 0]
E_MIN_7 = [0, 2, 0, 0, 0, 0]


class CableTest(unittest.TestCase):

    def test_chord_obj(self):
        cable = Cable()
        chord = Chord(Note.E, bass=Note.E, quality=Quality.MIN,
                      extension=Extension.E7)
        results = list(cable.generate(chord))
        self.assertTrue(len(results) > 0)

    def test_open_E_MIN_7(self):
        cable = Cable()
        results = list(cable.generate(
            Note.E, quality=Quality.MIN, extension=Extension.E7))
        self.assertTrue(E_MIN_7 in results)

    def test_slash(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.A, bass=Note.G, quality=Quality.MAJ)
        first_intervals = map(lambda result:
                              cu.get_notes_from_fingering(STANDARD, Note.A,
                                                          result)[0], results)
        first_notes = list(map(lambda interval: Note.A + interval,
                               first_intervals))
        print(first_notes)
        self.assertTrue(all(map(lambda note: note == Note.G, first_notes)))

    def test_slash_root(self):
        cable = Cable()
        results = list(cable.generate(Note.E, bass=Note.E, quality=Quality.MIN,
                                      extension=Extension.E7))
        self.assertTrue(len(results) > 0)

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
            Note.A, quality=Quality.MIN, extension=Extension.E7)
        results = list(results)
        print(len(results))
        self.assertTrue(A_MIN_7 in results)

    def test_E_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, quality=Quality.MAJ,
                                 extension=Extension.E9)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MAJ_9 in results)

    def test_fingers(self):
        cable = Cable(STANDARD, 3, 3)
        results = cable.generate(Note.Eb, quality=Quality.MAJ,
                                 extension=Extension.E9)
        results = list(results)
        self.assertFalse(Eb_MAJ_9 in results)
        self.assertFalse(ALT_Eb_MAJ_9 in results)

    def test_E_MIN_7_b13(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E, Interval.b13, quality=Quality.MIN,
                                 extension=Extension.E7)
        results = list(results)
        print(len(results))
        self.assertTrue(E_MIN_7_b13 in results)

    def test_Eb_MAJ_9(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.Eb, quality=Quality.MAJ,
                                 extension=Extension.E9)
        results = list(results)
        print(len(results))
        self.assertTrue(Eb_MAJ_9 in results)

    def test_intervals(self):
        # self.interval_helper(Note.Eb, Quality.MAJ, extension=Extension.E9)
        self.interval_helper(Note.A, Quality.MIN,
                             Interval.b13, extension=Extension.E7)
        # self.interval_helper(Note.E, Quality.MAJ)

    def interval_helper(self, note, quality, *add, extension=None):
        cable = Cable(STANDARD, 3)
        results = cable.generate(
            note, quality=quality, extension=extension, *add)
        intervals = set(cu.get_intervals(note, quality, extension, *add))
        result_intervals = list(map(lambda x:
                                    set(cu.get_notes_from_fingering(
                                        STANDARD, note, x)), results))
        result_set = set(map(frozenset, result_intervals))
        self.assertTrue(all(map(lambda x: intervals == x, result_intervals)))

    def test_span(self):
        self.span_helper(3)
        self.span_helper(2)

    def span_helper(self, span):
        cable = Cable(STANDARD, span)
        results = cable.generate(Note.E, quality=Quality.MAJ)
        results = map(lambda x: filter(bool, x), results)
        min_maxes = map(min_max, results)
        abs_diffs = map(lambda x: abs(x[0] - x[1]), min_maxes)
        self.assertTrue(all(map(lambda x: x <= span, abs_diffs)))

    def test_E_13(self):
        cable = Cable(STANDARD, 3)
        results = cable.generate(Note.E,
                                 extension=Extension.E13)
        results = list(results)
        self.assertTrue(len(results))


if __name__ == '__main__':
    unittest.main()
