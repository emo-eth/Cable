'''Chord generator library'''
import chordUtils as cu
import util
from itertools import chain
from constants import Interval, Note
from collections import Counter


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
        intervals = cu.get_intervals(root, quality, extended, *add)
        # notes = map(lambda interval: root + interval,
        #             intervals)
        # print(list(notes))
        yield from self.generate_chords(root, intervals, self.tuning)

    def generate_chords(self, root, intervals, strings, placed=set(),
                        fingering=[]):
        """Helper generator to yield results after updating placed intervals
        and fingering.

        Arguments:
            root {Note} -- root note
            intervals {set(Interval)} -- set of intervals in chord
            strings {list(Note)} -- remaining open strings
            placed {set(Interval)} -- Intervals present in fingering thus far
            fingering {list(int|Note.X)} -- fingering of constructed chord
                thus far
        """
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
        if self.invalid_fingering(filtered_fingering, frets):
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
            # curry args with a function call we can unpack for less verbosity
            def args(): return (root, intervals, strings[1:], placed.copy(),
                                fingering.copy(), interval)
            if fingers:
                if interval in span_below:
                    yield from self._generate_helper(*args(),
                                                     (lambda: min_fret +
                                                      span_below[interval]))
                if interval in span_above:
                    yield from self._generate_helper(*args(),
                                                     (lambda: max_fret +
                                                      span_above[interval]))
                if interval in span_between:
                    yield from self._generate_helper(*args(),
                                                     (lambda: min_fret +
                                                      span_between[interval]))
            else:
                # if no fingers have been placed, pick any fret
                string_interval = cu.get_relative_interval(root, strings[0],
                                                           interval)
                yield from self._generate_helper(*args(),
                                                 lambda: string_interval.value)
            # open string
            if interval == root.interval_to(strings[0]):
                yield from self._generate_helper(*args(), lambda: 0)
            # dead string
            # TODO: add rules for dead strings (no big gaps, etc, or score them
            # low)
            yield from self._generate_helper(*(args()[:-1]),
                                             None, lambda: Note.X)

    def _generate_helper(self, root, intervals, strings, placed, fingering,
                         interval, fret_func):
        """Helper generator to yield results after updating placed intervals
        and fingering.

        Arguments:
            root {Note} -- root note
            intervals {set(Interval)} -- set of intervals in chord
            strings {list(Note)} -- remaining open strings
            placed {set(Interval)} -- Intervals present in fingering thus far
            fingering {list(int|Note.X)} -- fingering of constructed chord
                thus far
            interval {Interval|None} -- interval relative to root that we are
                adding to the fingering
            fret_func {func -> int|Note.X} -- possibly curried function to
                calculate the fret on this string for this fingering
        """

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
        # TODO: make smart about preferred notes
        return len(strings) < (len(intervals) - len(placed))
    
    @staticmethod
    def invalid_fingering(filtered_fingering, frets):
        if not filtered_fingering:
            return False
        # if requires more than 4 fingers, can't finger
        if len(frets) > 4:
            return True
        counts = Counter(filtered_fingering)
        lowest = min(counts.keys())
        # if more than 3 fingered notes above barred, invalid
        if len(filtered_fingering) - lowest > 3:
            return True
        return False
