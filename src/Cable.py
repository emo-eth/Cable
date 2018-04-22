'''Chord generator library'''
import chordUtils as cu
import util
from itertools import chain
from constants import Interval, Note


class Cable(object):

    def __init__(self, tuning, span=3):
        self.tuning = tuning
        self.span = span

    def generate(self, root, *add, bass=None, quality=None, extended=None):
        """
        generate('A', quality=Quality.MAJ, extended=Extended.E7, Add.b13)
        Params:
            root: str - name of root to generate plus any sharp/flats. Capital
                vs lowercase indicates major vs minor unless quality is
                specified TODO: nah lol
            bass: Note
            quality: Quality - overall quality of root to generate without
                extensions
            extended: Extended - specifies which extended root to generate
            *add: collection(Add) - notes to add. No quality/extended specified
                will generate roots with the root and these additions, with no
                other notes
                TODO: add should also alter
        """
        intervals = cu.get_intervals(bass, root, quality, extended, *add)
        # notes = map(lambda interval: root + interval,
        #             intervals)
        # print(list(notes))
        yield from self.generate_chords(root, intervals, self.tuning)

    def generate_chords(self, root, intervals, strings, placed=set(),
                        fingering=[]):
        # make sure we can make the whole chord
        # TODO: decide optional notes for large voicings
        if self.unable_to_voice(strings, intervals, placed):
            return
        # base case
        if len(strings) == 0:
            yield fingering
            return
        filtered_fingering = list(filter(bool, fingering))
        frets = set(filtered_fingering)
        fingers = len(frets)
        if fingers > 4:
            return
        min_fret = max_fret = 0
        if frets:
            min_fret, max_fret = util.min_max(frets)
        remaining_span = self.span - (max_fret - min_fret)

        # allowable frets
        if fingers:
            span_below = {self.calculate_interval(root, strings[0], min_fret, x):
                          x for x in range(-remaining_span, 0)
                          if (x + min_fret) > 0}
            span_above = {self.calculate_interval(root, strings[0], max_fret, x):
                          x for x in range(1, remaining_span + 1)}
            span_between = {self.calculate_interval(root, strings[0], min_fret, x):
                            x for x in range(((max_fret - min_fret) + 1))}
        else:
            span_below = span_above = span_between = {}

        # TODO: assert >3 notes on same fret be lowest fret
        for interval in intervals:
            # TODO: dead notes
            if fingers:
                # TODO: handle previous frets and voicings around 12
                if interval in span_below:
                    yield from self._generate_helper(root, intervals, strings[1:],
                                                     placed.copy(), fingering.copy(),
                                                     interval,
                                                     (lambda: min_fret +
                                                      span_below[interval]))
                if interval in span_above:
                    yield from self._generate_helper(root, intervals, strings[1:],
                                                     placed.copy(), fingering.copy(),
                                                     interval,
                                                     (lambda: max_fret +
                                                      span_above[interval]))
                if interval in span_between:
                    yield from self._generate_helper(root, intervals, strings[1:],
                                                     placed.copy(), fingering.copy(),
                                                     interval,
                                                     (lambda: min_fret +
                                                      span_between[interval]))
            else:
                # if no fingers have been placed, pick any fret
                string_interval = cu.get_relative_interval(root, strings[0],
                                                           interval)
                yield from self._generate_helper(root, intervals, strings[1:],
                                                 placed.copy(), fingering.copy(),
                                                 interval,
                                                 lambda: string_interval.value)
            # open string
            if interval == root.interval_to(strings[0]):
                yield from self._generate_helper(root, intervals, strings[1:],
                                                 placed.copy(), fingering.copy(),
                                                 interval, lambda: 0)
            # dead string
            yield from self._generate_helper(root, intervals, strings[1:],
                                             placed.copy(), fingering.copy(),
                                             None, lambda: Note.X)

    def _generate_helper(self, root, intervals, strings, placed, fingering, interval,
                         fret_func):
        if interval:
            placed.add(interval)
        fingering = fingering + [fret_func()]
        yield from self.generate_chords(root, intervals, strings, placed,
                                        fingering)

    @staticmethod
    def calculate_interval(root, open_string, relative_fret, semitones):
        return root.interval_to(open_string +
                                Interval(relative_fret % 12) +
                                Interval(semitones % 12))

    @staticmethod
    def unable_to_voice(strings, intervals, placed):
        return len(strings) < (len(intervals) - len(placed))
