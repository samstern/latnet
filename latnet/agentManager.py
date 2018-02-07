from agent import *
import json


class AgentManager(object):
    """Container of Agent objects"""
    def __init__(self, agent_type):
        assert issubclass(agent_type, Agent)
        self.agent_type = agent_type  # The type of agent we want to work with (e.g., TopicSentimentAgent)
        self.agents = set()  # key value pairs where the keys are the agents' identifiers and the values are the agents
        self.names = dict()  # names of each of the agents


    def __contains__(self, agent):
        if isinstance(agent, self.agent_type):
            return (agent in self.agents)
        else:
            pass  #TODO: handle case when the agent isn't of type Agent

    def getAgent(self, agent_identifier):
        assert agent_identifier in self.names
        return self.names[agent_identifier]

    def addAgent(self, agent):
        identifier = agent.getIdentifier()
        self.names[identifier] = agent
        self.agents.add(agent)

    def makeAgent(self,identifier, *args, **kwargs):
        agent = self.agent_type(identifier, *args, **kwargs)
        return agent

    def saveToJson(self, file_name):
        with open(file_name, 'w') as f:
            agent_list = []
            for agent in self.agents:
                agent_list.append(agent.toJson())
            json_obj = dict()
            json_obj['agents'] = agent_list
            json_obj['class'] = self.agent_type.__name__
            json.dump(json_obj, f)

    @classmethod
    def loadFromJson(cls, file_name):
        with open(file_name, 'r') as f:
            from_file = json.load(f)
            agent_type = eval(from_file['class'])
            agents = from_file['agents']
            out = cls(agent_type)
            for agent_data in agents:
                un_jsoned=json.loads(agent_data)
                agent = agent_type.fromJson(un_jsoned)
                out.agents.add(agent)
                out.names[agent.getIdentifier] = agent
        return out
