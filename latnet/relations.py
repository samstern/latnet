from collections import defaultdict
from fun import set_default
import json

class Relations(object):
    """Abstract class for identifying different and storing types 
    of relations between agents"""
    def __init__(self):
        super(Relations, self).__init__()

    def updateRelations(self, agent_identifies):
        pass

    def getRelations(self):
        pass

    def saveToJson(self,file_name):
        dictified = self.__dict__
        print(dictified)
        rel_types = self.__class__.__name__
        json_obj = dict()
        json_obj['class'] = rel_types
        json_obj['relations'] = dictified
        with open(file_name, 'w') as f:
            json.dump(json_obj, f, default=set_default)

    @classmethod
    def loadFromJson(cls, file_name):
        with open(file_name, 'r') as f:
            from_file = json.load(f)
        print(from_file)
        relation_class = eval(from_file['class'])
        relations_lists = from_file['relations']
        relations_data = {int(key): set(val) for key, val in relations_lists['topic_contributors'].iteritems()}
        print(relations_data)
        relations = relation_class(topic_contributors=relations_data)
        return relations


class CoTopicRelations(Relations):
    """keep track of which sourcesare contributing to the same topics"""
    def __init__(self, topic_contributors=None):
        super(CoTopicRelations, self).__init__()
        if topic_contributors is None:
            self.topic_contributors = defaultdict(set)
        elif isinstance(topic_contributors, dict):
            self.topic_contributors = topic_contributors
        else:
            raise ValueError(('topic_contributors must be of type dict'))

    def updateRelations(self, agents):
        for agent in agents:
            for topic in agent.getTopics():
                self.topic_contributors[topic].add(agent.getIdentifier())

    def getRelations(self):
        return self.topic_contributors
