from agent import Agent

class AgentManager(object):
	"""Container of Agent objects"""
	def __init__(self,cls):
		assert issubclass(cls,Agent)
		self.cls=cls # The type of agent we want to work with (e.g., TopicSentimentAgent)
		self.agents={}

	def __contains__(self):
		if isinstance(agent,self.cls):
			return (agent in self.agents)
		else:
			pass #TODO: handle case when the agent isn't of type Agent

	def update(self,update_data):
		try: 
			update_data['agent']


	def add(self,agent):
		self.agents.add(agent)

	def updateAgent(self,agent,data):
		if agent in self.agents:
			agent.update(data)
		else:


	def agentFactory(self,*args,**kwargs):
		agent=self.cls(*args,**kwargs)
		self.add(agent)
