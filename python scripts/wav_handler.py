import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def load_song(filename, desired_len, hop_length = 128):
    duration = librosa.get_duration(filename=filename)
    sro = desired_len/duration
    y, sr = librosa.load(filename, sr = hop_length*sro)
    while y.shape[0]/hop_length > desired_len:
        y = y[:-1]
    return y, sr

def generate_spectogram(y, sr, hop_length = 128, spec_type = 'cqt', plot = False, plot_name = 'data_spectogram'):
    C = None
    n_fft = 512
    n_mels = 128
    y_axis = None
    if spec_type == 'cqt':
        C = np.abs(librosa.cqt(y, sr=sr,  hop_length=hop_length))
        C = librosa.amplitude_to_db(C, ref=np.max)
        y_axis = 'cqt_note'
    elif spec_type == 'mel':
        C = librosa.feature.melspectrogram(y, sr=sr, hop_length=hop_length)
        C = librosa.power_to_db(C, ref=np.max)
        y_axis='mel'
    elif spec_type == 'stft':
        C = np.abs(librosa.stft(y,  hop_length=hop_length, n_fft = n_fft))
        C = librosa.amplitude_to_db(C, ref=np.max)
        y_axis='linear'
    elif spec_type == 'lft':
        C = np.abs(librosa.stft(y,  hop_length=hop_length, n_fft = n_fft))
        C = librosa.amplitude_to_db(C, ref=np.max)
        y_axis='log'
    else:
        raise ValueError(spec_type + 'is not valid type of tranformation')
    
    if plot:
        fig, ax = plt.subplots()
        img = librosa.display.specshow(C, sr=sr, x_axis='time', y_axis=y_axis, ax=ax)
        ax.set_title(plot_name)
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        plt.savefig(plot_name + '.jpg')
    return C

