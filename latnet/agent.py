from collections import defaultdict
import json

class Agent(object):
    """Agents are the nodes in the network"""
    def __init__(self, identifier):
        self.identifier = identifier

    def getIdentifier(self):
        return self.identifier

    def update(self, *args, **kwargs):
        pass

    @classmethod
    def fromJson(cls, in_data):
        out = cls(**in_data)


class TopicSentimentAgent(Agent):
    """An Agent that has a sentiment score for various topics"""
    def __init__(self, identifier,topic_sentiment=None):
        super(TopicSentimentAgent, self).__init__(identifier)
        if topic_sentiment is not None:
            self.topic_sentiment = defaultdict(float)
        elif isinstance(topic_sentiment,dict):
            self.topic_sentiment = topic_sentiment
        else:
            raise ValueError('topic_sentiment must be of type dict')

    def update(self, topic, sentiment):
        if topic is not None:
            net_sentiment = sentiment['net']
            for topic_id, topic_probability in topic:
                print(topic_id)
                print(topic_probability)
                self.topic_sentiment[topic_id] += net_sentiment * topic_probability

    def getTopics(self, topicStrengthThreshold=2):
        out = {key: val for key, val in
               self.topic_sentiment.iteritems() if abs(val) > topicStrengthThreshold}
        return out

    def toJson(self):
        dictified = self.__dict__
        jsonified = json.dumps(dictified)
        return jsonified

