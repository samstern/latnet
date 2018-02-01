from extractor import Extractor

class TextProcessor(object):
	"""Class for managing what information is extracted from an article and how"""
	def __init__(self):
		self.extractors=[]

	def addExtractor(self,extractor):
		"""add additional extraction step"""
		assert isinstance(extractor,Extractor)
		self.extractors.append(extractor)

	def processText(self,text):
		out_data={}
		for extractor in self.extractors:
			out_data[extractor]=extractor.apply(text)
		return out_data
		