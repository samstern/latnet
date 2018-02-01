from gensim import corpora
from gensim import models
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import json

class Extractor(object):
	"""docstring for Extractor"""
	def __init__(self):
		pass
	
	def apply(self,text):
		pass	

	def update(self,*args,**kwargs):
		pass


class SentimentExtractor(Extractor):
	"""docstring for SentimentExtractor"""
	def __init__(self):
		super(SentimentExtractor, self).__init__()

	def apply(self,text):
		pass

	def update(self,*args,**kwargs):
		pass

class KeywordSentimentExtractor(SentimentExtractor):
	"""docstring for KeywordSentimentExtractor"""
	def __init__(self, keyword_file="../data/sentiment_keywords.json"):
		super(KeywordSentimentExtractor, self).__init__()
		with open(keyword_file,'r') as f:
			keywords=json.load(f)
			self.excitement_keywords=keywords['Excitement']
			self.anxiety_keywords=keywords['Anxiety']

	def apply(self,text,count_method='count',net_method='ratio'):
		emotion_count={'anxiety':0,'excitement':0,'net':0}
		emotion_count['anxiety']+=countKeywords(text,self.anxiety_keywords,method=count_method)
		emotion_count['excitement']+=countKeywords(text,self.excitement_keywords,method=count_method)
		emotion_count['net']=netSentiment(emotion_count['anxiety'],emotion_count['excitement'],method=net_method)
		return emotion_count

	def update(self,*args,**kwargs):
		pass

def countKeywords(text,keywords,method="count"):
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
			return float(excitement)/float(anxiety)
		except ZeroDivisionError:
			epsilon=0.0000001
			ex_eps=excitement+epsilon
			an_eps=anxiety+epsilon
			return ex_eps/an_eps
	elif method=="percent":
		"""the percentage of emotive words that are excitement"""
		try:
			return float(excitement)/float(anxiety+excitement)
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

	def update(self,*args,**kwargs):
		pass

class LDAExtractor(TopicExtractor):
	"""docstring for LDAExtractor"""
	def __init__(self, num_topics=50,eta=0.,bigram_mode=False):
		super(LDAExtractor, self).__init__()
		self.num_topics = num_topics
		self.bigram_mode = bigram
		if self.bigram_mode:
			self.bigram=models.phrases.Phrases()

		self.tokenizer = RegexpTokenizer(r'\w+')
		self.stemmer = SnowballStemmer("english")

		self.stopless=[]
		self.gs_dict=corpora.Dictionary()

		self.lda_model=None

	def apply(self,text):
		tokenized=self.tokenizer.tokenize(text)
		self.stopless.append([token for token in tokenized if token not in stopwords.words('english')])
		doc_bow=self.dict.doc2bow(text)

		try:
			return self.lda_model.get_document_topics(doc_bow)
		except AttributeError:
			return None

	def update(self):
		if self.bigram_mode:
			#bigram=models.phrases.Phrases(self.stopless)
			self.bigram.add_vocab(self.stopless)
			self.dict.add_documents(bigram[self.stopless])
			corpus=[self.dict.doc2bow(text) for text in bigram[self.stopless]]
		else:
			self.dict.add_documents(self.stopless)
			corpus=[self.dict.doc2bow(text) for text in self.stopless]]
		#dictionary = corpora.Dictionary(bigram[self.stopless])
		#corpus = [dictionary.doc2bow(text) for text in bigram[self.stopless]]
		try:
			self.lda_model.update(corpus)
		except AttributeError:
			num_tokens=len(dictionary.token2id)
			etas=np.full([self.num_topics,num_tokens],eta)
			self.lda_model=models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=self.num_topics,alpha='auto',eta='auro',passes=5)
		
	def resetStopless(self):
		self.stopless=[]