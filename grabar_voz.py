
"""
Para ejecutar éste código usar:

manim -pqh grabar_voz.py --disable_caching

"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
import warnings
warnings.filterwarnings("ignore")
config.media_width = "100%"
config.verbosity = "WARNING"

class Inicio(VoiceoverScene):
    def construct(self):
       
        self.set_speech_service(RecorderService())

        circle = Circle()
        square=Square()
       
        with self.voiceover(text="Éste es un ejemplo") as tracker:
            self.play(Create(square), run_time=tracker.duration)
       
        with self.voiceover(text="De cómo grabar tu voiceover") as tracker:
            self.play(Create(circle), run_time=tracker.duration)
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)
# test=Inicio()
# test.render()
