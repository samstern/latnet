from agent import Agent

class AgentManager(object):
	"""Container of Agent objects"""
	def __init__(self):
		self.agents={}

	def __contains__(self,agent):
		return (agent in self.agents)

	def add(self,agent):
		self.agents.add(agent)

	def agentFactory(self,*args,**kwargs):
		agent=Agent(*args,**kwargs)
		self.add(agent)
