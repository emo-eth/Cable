from constants import Note, Quality, Interval, Extension, Degree
from itertools import chain


class Chord(object):
    '''Container class for chord information'''

    def __init__(self, root, *add, bass=None, quality=None, extension=None):
        self.root = root
        self.add = add
        self.bass = bass
        self.quality = quality
        self.extension = extension


def sharp_flat_delta(note_name):
    if note_name.endswith('b'):
        return -1
    elif note_name.endswith('#'):
        return 1
    elif note_name.endswith('bb'):
        return -2
    elif note_name.endswith('x'):
        return 2
    return 0


def get_intervals(root, quality, extension, *add):
    intervals = get_quality_intervals(quality, extension)
    extension_intervals = get_extension_intervals(quality, extension)
    return intervals + extension_intervals + list(add)


def get_quality_intervals(quality, extension):
    if extension is None and quality is None:
        return dict()
    elif quality is None:
        return QUALITY_NOTE_MAP[Quality.MAJ].copy()
    return QUALITY_NOTE_MAP[quality].copy()


def get_extension_intervals(quality, extension):
    '''Get the extension notes included in a chord extension'''
    if extension is None or (extension == Extension.E7 and
                             quality in {Quality.DIM, Quality.DOM,
                                         Quality.MIN_MAJ}):
        return list()
    if extension == Extension.E7:
        if quality in (Quality.MIN, Quality.HALF_DIM):
            return [Interval.MINOR_SEVENTH]
        elif (quality == Quality.MAJ):
            return [Interval.MAJOR_SEVENTH]
    elif quality in (Quality.MAJ, Quality.MIN_MAJ):
        notes = [Interval.MAJOR_SEVENTH]
    else:
        notes = [Interval.MINOR_SEVENTH]
    extension_notes = EXTENSION_NOTE_MAP[extension]
    return notes + extension_notes


def score_difficulty(fingering):
    # TODO: account for barre chords
    return len(set(filter(bool, fingering)))


def get_intervals_from_fingering(tuning, root, fingering):
    filtered = filter(lambda x: x[1] != Note.X, zip(tuning, fingering))
    notes = map(lambda t: t[0] + Interval(t[1] % 12), filtered)
    return list(map(lambda note: root.interval_to(note), notes))


QUALITY_NOTE_MAP = {
    Quality.HALF_DIM: [Interval.ROOT,
                       Interval.MINOR_THIRD,
                       Interval.DIMINISHED_FIFTH],
    Quality.MIN: [Interval.ROOT,
                  Interval.MINOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.MAJ: [Interval.ROOT,
                  Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.SUS2: [Interval.ROOT,
                   Interval.MAJOR_SECOND,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb2: [Interval.ROOT,
                    Interval.MINOR_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs2: [Interval.ROOT,
                    Interval.AUGMENTED_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUS4: [Interval.ROOT,
                   Interval.PERFECT_FOURTH,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb4: [Interval.ROOT,
                    Interval.DIMINISHED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs4: [Interval.ROOT,
                    Interval.AUGMENTED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.AUG: [Interval.ROOT,
                  Interval.MAJOR_THIRD,
                  Interval.AUGMENTED_FIFTH],
    Quality.DIM: [Interval.ROOT,
                  Interval.MINOR_THIRD,
                  Interval.DIMINISHED_FIFTH,
                  Interval.DIMINISHED_SEVENTH],
    Quality.DOM: [Interval.ROOT,
                  Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH,
                  Interval.MINOR_SEVENTH],
    Quality.MIN_MAJ: [Interval.ROOT,
                      Interval.MINOR_THIRD,
                      Interval.PERFECT_FIFTH,
                      Interval.MAJOR_SEVENTH]
}
# TODO: Define priorities
EXTENSION_NOTE_MAP = {
    Extension.Eb9: [Interval.MINOR_SECOND],
    Extension.E9: [Interval.MAJOR_SECOND],
    Extension.Es9: [Interval.AUGMENTED_SECOND],
    Extension.Eb11: [Interval.MAJOR_SECOND,
                     Interval.DIMINISHED_FOURTH],
    Extension.E11: [Interval.MAJOR_SECOND,
                    Interval.PERFECT_FOURTH],
    Extension.Es11: [Interval.MAJOR_SECOND,
                     Interval.AUGMENTED_FOURTH],
    Extension.Eb13: [Interval.MAJOR_SECOND,
                     Interval.PERFECT_FOURTH,
                     Interval.MINOR_SIXTH],
    Extension.E13: [Interval.MAJOR_SECOND,
                    Interval.PERFECT_FOURTH,
                    Interval.MAJOR_SIXTH],
    Extension.Es13: [Interval.MAJOR_SECOND,
                     Interval.PERFECT_FOURTH,
                     Interval.AUGMENTED_SIXTH]
}


def get_inverted_root(root, inversion):
    pass
