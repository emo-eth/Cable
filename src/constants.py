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
    
    def __repr__(self):
        if self == Note.X:
            return 'x'
        return super().__repr__()


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
    MAJ = auto()
    MIN = auto()
    HALF_DIM = auto()
    DIM = auto()  # implies a bb7
    AUG = auto()
    DOM = auto()  # implies a b7
    SUS2 = auto()
    SUS4 = auto()
    SUSb2 = auto()
    SUSs2 = auto()
    SUSb4 = auto()
    SUSs4 = auto()
    MIN_MAJ = auto()


class Extension(Enum):
    '''
    Enum of common extensions
    '''
    E7 = auto()
    E9 = auto()
    E11 = auto()
    E13 = auto()
    Eb9 = auto()
    Es9 = auto()
    Eb11 = auto()
    Es11 = auto()
    Eb13 = auto()
    Es13 = auto()

# TODO: octaves?
# eg maybe a 9th should always be +1 oct, bass notes on instruments like 
# banjo and ukulele
STANDARD = (Note.E, Note.A, Note.D, Note.G, Note.B, Note.E)
