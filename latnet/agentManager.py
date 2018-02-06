from agent import Agent


class AgentManager(object):
    """Container of Agent objects"""
    def __init__(self, cls):
        assert issubclass(cls, Agent)
        self.cls = cls  # The type of agent we want to work with (e.g., TopicSentimentAgent)
        self.agents = set()  # key value pairs where the keys are the agents' identifiers and the values are the agents
        self.names = dict()  # names of each of the agents


    def __contains__(self, agent):
        if isinstance(agent, self.cls):
            return (agent in self.agents)
        else:
            pass  #TODO: handle case when the agent isn't of type Agent

    def getAgent(self, agent_identifier):
        assert agent_identifier in self.names
        return self.names[agent_identifier]

    def addAgent(self, identifier, *args, **kwargs):
        agent = self.cls(identifier, *args, **kwargs)
        self.names[identifier] = agent
        self.agents.add(agent)
