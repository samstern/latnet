class Agent(object):
	"""Agents are the nodes in the network"""
	def __init__(self,id,name):
		self.id=id
		self.name=name

	def update(self):
		pass

		
class TopicSentimentAgent(Agent):
	"""An Agent that has a sentiment score for various topics"""
	def __init__(self, id, name):
		super(TopicSentimentAgent, self).__init__(id,name)
		self.topic_sentiment=dict()
		
	def update(self,topic,sentiment):
		self.topic_sentiment[topic]=sentiment
