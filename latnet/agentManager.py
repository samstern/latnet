from agent import Agent

class AgentManager(object):
	"""Container of Agent objects"""
	def __init__(self,cls):
		assert issubclass(cls,Agent)
		self.cls=cls # The type of agent we want to work with (e.g., TopicSentimentAgent)
		self.agents=dict() # key value pairs where the keys are the agents' identifiers and the values are the agents
		self.names=set() #names of each of the agents

	def __contains__(self,agent):
		if isinstance(agent,self.cls):
			return (agent in self.agents)
		else:
			pass #TODO: handle case when the agent isn't of type Agent

	def getAgent(self,agent_identifier):
		assert agent_identifier in self.agents
		return self.agents[agent]

	#def update(self,update_data):
	#	try: 
	#		update_data['agent']


	def addAgent(self,*args,**kwargs):
		agent=self.cls(*args,**kwargs)
		self.agents.add(agent)

	#def updateAgent(self,agent,data):
	#	if agent in self.agents:
	#		agent.update(data)
	#	else:
