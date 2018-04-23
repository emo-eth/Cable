import unittest
import sys
sys.path.append('../src')
from VoiceLeader import Cable, Chord, lead
from constants import Note


class VoiceLeaderTest(unittest.TestCase):

    def test_works(self):
        cable = Cable()
        chord1 = Chord(Note.E)
        chord2 = Chord(Note.B)
        lead(cable, chord1, chord2)
