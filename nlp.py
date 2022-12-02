import nltk, spacy, joblib, re
from langdetect import detect
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from typing import *
from sklearn import svm

class Nlp:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")#model of the word vectors 

    def get_wordnet_pos(self,word):
        tag = nltk.pos_tag([word])[0][1][0].lower()
        if tag not in ['n', 'v', 'a', 'r']:
            return "n"
        return tag

    def text_process(self, phrase:str)->str:
        
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = stopwords.words('english')

        regex = r"(?i)([0-9])|(\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])))"
        phrase = re.sub(regex, '', phrase) #remove number and url from phrase

        if detect(phrase) != 'en':
            raise KeyError

        words = tokenizer.tokenize(phrase) #remove punctuation

        stripped_phrase = []  #remove stopwords
        for word in words:
            if word not in stop_words:
                stripped_phrase.append(word)

        stemmed_words = [] #stemming
        for word in stripped_phrase:
            stemmed_words.append(stemmer.stem(word))

        lemmatized_words = [] #lemmatization
        for word in stemmed_words:
            lemmatized_words.append(lemmatizer.lemmatize(word, self.get_wordnet_pos(word)))

        return (" ".join(lemmatized_words))
    

    def train(self, x_data: list, y_data: list) -> None: #
        """
        `x_data` need to be a list contain mutiple `list`
            each `list` represent comments of one song
        
        `y_data` contain result

        this two list's size should be same
        """
        if len(x_data) != len(y_data):
            raise KeyError
        train_x = []
        for phrases in x_data:
            all_phrase = []
            for phrase in phrases:
                try:
                    words = self.text_process(phrase)
                    all_phrase.append(words)
                except:
                    pass
            train_x.append(" ".join(all_phrase))

        nlp = self.nlp
        doc = [nlp(text) for text in train_x] #build the word vectors of each sentence
        clf_svm = svm.SVC(kernel="linear") #build a classifier
        clf_svm.fit([x.vector for x in doc], y_data)
        joblib.dump(clf_svm, 'model.joblib')

    def predict(self, test_data: list) -> list:
        """
        predict the result of `test_data`
        """
        nlp = self.nlp
        clf_svm:svm.SVC = joblib.load('model.joblib') 
        result = [clf_svm.predict([nlp(sentence).vector]) for sentence in test_data]
        return result