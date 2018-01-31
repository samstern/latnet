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

class KeywordSentimentExtractor(SentimentExtractor):
	"""docstring for KeywordSentimentExtractor"""
	def __init__(self, keyword_file="../data/sentiment_keywords.json"):
		super(KeywordSentimentExtractor, self).__init__()
		with open(keyword_file,'r') as f:
			keywords=json.load(f)
			self.excitement_keywords=keywords['Excitement']
			self.anxiety_keywords=keywords['Anxiety']

	def apply(self,text):
		emotion_count={'anxiety':0,'excitement':0,'net':0}
		emotion_count['anxiety']+=countKeywords(article,self.anxiety_keywords)
		emotion_count['excitement']+=countKeywords(article,self.excitement_keywords)
		emotion_count['net']=netSentiment(emotion_count['anxiety'],emotion_count['excitement'],method='ratio')
		return emotion_count

def function(text,keywords,method="count"):
	count=0
	lower=text.lower()
	for word in keywords:
		if method=="count":
			count+=lower.count(word)
		elif method=="exists":
			count+=(word in lower)
		else:
			raise ValueError("invalid argument for the 'method' parameter. Valid methods are 'count' and 'exists'.")
		return count
def netSentiment(anxiety,excitement,method="difference"):
	if method=="difference":
		"""hoe many more excitement words than there are anxiety words"""
		return excitement-anxiety
	elif method=="ratio":
		"""the ratio of excitement words to anxiety words"""
		try:
			return double(excitement)/double(anxiety)
		except ZeroDivisionError:
			epsilon=0.0000001
			ex_eps=excitement+epsilon
			an_eps=anxiety+epsilon
			return ex_eps/an_eps
	elif method=="percent":
		"""the percentage of emotive words that are excitement"""
		try:
			return double(excitement)/double(anxiety+excitement)
		except ZeroDivisionError:
			epsilon=0.0000001
			ex_eps=excitement+epsilon
			an_eps=anxiety+epsilon
			return ex_eps/(an_eps+ex_eps)
	else:
		raise ValueError("invalid argument for the 'method' paramiter. Valid methods are 'difference'','ratio', and 'percent'")



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
		