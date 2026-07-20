import soundfile as sf
import sounddevice as sd

#PROCESSING CLASSES
from processing.softclipping import SoftClipping, CubeWave
from processing.bitcrushing import BitCrushing, BitDepthReduction
from processing.downsampling import DownSampler, ZeroAndHold
from processing.wowflutter import WowAndFlutter, LFO

from visual.sound import plot_audio

def main():
    print("Hello from pyth!")
    audio_path = "audio/chillshite.wav"
    data, samplerate = sf.read(audio_path)
    print(data)

    p_softclipping = SoftClipping(CubeWave())
    p_bitcrushing = BitCrushing(BitDepthReduction())
    p_downsample = DownSampler(ZeroAndHold())
    p_wowflutter = WowAndFlutter(LFO())
    new_audio = p_wowflutter.process(data, samplerate)
    new_audio = p_softclipping.process(new_audio)
    new_audio = p_bitcrushing.process(new_audio)
    new_audio = p_downsample.process(new_audio)
    
    plot_audio(new_audio, samplerate)

    # input("press to move on foo")

    sd.play(new_audio, samplerate)

    input("press to shut this foo up")

    sd.stop()

#https://python-sounddevice.readthedocs.io/en/0.5.3/examples.html#play-a-sound-file
def play_audio(data, chnuksize):
    pass

if __name__ == "__main__":
    main()