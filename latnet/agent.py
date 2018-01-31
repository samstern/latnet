class Agent(object):
	"""Agents are the nodes in the network"""
	def __init__(self,name):
		self.name=name
		self.topic_sentiment=dict()

	def updateTopicSentiment(topic,sentiment):
		self.topic_sentiment[topic]=sentiment

		
class Publisher(Agent):
	"""news publisher agent"""
	def __init__(self, name):
		super(Publisher, self).__init__()
		self.name=name
		self.topic_sentiment=dict()

