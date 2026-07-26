import soundfile as sf
import sounddevice as sd

#PROCESSING CLASSES
from processing.softclipping import SoftClipping, CubeWave
from processing.bitcrushing import BitCrushing, BitDepthReduction
from processing.downsampling import DownSampler, ZeroAndHold
from processing.wowflutter import WowAndFlutter, LFO

from audio_engine.audio_engine import AudioEngine
from audio_interface.pedal import PedalBoard
from visual.sound import plot_audio

def main():
    print("Hello from pyth!")
    audio_path = "audio/chillshite.wav"
    data, sample_rate = sf.read(audio_path)
    print(data)

    # p_softclipping = SoftClipping(CubeWave())
    # p_bitcrushing = BitCrushing(BitDepthReduction())
    # p_downsample = DownSampler(ZeroAndHold())
    # p_wowflutter = WowAndFlutter(LFO())
    # new_audio = p_wowflutter.process(data, samplerate)
    # new_audio = p_softclipping.process(new_audio)
    # new_audio = p_bitcrushing.process(new_audio)
    # new_audio = p_downsample.process(new_audio)

    pedal = PedalBoard()
    pedal.add_effect(SoftClipping(CubeWave()))
    pedal.add_effect(BitCrushing(20, BitDepthReduction()))
    pedal.add_effect(DownSampler(4, ZeroAndHold()))
    pedal.add_effect(WowAndFlutter(sample_rate, LFO()))
    # new_audio = pedal.process(data)

    engine = AudioEngine(pedal)
    engine.play(data, sample_rate)
    
    
    # plot_audio(new_audio, sample_rate)

    # input("press to move on foo")

    # sd.play(new_audio, sample_rate)

    # input("press to shut this foo up")

    # sd.stop()

#https://python-sounddevice.readthedocs.io/en/0.5.3/examples.html#play-a-sound-file
def play_audio(data, chnuksize):
    pass

if __name__ == "__main__":
    main()