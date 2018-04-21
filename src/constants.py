from frozendict import frozendict
from enum import enum

# dead note
X = 'x'


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

QUALITIES = frozendict({
    '7': Quality.DOM,
    'ø', Quality.HALF_DIM,
    'o', Quality.DIM,
    'x', Quality.AUG
})


class Extended(Enum):
    '''
    Enum of common extensions
    #TODO: b13 extension?
    '''
    E7 = 0
    E9 = 1
    E11 = 2
    E13 = 3
    # TODO: b13, s13, etc

EXTENDED = frozendict({
    '7': Extended.E7,
    '9': Extended.E9,
    '11': Extended.E11,
    '13', Extended.E13
})


class Add(Enum):
    '''
    Enum of common added notes
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


ADD = frozendict({
    'b5': Add.b5,
    '#5': Add.s5,
    # etc
})
