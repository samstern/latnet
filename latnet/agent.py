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

    def toJson(self):
        dictified = self.__dict__
        jsonified = json.dumps(dictified)
        return jsonified

    @classmethod
    def fromJson(cls, in_data):
        out = cls(**in_data)
        return out

    def toNetworkxFormat(self):
        #should be overridden by subclass
        return self.getIdentifier()

class TopicSentimentAgent(Agent):
    """An Agent that has a sentiment score for various topics"""
    def __init__(self, identifier,topic_sentiment=None):
        super(TopicSentimentAgent, self).__init__(identifier)
        if topic_sentiment is None:
            self.topic_sentiment = defaultdict(float)
        elif isinstance(topic_sentiment, dict):
            try:  # when topics are ints but are passed as strings
                self.topic_sentiment = defaultdict(float)
                for topic in topic_sentiment:
                    key = int(topic)
                    self.topic_sentiment[key] = topic_sentiment[topic]
            except ValueError:
                self.topic_sentiment = topic_sentiment
        else:
            raise ValueError('topic_sentiment must be of type dict')

    def update(self, topic, sentiment,topic_prob_weighted=True):
        if topic is not None:
            net_sentiment = sentiment['net']
            if topic_prob_weighted:
                for topic_id, topic_probability in topic:
                    self.topic_sentiment[topic_id] += net_sentiment * topic_probability
            else:
                topics, topic_probability = zip(*topic)
                topic_index=topic_probability.index(max(topic_probability))
                topic_id = topics[topic_index]
                self.topic_sentiment[topic_id] += net_sentiment


    def getTopics(self, topic_strength_threshold):
        out = {key: val for key, val in
               self.topic_sentiment.items() if abs(val) > topic_strength_threshold}
        return out

    def toNetworkXFormat(self):
        return (self.identifier, self.topic_sentiment)

    def reset(self):
        self.topic_sentiment=defaultdict(float)
