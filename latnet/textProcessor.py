

class TextProcessor(object):
	"""Class for managing what information is extracted from an article and how"""
	def __init__(self):
		self.extractors=[]

	def addExtractor(self,extractor):
		"""add additional extraction step"""
		self.extractors.append(extractor)

	def processText(self,text):
		for extractor in self.extractors:
			extractor.apply(text)
		