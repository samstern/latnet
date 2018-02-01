class Agent(object):
	"""Agents are the nodes in the network"""
	def __init__(self,identifier):
		self.identifier=identifier

	def update(self):
		pass

		
class TopicSentimentAgent(Agent):
	"""An Agent that has a sentiment score for various topics"""
	def __init__(self, identifier):
		super(TopicSentimentAgent, self).__init__(identifier)
		self.topic_sentiment=dict()

	def update(self,topic,sentiment):
		self.topic_sentiment[topic]=sentiment
