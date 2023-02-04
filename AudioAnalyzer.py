import os
import librosa
import numpy as np
import pydub
class AudioAnalyzer:

    def __init__(self):
        return
    
    def Resize(self, data, n):
        Ok = np.resize(data, (data.shape[0], n))
        return Ok
    
    def analyze_STFT(self, Audio, time_size):
        y, sr = librosa.load(Audio)
        STFT = librosa.stft(y)
        STFT = self.Resize(STFT, time_size)
        return STFT #numpy

    def analyze_MFCC(self, Audio, time_size):
        y,sr = librosa.load(Audio)
        MFCC = librosa.feature.mfcc(y = y, sr = sr)
        MFCC = self.Resize(MFCC, time_size)
        return MFCC #numpy

    def analyze_CQT(self, Audio, time_size):
        y, sr = librosa.load(Audio)
        CQT = librosa.feature.chroma_cqt(y = y,sr = sr)
        CQT = self.Resize(CQT, time_size)
        return CQT #numpy

    def analyze_ALL(self, Audio, time_size):
        y, sr = librosa.load(Audio)
        STFT = librosa.stft(y)
        STFT = self.Resize(STFT, time_size)
    
        MFCC = librosa.feature.mfcc(y = y,sr = sr)
        MFCC = self.Resize(MFCC, time_size)
    
        CQT = librosa.feature.chroma_cqt(y = y,sr = sr)
        CQT = self.Resize(CQT, time_size)
        
        totaldata = np.vstack([STFT, MFCC])
        totaldata = np.vstack([totaldata, CQT])
        return totaldata #numpy
    
    def save(self, data, path):
        np.save(path, data)
        
    def get_raw_data(self,f, normalized=False):
        """MP3 to numpy array"""
        a = pydub.AudioSegment.from_mp3(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y

'''debug
a=AudioAnalyzer()
path='1/1.mp3'
print(a.Analyze_ALL(path, 5000).shape)
'''