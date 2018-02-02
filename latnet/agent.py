from collections import defaultdict


class Agent(object):
    """Agents are the nodes in the network"""
    def __init__(self, identifier):
        self.identifier = identifier

    def update(self,*args,**kwargs):
        pass


class TopicSentimentAgent(Agent):
    """An Agent that has a sentiment score for various topics"""
    def __init__(self, identifier):
        super(TopicSentimentAgent, self).__init__(identifier)
        self.topic_sentiment = defaultdict(float)

    def update(self, topic, sentiment):
        if topic is not None:
            net_sentiment=sentiment['net']
            for topic_id, topic_probability in topic:
                print(topic_id)
                print(topic_probability)
                self.topic_sentiment[topic_id] += net_sentiment * topic_probability
