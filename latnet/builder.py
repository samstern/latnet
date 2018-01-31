from loader import Loader
from textProcessor import TextProcessor
from extractor import LDAExtractor
from datetime import datetime

class Builder(object):
	"""Handels the processing of multiple texts"""
	def __init__(self, start_date,end_date):
		self.start_date = start_date
		self.end_date = end_date
		self.textProcessor= TextProcessor()

	def addExtractor(self,extractor):
		self.textProcessor.addExtractor(extractor)

	def processText(self,text):
		self.textProcessor.processText(text)

	def process(self,in_data,text_field_name='content'):
		for item in loader:
			text=item['text_field_name']
			self.processText(text)




if __name__=="__main__":
	builder=Builder('2016-08-08','2016-08-09')
	builder.addExtractor(LDAExtractor())
	db_params={'dbname':'moreover','username':'sam','password':'s.stern'}
	data=Loader(**db_params)




		
