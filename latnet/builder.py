from textProcessor import TextProcessor
from extractor import LDAExtractor

class Builder(object):
	"""Handels the processing of multiple texts"""
	def __init__(self):
		self.textProcessor= TextProcessor()

	def addExtractor(self,extractor):
		self.textProcessor.addExtractor(extractor)

	def processText(self,text):
		self.textProcessor.processText(text)

	def process(self,in_data,text_field_name='content'):
		for item in in_data:
			text=item[text_field_name]
			self.processText(text)




