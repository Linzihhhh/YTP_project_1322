import torch
import torch.nn as nn
import torchvision
import torchvision.models as models

import librosa

import numpy as np

from .downloader import YoutubeDownloader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Predictor:

    def __init__(self):

        self.model = models.mobilenet_v3_small()
        self.model.features[0][0] = nn.Conv2d(1, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        self.model.classifier[3] = nn.Linear(in_features=1024, out_features=4, bias=True)

        self.model.load_state_dict(torch.load("model.pth", map_location=device))
        self.model.eval()

    def _transform(cls, audio):
        """
        Give a music directory and transform it into a ndarray
        """
        y, sr = librosa.load(audio)
        y_44100 = librosa.resample(y, orig_sr=sr, target_sr=44100)
        
        stft = librosa.stft(y_44100)
        stft = stft[:,1000:2000]
        return stft
    
    async def predict(self, id: str):
        """
        Give a song id and return the most possible class
        """
        await YoutubeDownloader.download(id, path="Songs")
        data = self._transform(f"Songs/{id}.mp3")
        return self._predict(data)

    def _predict(self, audio):
        """
        Give a feature ndarray and return the most possible class
        """
        with torch.no_grad():
            # data = np.array([[AudioAnalyzer._get_data("qeEIfm6FXxg.mp3")]])
            data = np.array([[audio]])
            # print(data.shape)
            data = torch.from_numpy(data).abs()

            outputs = self.model(data)
            # print(outputs[0])
            outputs = nn.functional.softmax(outputs[0])
            # print(outputs)
            _, predicted = torch.max(outputs, 0)

            return predicted.item()

predictor = Predictor()