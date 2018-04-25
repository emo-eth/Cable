'''Chord generator library'''
from chordUtils import Chord, get_intervals
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
        generate('A', Interval.b13, quality=Quality.MAJ, extended=Extended.E7)
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
        if isinstance(root, Chord):
            add = root.add
            bass = root.bass
            quality = root.quality
            extension = root.extension
            root = root.root
        # default to MAJ if nothing specified
        if quality is None and extension is None and len(add) == 0:
            quality = Quality.MAJ
        intervals = set(get_intervals(root, quality, extension, *add))
        if bass:
            intervals.add(root.interval_to(bass))
        yield from self.generate_chords(root, bass, intervals, self.tuning)

    def generate_chords(self, root, bass, intervals, strings, placed=set(),
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
        # strings with frets (not open or dead)
        filtered_fingering = list(filter(bool, fingering))
        # any notes placed, for deciding to force bass
        # frets in fingering
        frets = set(filtered_fingering)
        # minimum number of fingers needed to fret above notes
        fingers = len(frets)
        # throw out chords that are impossible to finger
        if self.invalid_fingering(filtered_fingering, frets):
            return
        # base case
        if len(strings) == 0:
            yield fingering
            return
        # lowest/highest: current lowest/highest
        # min/max: lowest/highest allowed frets
        lowest_fret = highest_fret = min_fret = max_fret = 0
        # if there are fretted notes, determine the available fret span
        if frets:
            lowest_fret, highest_fret = util.min_max(frets)
            remaining_span = self.span - (highest_fret - lowest_fret)
            min_fret = lowest_fret - remaining_span
            max_fret = highest_fret + remaining_span
            if min_fret < 0:
                min_fret = 0
        # interval to lowest fret
        min_fret_interval = Interval(min_fret)
        # lowest possible note to fret on this string
        min_fretted_note = strings[0] + min_fret_interval

        # curry args with a function call we can unpack for less verbosity
        def args(): return (root, bass, intervals, strings[1:], placed.copy(),
                            fingering.copy())
        # force bass note on this string if no other notes placed
        if not placed and bass:
            bass_interval = strings[0].interval_to(bass) if bass else None
            yield from self._generate_helper(*args(), bass_interval,
                                             lambda: bass_interval.value)
        else:  # otherwise iterate over intervals
            for interval in intervals:
                # get interval to fret this note on this string
                fret_interval = min_fretted_note.interval_to(root + interval)
                if (not fingers or  # if no fingers have been placed, pick any fret
                    # otherwise pick any fret between min/max
                    (min_fret <=
                     min_fret + fret_interval.value <=
                     max_fret)):
                    yield from self._generate_helper(*args(), interval, lambda: min_fret +
                                                     fret_interval.value)
        # dead note, skip string
        # TODO: limit number of skipped strings
        yield from self._generate_helper(*args(),
                                         None, lambda: Note.X)

    def _generate_helper(self, root, bass, intervals, strings, placed, fingering,
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
        # don't add bass to placed (TODO: why)
        if interval:
            placed.add(interval)
        fingering = fingering + [fret_func()]
        yield from self.generate_chords(root, bass, intervals, strings, placed,
                                        fingering)

    @staticmethod
    def unable_to_voice(strings, intervals, placed):
        # TODO: make smart about preferred notes
        return len(strings) < (len(intervals) - len(placed))

    def invalid_fingering(self, filtered_fingering, frets):
        # nothing fretted, not invalid
        if not filtered_fingering:
            return False
        # if requires more than x fingers, can't finger
        if len(frets) > self.fingers:
            return True
        counts = Counter(filtered_fingering)
        lowest = min(filtered_fingering)
        lowest_count = counts[lowest]
        # if more than (x-1) fingered notes above barred, invalid
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
