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
			if agent_field_name is None:
				#--TODO
				#case where agents are extracted from the text and are therefore in the out_data
				pass
			elif isinstance(agent_field_name,basestring):
				#case where the agent names are expected to be in the incoming data
				agent_identifier=item[agent_field_name]

			if agent_identifier not in agent_manager.names:
				agent_manager.addAgent(agent_identifier)
			agent=agent_manager.getAgent(agent_identifier)
			agent.update(out_data)





