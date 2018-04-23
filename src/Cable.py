'''Chord generator library'''
import chordUtils as cu
import util
from itertools import chain
from constants import Quality, Interval, Note, STANDARD
from collections import Counter


class Cable(object):

    def __init__(self, tuning=STANDARD, span=3, fingers=4):
        self.tuning = tuning
        self.span = span
        self.fingers = fingers

    def generate(self, root, *add, bass=None, quality=None, extension=None):
        """
        generate('A', quality=Quality.MAJ, extended=Extended.E7, Add.b13)
        Params:
            root: str - name of root to generate plus any sharp/flats. Capital
                vs lowercase indicates major vs minor unless quality is
                specified
            bass: Note
            quality: Quality - overall quality of root to generate without
                extensions
            extended: Extended - specifies which extended root to generate
            *add: collection(Add) - notes to add. No quality/extended specified
                will generate roots with the root and these additions, with no
                other notes
        """
        if quality is None and extension is None and len(add) == 0:
            quality = Quality.MAJ
        intervals = set(cu.get_intervals(root, quality, extension, *add))
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
        filtered_fingering = list(filter(bool, fingering))
        frets = set(filtered_fingering)
        fingers = len(frets)
        if self.invalid_fingering(filtered_fingering, frets):
            return
        # base case
        if len(strings) == 0:
            yield fingering
            return
        lowest_fret = highest_fret = min_fret = max_fret = 0
        if frets:
            lowest_fret, highest_fret = util.min_max(frets)
            remaining_span = self.span - (highest_fret - lowest_fret)
            min_fret = lowest_fret - remaining_span
            max_fret = highest_fret + remaining_span
            if min_fret < 0:
                min_fret = 0
        min_fret_interval = Interval(min_fret)
        min_fretted_note = strings[0] + min_fret_interval
        for interval in intervals:
            fret_interval = min_fretted_note.interval_to(root + interval)
            # curry args with a function call we can unpack for less verbosity

            def args(): return (root, intervals, strings[1:], placed.copy(),
                                fingering.copy(), interval)
            if (not fingers or  # if no fingers have been placed, pick any fret
                # otherwise pick any fret between min/max
                (min_fret <=
                 min_fret + fret_interval.value <=
                 max_fret)):
                yield from self._generate_helper(*args(), lambda: min_fret +
                                                 fret_interval.value)
        # dead note, skip string
        # TODO: limit number of skipped strings
        yield from self._generate_helper(*args()[:-1],
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
    def unable_to_voice(strings, intervals, placed):
        # TODO: make smart about preferred notes
        return len(strings) < (len(intervals) - len(placed))

    def invalid_fingering(self, filtered_fingering, frets):
        if not filtered_fingering:
            return False
        # if requires more than 4 fingers, can't finger
        if len(frets) > self.fingers:
            return True
        counts = Counter(filtered_fingering)
        lowest = min(filtered_fingering)
        lowest_count = counts[lowest]
        # if more than 3 fingered notes above barred, invalid
        if len(filtered_fingering) - lowest_count > (self.fingers - 1):
            return True
        return False

    @staticmethod
    def can_skip_strings(fingering, intervals):
        return True
        counts = Counter(fingering)
        if counts.get(Note.X, 0) >= 3 and len(intervals) > 2:
            return False
        return True
        # allow leading and trailing dead notes
        # don't allow interspersed dead notes
        # don't allow X in between dead notes
        last_dead = False
        for fret in fingering:
            if fret == Note.X:
                if not last_dead and (dead_count and fret_count):
                    return False
                # don't count leading dead notes
                if frets:
                    dead_count += 1

                if frets:
                    last_dead = True
                # allow tailing dead notes

            else:
                fret_count += 1
                last_dead = False

        dead_cont = 0
        fret_count = 0
        pass
