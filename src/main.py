#AUDIO INPUT/OUTPUT
import soundfile as sf
import sounddevice as sd

#DS
from queue import Queue

#THREADING
import threading

#PROCESSING CLASSES
from processing.softclipping import SoftClipping, CubeWave
from processing.bitcrushing import BitCrushing, BitDepthReduction
from processing.downsampling import DownSampler, ZeroAndHold
from processing.wowflutter import WowAndFlutter, LFO
from processing.delay import Delay, SimpleDelayBuffer
from processing.lowpassfilter import LpwPassFilter, lpf

#AUDIO ENGINES
from audio_engine.audio_engine import AudioEngine
from audio_interface.pedal import PedalBoard

#CLI
from cli.cli import CLI

#VISUAL PLOTTING
from visual.sound import plot_audio

def main():
    print("Hello from pyth!")
    audio_path = "audio/chillshite.wav"
    data, sample_rate = sf.read(audio_path)

    command_queue = Queue(maxsize = 5)
    cli = CLI(command_queue)
    
    cli_thread = threading.Thread(target= cli.run)
    

    print("CONTINUE")
    pedal = PedalBoard()
    # pedal.add_effect(SoftClipping(1, CubeWave()))
    # pedal.add_effect(DownSampler(2, ZeroAndHold()))
    # pedal.add_effect(WowAndFlutter(sample_rate, LFO()))
    # pedal.add_effect(BitCrushing(6, BitDepthReduction()))
    # pedal.add_effect(Delay(SimpleDelayBuffer()))
    # pedal.add_effect(LpwPassFilter(0.5, lpf()))

    

    # pedal.set_effect_perameter(0, drive=4)
    # pedal.set_effect_perameter(1, reduction = 2)
    # pedal.set_effect_perameter(2, wow_depth=4, wow_rate=40)
    # pedal.set_effect_perameter(3, bit_depth=10)

    # pedal.bypass_effect(2)
    

    cli_thread.start()
    engine = AudioEngine(sample_rate, pedal, command_queue)
    engine.play(data, sample_rate)
    
    
    # plot_audio(new_audio, sample_rate)

    # input("press to move on foo")

    # sd.play(data, sample_rate)

    # input("press to shut this foo up")

    # sd.stop()

#https://python-sounddevice.readthedocs.io/en/0.5.3/examples.html#play-a-sound-file
def play_audio(data, chnuksize):
    pass

if __name__ == "__main__":
    main()