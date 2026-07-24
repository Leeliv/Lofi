import matplotlib.pyplot as plt
import numpy as np

def plot_audio(audio, samplerate):
    # time = np.arrange(len(audio)) / samplerate
    time = np.linspace(0,len(audio)/samplerate, num=len(audio))

    plt.figure(1)
    plt.title("Sound wave")
    plt.xlabel("Time")
    plt.plot(time, audio)
    plt.show()
    # input("WAIT LEMMI TELL YOU SUMTHINNNN")