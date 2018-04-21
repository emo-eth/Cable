from enum import Enum
from functools import reduce

# dead note
X = 'x'


class Note(Enum):
    Cb = 11
    C = 0
    Cs = 1
    Db = 1
    D = 2
    Ds = 3
    Eb = 3
    E = 4
    Es = 5
    Fb = 4
    F = 5
    Fs = 6
    Gb = 6
    G = 7
    Gs = 8
    Ab = 8
    A = 9
    As = 10
    Bb = 10
    B = 11
    Bs = 0

    def __add__(self, interval):
        return Note((self.value + interval.value) % 12)

    def __radd__(self, interval):
        return self.__add__(interval)



# TODO: octaves?
# maybe not, "bass" is just first string with note played
STANDARD = (Note.E, Note.A, Note.D, Note.G, Note.B, Note.E)


class Interval(Enum):
    '''Interval constants for constructing chord from Qualities'''
    ROOT = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    AUGMENTED_SECOND = 3
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    AUGMENTED_THIRD = 5
    DIMINISHED_FOURTH = 4
    PERFECT_FOURTH = 5
    AUGMENTED_FOURTH = 6
    DIMINISHED_FIFTH = 6
    PERFECT_FIFTH = 7
    AUGMENTED_FIFTH = 8
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    AUGMENTED_SIXTH = 10
    DIMINISHED_SEVENTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    FLAT_NINTH = 1
    NINTH = 2
    SHARP_NINTH = 3
    FLAT_ELEVENTH = 4
    ELEVENTH = 5
    SHARP_ELEVENTH = 6
    FLAT_THIRTEENTH = 8
    THIRTEENTH = 10
    SHARP_THIRTEENTH = 11


class Add(Enum):
    '''
    Enum of common added notes
    TODO: Probably can just add these names to Interval
    '''
    b5 = 0
    s5 = 1
    a9 = 2
    b9 = 3
    s9 = 4
    a11 = 5
    b11 = 6
    s11 = 7
    a13 = 8
    b13 = 9
    s13 = 10
    m3 = 11
    M3 = 12
    m7 = 13
    M7 = 14
    b2 = 15
    a2 = 16
    s2 = 17
    b6 = 18
    a6 = 19
    s6 = 20
    b4 = 21
    a4 = 22
    s4 = 23
    a5 = 24
    s3 = 25
    d7 = 26


def map_dict(value, keys):
    out = dict()
    for key in keys:
        out[key] = value
    return out


def stargs(f):
    def helper(args):
        return f(*args)
    return helper


NINTHS = frozenset((Interval.MINOR_SECOND, Interval.MAJOR_SECOND,
                    Interval.AUGMENTED_SECOND, Interval.NINTH,
                    Interval.FLAT_NINTH, Interval.SHARP_NINTH,
                    Add.b9, Add.a9, Add.s9))
THIRDS = frozenset((Interval.MINOR_THIRD, Interval.MAJOR_THIRD,
                    Interval.AUGMENTED_THIRD, Add.m3, Add.M3, Add.s3))
ELEVENTHS = frozenset((Interval.DIMINISHED_FOURTH, Interval.PERFECT_FOURTH,
                       Interval.AUGMENTED_FOURTH, Interval.FLAT_ELEVENTH,
                       Interval.ELEVENTH, Interval.SHARP_ELEVENTH, Add.b4,
                       Add.a4, Add.s4, Add.b11, Add.a11, Add.s11))
FIFTHS = frozenset((Interval.DIMINISHED_FIFTH, Interval.PERFECT_FIFTH,
                    Interval.AUGMENTED_FIFTH, Add.b5, Add.a5, Add.s5))
THIRTEENTHS = frozenset((Interval.MINOR_SIXTH, Interval.MAJOR_SIXTH,
                         Interval.AUGMENTED_SIXTH, Interval.THIRTEENTH,
                         Interval.FLAT_THIRTEENTH, Interval.SHARP_THIRTEENTH,
                         Add.a6, Add.b6, Add.s6, Add.b13, Add.a13, Add.s13))
SEVENTHS = frozenset((Interval.MAJOR_SEVENTH, Interval.MINOR_SEVENTH,
                      Interval.DIMINISHED_SEVENTH, Add.m7, Add.M7, Add.d7))


def merge_dicts(a, b):
    a.update(b)
    return a


class Degree(Enum):
    ROOT = -1
    SECOND = 0
    THIRD = 1
    FOURTH = 2
    FIFTH = 3
    SIXTH = 4
    SEVENTH = 5
    NINTH = 6
    ELEVENTH = 7
    THIRTEENTH = 8


DEGREE_MAP = reduce(lambda prev, curr: merge_dicts(prev, curr),
                    map(stargs(map_dict), ((Degree.NINTH, NINTHS),
                                           (Degree.THIRD, THIRDS),
                                           (Degree.ELEVENTH, ELEVENTHS),
                                           (Degree.FIFTH, FIFTHS),
                                           (Degree.THIRTEENTH, THIRTEENTHS),
                                           (Degree.SEVENTH, SEVENTHS),
                                           (Degree.ROOT, {Interval.ROOT}))),
                    dict())


class Quality(Enum):
    '''
    Enum of common chord qualities
    TODO: Support MAJb5 etc?
    '''
    MAJ = 1
    MIN = 2
    HALF_DIM = 3
    DIM = 4  # implies a bb7
    AUG = 5
    DOM = 6  # implies a b7
    SUS2 = 7
    SUS4 = 8
    SUSb2 = 9
    SUSs2 = 10
    SUSb4 = 11
    SUSs4 = 12
    MIN_MAJ = 13


QUALITIES = {
    '7': Quality.DOM,
    'ø': Quality.HALF_DIM,
    'o': Quality.DIM,
    'x': Quality.AUG
}


class Extended(Enum):
    '''
    Enum of common extensions
    # TODO: b13 extension?
    '''
    E7 = 0
    E9 = 1
    E11 = 2
    E13 = 3
    Eb9 = 4
    Es9 = 5
    Eb11 = 6
    Es11 = 7
    Eb13 = 8
    Es13 = 9
    # TODO: b13, s13, etc


EXTENDED = {
    '7': Extended.E7,
    '9': Extended.E9,
    '11': Extended.E11,
    '13': Extended.E13
}


ADD =   {
    'b5': Add.b5,
    '#5': Add.s5,
    # etc
}
