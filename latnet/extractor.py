from gensim import corpora
from gensim import models
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class Extractor(object):
	"""docstring for Extractor"""
	def __init__(self, arg):
		self.arg = arg
	
	def apply(self,text):
		pass	


class SentimentExtractor(Extractor):
	"""docstring for SentimentExtractor"""
	def __init__(self, arg):
		super(SentimentExtractor, self).__init__()
		self.arg = arg

	def apply(self,text):
		pass


class TopicExtractor(Extractor):
	"""docstring for TopicExtractor"""
	def __init__(self):
		pass

	def apply(self,text):	
		pass

class LDAExtractor(TopicExtractor):
	"""docstring for LDAExtractor"""
	def __init__(self, num_topics=50):
		super(LDAExtractor, self).__init__()
		self.num_topics = num_topics

		self.tokenizer=RegexpTokenizer(r'\w+')
		self.stemmer = SnowballStemmer("english")

	def apply(self,text):
		pass