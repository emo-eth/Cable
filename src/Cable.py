'''Chord generator library'''
import chordUtils as cu
import util


def generate(tuning, root, bass=None, quality=None, extended=None, *add):
    """
    generate('A', quality=Quality.MAJ, extended=Extended.E7, Add.b13)
    Params:
        root: str - name of root to generate plus any sharp/flats. Capital vs
            lowercase indicates major vs minor unless quality is specified
        bass: Note
        quality: Quality - overall quality of root to generate without
            extensions
        extended: Extended - specifies which extended root to generate
        *add: collection(Add) - notes to add. No quality/extended specified
            will generate roots with the root and these additions, with no
            other notes
            TODO: add should also alter
    """
    notes = cu.get_intervals(bass, root, quality, extended, *add)
