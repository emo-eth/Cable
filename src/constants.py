from enum import Enum, auto
from functools import reduce
from util import stargs, map_dict, merge_dicts

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
    X = float('-inf')

    def __add__(self, interval):
        if not isinstance(interval, Interval):
            raise TypeError("Can only add intervals to notes")
        if self == Note.X:
            raise TypeError("Dead note is not a note")
        return Note((self.value + interval.value) % 12)

    def __radd__(self, interval):
        return self.__add__(interval)

    def __bool__(self):
        return self != Note.X

    def interval_to(self, note):
        if note == Note.X:
            raise TypeError("Dead note is not a note")
        return Interval((note.value - self.value) % 12)


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
    b2 = 1
    m2 = 1
    a2 = 2
    M2 = 2
    s2 = 3
    m3 = 3
    M3 = 4
    s3 = 4
    b4 = 4
    a4 = 5
    s4 = 6
    b5 = 6
    a5 = 7
    s5 = 8
    m6 = 8
    M6 = 9
    s6 = 10
    d7 = 9
    m7 = 10
    M7 = 11
    b9 = 1
    a9 = 2
    s9 = 3
    b11 = 4
    a11 = 5
    s11 = 6
    b13 = 8
    a13 = 9
    s13 = 10

    def __add__(self, interval):
        return Interval((self.value + interval.value) % 12)

    def __sub__(self, interval):
        return Interval((self.value - interval.value) % 12)

    def __gt__(self, interval):
        if not isinstance(interval, Interval):
            raise TypeError("Can only compare Intervals")
        return self.value > interval.value

    def __lt__(self, interval):
        if not isinstance(interval, Interval):
            raise TypeError("Can only compare Intervals")
        return self.value < interval.value


class Degree(Enum):
    ROOT = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()
    FIFTH = auto()
    SIXTH = auto()
    SEVENTH = auto()
    NINTH = auto()
    ELEVENTH = auto()
    THIRTEENTH = auto()


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


class Extension(Enum):
    '''
    Enum of common extensions
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


# TODO: aliases do fuck this up. use .name property?
NINTHS = frozenset((Interval.MINOR_SECOND, Interval.MAJOR_SECOND,
                    Interval.AUGMENTED_SECOND, Interval.NINTH,
                    Interval.FLAT_NINTH, Interval.SHARP_NINTH))
THIRDS = frozenset((Interval.MINOR_THIRD, Interval.MAJOR_THIRD,
                    Interval.AUGMENTED_THIRD))
ELEVENTHS = frozenset((Interval.DIMINISHED_FOURTH, Interval.PERFECT_FOURTH,
                       Interval.AUGMENTED_FOURTH, Interval.FLAT_ELEVENTH,
                       Interval.ELEVENTH, Interval.SHARP_ELEVENTH))
FIFTHS = frozenset((Interval.DIMINISHED_FIFTH, Interval.PERFECT_FIFTH,
                    Interval.AUGMENTED_FIFTH))
THIRTEENTHS = frozenset((Interval.MINOR_SIXTH, Interval.MAJOR_SIXTH,
                         Interval.AUGMENTED_SIXTH, Interval.THIRTEENTH,
                         Interval.FLAT_THIRTEENTH, Interval.SHARP_THIRTEENTH))
SEVENTHS = frozenset((Interval.MAJOR_SEVENTH, Interval.MINOR_SEVENTH,
                      Interval.DIMINISHED_SEVENTH))

# map degrees to intervals
DEGREE_MAP = reduce(lambda prev, curr: merge_dicts(prev, curr),
                    map(stargs(map_dict), ((Degree.NINTH, NINTHS),
                                           (Degree.THIRD, THIRDS),
                                           (Degree.ELEVENTH, ELEVENTHS),
                                           (Degree.FIFTH, FIFTHS),
                                           (Degree.THIRTEENTH, THIRTEENTHS),
                                           (Degree.SEVENTH, SEVENTHS),
                                           (Degree.ROOT, {Interval.ROOT}))),
                    dict())

# TODO: octaves?
# maybe not, "bass" is just first string with note played
# but maybe a 9th should always be +1 oct
STANDARD = (Note.E, Note.A, Note.D, Note.G, Note.B, Note.E)
