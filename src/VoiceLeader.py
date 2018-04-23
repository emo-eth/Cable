from Cable import Cable, Chord


def lead(cable, *chords):
    chord_fingerings = list(map(list, map(cable.generate, chords)))
    print(len(chord_fingerings))
