import soundfile as sf
import sounddevice as sd
from processing.softclipping import SoftClipping, CubeWave

def main():
    print("Hello from pyth!")
    audio_path = "audio/chillshite.wav"
    data, samplerate = sf.read(audio_path)
    print(data.shape)

    p_softclipping = SoftClipping(CubeWave())
    new_audio = p_softclipping.process(data)

    sd.play(new_audio, samplerate)

    input("press to shut this foo up")

    sd.stop()

#https://python-sounddevice.readthedocs.io/en/0.5.3/examples.html#play-a-sound-file
def play_audio(data, chnuksize):
    pass

if __name__ == "__main__":
    main()