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

	def process(self,in_data,agent_manager,agent_field_name=None,text_field_name='content'):
		"""Iterate through the data, identify the agents and update their attributes based on the contents of the texts"""
		for item in in_data:
			text=item[text_field_name]
			out_data=self.processText(text)
			try:
				agent=item[agent_field_name]
				try: #see if out_data is a dictionary(like) object
					out_data['agent']:agent
				except TypeError:
					pass
			except KeyError:
				pass
			agent_manager.update(out_data)




