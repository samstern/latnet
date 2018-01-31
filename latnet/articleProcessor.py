

class TextProcessor(object):
	"""Class for managing what information is extracted from an article and how"""
	def __init__(self, arg):
		self.extractors=[]

	def addExtractor(self,extractor):
		"""add additional extraction step"""
		self.extractors+=extractor

	def processArticle(self,text):
		for extractor in self.extractors:
			extractor.apply(text)
		