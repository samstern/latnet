from collections import defaultdict
import json

class Relations(object):
    """Abstract class for identifying different and storing types 
    of relations between agents"""
    def __init__(self):
        super(Relations, self).__init__()

    def updateRelations(self, agents):
        pass

    def getRelations(self):
        pass

    def saveToJson(self,file_name):
        dictified = self.__dict__
        rel_types = self.__class__.__name__
        json_obj = dict()
        json_obj['class'] = rel_types
        json_obj['relations'] = dictified
        with open(file_name, 'w') as f:
            json.dump(json_obj, f)

    @classmethod
    def fromJson(cls, file_name):
        with open(file_name, 'r') as f:
            from_file = json.load(f)
        relation_class = eval(from_file['class'])
        relations_data = from_file['relations']
        relations = relation_class(**relations_data)
        return relations


class CoTopicRelations(object):
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
                self.topic_contributors[topic].add(agent)

    def getRelations(self):
        return self.topic_contributors
