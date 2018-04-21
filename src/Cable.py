'''Chord generator library'''
import chordUtil as cu
import util


def generate(chord, quality=None, extended=None, *add):
    """
    generate('A', quality=Quality.MAJ, extended=Extended.E7, Add.b13)
    Params:
        chord: str - name of chord to generate plus any sharp/flats. Capital vs
            lowercase indicates major vs minor unless quality is specified
        quality: Quality - overall quality of chord to generate without
            extensions
        extended: Extended - specifies which extended chord to generate
        *add: collection(Add) - notes to add. No quality/extended specified
            will generate chords with the root and these additions, with no
            other notes
    """
    pass
