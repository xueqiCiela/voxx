from __future__ import division, print_function
# pset4.py

import sys
sys.path.append('..')
from common.core import *
from common.audio import *
from common.synth import *
from common.gfxutil import *
from common.clock import *
from common.metro import *
from common.noteseq import *
import math

guitar1 = [[240,0],[480,65],[480,65],[240,57],[240,60],[240,57],[240,0],[480,55],[240,60],[240,59],[720,55],[240,0],[480,64],[480,64],[240,55],[240,59],[240,55],[240,0],[480,60],[480,62],[240,64],[240,60],[240,55]]
guitar2 = [[240,0],[480,60],[720,60],[480,0],[240,0],[480,62],[720,62],[480,0],[240,0],[480,59],[720,59],[480,0],[240,0],[480,64],[720,60],[480,0]]
guitar3 = [[240,0],[480,57],[720,57],[480,0],[240,0],[480,59],[720,59],[480,0],[240,0],[480,55],[720,55],[480,0],[240,0],[480,60],[720,59],[480,0]]

# Part 2, 3, and 4
class MainWidget2(BaseWidget) :
    def __init__(self):
        super(MainWidget2, self).__init__()

        self.audio = Audio(2)
        self.synth = Synth('FluidR3_GM.sf2')

        # create TempoMap, AudioScheduler
        self.tempo_map  = SimpleTempoMap(120)
        self.sched = AudioScheduler(self.tempo_map)

        # connect scheduler into audio system
        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)

        # animations
        self.objects = AnimGroup()
        self.canvas.add(self.objects)

        for line in [guitar1, guitar2, guitar3]:
            seq = NoteSequencer(self.sched, self.synth, 1, (0,0), line)
            seq.start()

    def on_update(self):
        self.audio.on_update()

run(MainWidget2)
