from collections import defaultdict


class Relations(object):
    """Abstract class for identifying different and storing types 
    of relations between agents"""
    def __init__(self):
        super(Relations, self).__init__()

    def updateRelations(self, agents):
        pass

    def getRelations(self):
        pass


class CoTopicRelations(object):
    """keep track of which sourcesare contributing to the same topics"""
    def __init__(self, arg):
        super(CoTopicRelations, self).__init__()
        self.topic_contributors = defaultdict(set)

    def updateRelations(self, agent_manager):
        for agent in agent_manager.agents:
            for topic in agent.getTopics():
                self.topic_contributors[topic].add(agent)

    def getRelations(self):
        return self.topic_contributors
