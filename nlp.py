from typing import *
from sklearn import svm
import spacy
import joblib

class Nlp:
    def train(self, x_data: list, y_data: list) -> None:
        nlp = spacy.load("en_core_web_lg") #model of the word vectors 
        doc = [nlp(text) for text in x_data] #build the word vectors of each sentence
        clf_svm = svm.SVC(kernel="linear") #build a classifier
        clf_svm.fit([x.vector for x in doc], y_data)
        joblib.dump(clf_svm, 'model.joblib')

    def predict(self, test_data: list) -> list:
        nlp = spacy.load("en_core_web_lg")
        clf_svm = joblib.load('model.joblib') 
        result = [clf_svm.predict([nlp(sentence).vector]) for sentence in test_data]
        return result