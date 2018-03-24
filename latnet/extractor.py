from gensim import corpora
from gensim import models
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import json
import numpy as np
import os


class Extractor(object):
    """
    docstring for Extractor
    """
    def __init__(self,name="base extractor"):
        self.name=name

    def apply(self, text):
        pass

    def update(self, *args, **kwargs):
        pass

    def getName(self):
        """name must match the input parameter of the agent"""
        return self.name

    def save(self,dir_name):
        pass

class SentimentExtractor(Extractor):
    """docstring for SentimentExtractor"""
    def __init__(self, name="sentiment"):
        super(SentimentExtractor, self).__init__(name=name)

    def apply(self, text):
        pass

    def update(self, *args, **kwargs):
        pass

class KeywordSentimentExtractor(SentimentExtractor):
    """docstring for KeywordSentimentExtractor"""
    def __init__(self, keyword_file=os.path.join(os.path.dirname(__file__), "../data/sentiment_keywords.json")):
        super(KeywordSentimentExtractor, self).__init__()
        with open(keyword_file, 'r') as f:
            keywords = json.load(f)
            self.excitement_keywords = keywords['Excitement']
            self.anxiety_keywords = keywords['Anxiety']

    def apply(self, text, count_method='count', net_method='difference'):
        text_len=len(text)
        emotion_count = {'anxiety': 0, 'excitement': 0, 'net': 0}
        emotion_count['anxiety'] += countKeywords(
            text, self.anxiety_keywords, method=count_method)
        emotion_count['excitement'] += countKeywords(
            text, self.excitement_keywords, method=count_method)
        emotion_count['net'] = netSentiment(emotion_count['anxiety'],
                                            emotion_count['excitement'],
                                            method=net_method,text_len=text_len)
        return emotion_count

    def update(self, *args, **kwargs):
        pass


def countKeywords(text, keywords, method="count"):
    count = 0
    lower = text.lower()
    for word in keywords:
        if method == "count":
            count += lower.count(word)
        elif method == "exists":
            count += (word in lower)
        else:
            raise ValueError("invalid argument for the 'method' parameter. \
                Valid methods are 'count' and 'exists'.")
        return count


def netSentiment(anxiety, excitement, method="difference", text_len=None):
    if method == "difference":
        """hoe many more excitement words than there are anxiety words"""
        try:
            return (excitement - anxiety)/text_len
        except ZeroDivisionError:
            return 0.0
        except TypeError:
            print("need to pass the length of the text to netSentiment")
    elif method == "ratio":
        """the ratio of excitement words to anxiety words"""
        try:
            return float(excitement) / float(anxiety)
        except ZeroDivisionError:
            epsilon = 1
            ex_eps = excitement + epsilon
            an_eps = anxiety + epsilon
            return ex_eps / an_eps
    elif method == "percent":
        """the percentage of emotive words that are excitement"""
        try:
            return float(excitement) / float(anxiety + excitement)
        except ZeroDivisionError:
            epsilon = 0.0000001
            ex_eps = excitement + epsilon
            an_eps = anxiety + epsilon
            return ex_eps / (an_eps + ex_eps)
    else:
        raise ValueError("invalid argument for the 'method' paramiter. \
            Valid methods are 'difference'','ratio', and 'percent'")


class TopicExtractor(Extractor):
    """docstring for TopicExtractor"""
    def __init__(self, name="topic"):
        super(TopicExtractor, self).__init__(name=name)

    def apply(self, text):
        pass

    def update(self, *args, **kwargs):
        pass


class LDAExtractor(TopicExtractor):
    """docstring for LDAExtractor"""
    def __init__(self, num_topics=50, eta=0.0001,
                 bigram_mode=False, dictionary=None,remove_stopwords=False):
        super(LDAExtractor, self).__init__()
        self.num_topics = num_topics
        self.bigram_mode = bigram_mode
        self.eta = eta
        self.remove_stopwords=remove_stopwords
        if self.bigram_mode:
            self.bigram = models.phrases.Phrases()

        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = SnowballStemmer("english")

        self.stopless = []
        self.corpus = []
        if dictionary is None:
            self.dictionary = corpora.Dictionary()

        else:
            self.dictionary = corpora.Dictionary.load_from_text(dictionary)

        self.lda_model = None

    def save(self,dir_name):
        self.lda_model.save(dir_name+'lda_model')

    @classmethod
    def load_lda_model(cls,lda_file):
        cls=cls()
        cls.lda_model=models.ldamulticore.LdaMulticore.load(lda_file)
        cls.dictionary=cls.lda_model.id2word
        cls.num_topics=cls.lda_model.num_topics
        return cls

    def apply(self, text):
        tokenized = self.tokenizer.tokenize(text)
        if self.remove_stopwords:
            tokenized = [token for token in tokenized
                            if token not in stopwords.words('english')]
    #        self.stopless.append(tokenized)

        try:
            doc_bow = self.dictionary.doc2bow(tokenized)
            if self.bigram_mode:
                self.bigram.add_vocab(tokenized)
                self.corpus.append(self.dictionary.doc2bow(self.bigram[tokenized]))
            else:
                self.corpus.append(self.dictionary.doc2bow(tokenized))
            document_topics = self.lda_model.get_document_topics(doc_bow)
            return document_topics
        except AttributeError:
            return None

    def update(self,passes=5,iterations=100):
        '''
        if self.bigram_mode:
            # bigram=models.phrases.Phrases(self.stopless)
            self.bigram.add_vocab(self.stopless)
            # self.dictionary.add_documents(self.bigram[self.stopless])
            corpus = [self.dictionary.doc2bow(text)
                      for text in self.bigram[self.stopless]]
        else:
            # self.dictionary.add_documents(self.stopless)
            corpus = [self.dictionary.doc2bow(text) for text in self.stopless]
        # dictionary = corpora.Dictionary(bigram[self.stopless])
        # corpus = [dictionary.doc2bow(text) for text in bigram[self.stopless]]
        '''
        try:
            self.lda_model.update(self.corpus)
        except AttributeError:
            # num_tokens = len(self.dictionary.token2id)
            # etas = np.full([self.num_topics, num_tokens], self.eta)
            self.lda_model = models.ldamulticore.LdaMulticore(
                corpus=self.corpus, id2word=self.dictionary,
                num_topics=self.num_topics,passes=passes,iterations=iterations) #, alpha='auto',
                # eta='auto', passes=5)
#        self.resetStopless()
        self.resetCorpus()

    def resetStopless(self):
        self.stopless = []

    def resetCorpus(self):
        self.corpus = []
