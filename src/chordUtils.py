from constants import Quality, Interval, Extended, Degree, DEGREE_MAP


def is_major(chord_name):
    '''Guesses a chord is major or minor by its capitalization'''
    return chord_name[0].isupper()


def to_chroma(pitch):
    '''Convert a numeric pitch in any octave to a chroma between 0-12'''
    return pitch % 12


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


def get_intervals(bass, root, quality, extended, *add):
    notes = []
    if bass:
        notes = [bass]
    intervals = get_quality_intervals(quality)
    extended_intervals = get_extended_intervals(quality, extended)
    return bag_intervals(intervals, extended_intervals, add)


def bag_intervals(quality, extended, add):
    '''Return a dict of degrees to intervals
    Ensures that extended notes override quality notes, and that added notes
    override both.
    '''
    intervals = {}
    for interval in quality:
        intervals[DEGREE_MAP[interval]] = interval
    for interval in extended:
        intervals[DEGREE_MAP[interval]] = interval
    for interval in add:
        intervals[DEGREE_MAP[interval]] = interval
    return intervals.values()


def get_quality_intervals(quality):
    return QUALITY_NOTE_MAP[quality]


QUALITY_NOTE_MAP = {
    Quality.HALF_DIM: [Interval.ROOT, Interval.MINOR_THIRD,
                       Interval.DIMINISHED_FIFTH],
    Quality.MIN: [Interval.ROOT, Interval.MINOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.MAJ: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.SUS2: [Interval.ROOT, Interval.MAJOR_SECOND,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb2: [Interval.ROOT, Interval.MINOR_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs2: [Interval.ROOT, Interval.AUGMENTED_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUS4: [Interval.ROOT, Interval.PERFECT_FOURTH,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb4: [Interval.ROOT, Interval.DIMINISHED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs4: [Interval.ROOT, Interval.AUGMENTED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.AUG: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.AUGMENTED_FIFTH],
    Quality.DIM: [Interval.ROOT, Interval.MINOR_THIRD,
                  Interval.DIMINISHED_FIFTH, Interval.DIMINISHED_SEVENTH],
    Quality.DOM: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH, Interval.MINOR_SEVENTH],
    Quality.MIN_MAJ: [Interval.ROOT, Interval.MINOR_THIRD,
                      Interval.PERFECT_FIFTH, Interval.MAJOR_SEVENTH]
}


def get_extended_intervals(quality, extended):
    '''Get the extended notes included in a chord extension'''
    if extended is None or (extended == Extended.E7 and
                            (quality == Quality.DIM or
                             quality == Quality.DOM)):
        return []
    if quality in (Quality.MAJ, Quality.MIN_MAJ) or (quality == Quality.MAJ and
                                                     extended == Extended.E7):
        notes = [Interval.MAJOR_SEVENTH]
    else:
        notes = [Interval.MINOR_SEVENTH]
    extended_notes = EXTENDED_NOTE_MAP[extended] if extended else []
    return notes + extended_notes


# TODO: Define priorities
EXTENDED_NOTE_MAP = {
    Extended.Eb9: [Interval.MINOR_SECOND],
    Extended.E9: [Interval.MAJOR_SECOND],
    Extended.Es9: [Interval.AUGMENTED_SECOND],
    Extended.Eb11: [Interval.MAJOR_SECOND, Interval.DIMINISHED_FOURTH],
    Extended.E11: [Interval.MAJOR_SECOND, Interval.PERFECT_FOURTH],
    Extended.Es11: [Interval.MAJOR_SECOND, Interval.AUGMENTED_FOURTH],
    Extended.Eb13: [Interval.MAJOR_SECOND, Interval.PERFECT_FOURTH,
                    Interval.MINOR_SIXTH],
    Extended.E13: [Interval.MAJOR_SECOND,
                   Interval.PERFECT_FOURTH, Interval.MAJOR_SIXTH],
    Extended.Es13: [Interval.MAJOR_SECOND,
                    Interval.PERFECT_FOURTH, Interval.AUGMENTED_SIXTH]

}


def get_inverted_root(root, inversion):
    pass
