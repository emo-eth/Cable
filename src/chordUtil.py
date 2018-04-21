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
