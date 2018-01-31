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
	def __init__(self, num_topics=50,eta=0.0001):
		super(LDAExtractor, self).__init__()
		self.num_topics = num_topics

		self.tokenizer=RegexpTokenizer(r'\w+')
		self.stemmer = SnowballStemmer("english")

		self.stopless=[]

		self.lda_model=None

	def apply(self,text):
		tokenized=self.tokenizer.tokenize(text)
		self.stopless.append([token for token in tokenized if token not in stopwords.words('english')])

	def update(self):
		bigram=models.phrases.Phrases(self.stopless)
		dictionary = corpora.Dictionary(bigram[self.stopless])
		corpus = [dictionary.doc2bow(text) for text in bigram[self.stopless]]
		try:
			self.lda_model.update(corpus)
		except AttributeError:
			num_tokens=len(dictionary.token2id)
			etas=np.full([self.num_topics,num_tokens],eta)
			self.lda_model=models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=self.num_topics,alpha='auto',eta='auro',passes=5)
		