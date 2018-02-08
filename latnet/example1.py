from datetime import datetime, timedelta
from builder import Builder
from loader import Loader
from extractor import LDAExtractor, KeywordSentimentExtractor
from agentManager import AgentManager
from agent import TopicSentimentAgent
from relations import CoTopicRelations
import os

print(os.getcwd())

if __name__ == "__main__":
    start_date = '08-08-2016'
    num_days = 2
    date_list = [datetime.strptime(start_date, "%d-%m-%Y") +
                 timedelta(days=x) for x in range(num_days)]
    gs_dict = '../data/gensim/wiki_en_wordids.txt.bz2'

    builder = Builder()
    builder.addExtractor(LDAExtractor(dictionary=gs_dict))
    builder.addExtractor(KeywordSentimentExtractor())
    publishers = AgentManager(TopicSentimentAgent)
    relations = CoTopicRelations()
    db_params = {'dbname': 'moreover',
                 'user': 'sam',
                 'password': 's.stern'}
    data = Loader(**db_params)
    query_file = "simple query"

    for date in date_list:
        data.executeQuery(query_file, date)  # obtain the data for the given query
        builder.process(data, publishers, agent_field_name='source')  # extract the relevant information from the data
        agents = publishers.agents
        relations.updateRelations(agents)

    agents_filename = '../data/example1_out.json'
    relations_filename = '../data/example1_relations.json'
    publishers.saveToJson(agents_filename)

    loaded_agents=AgentManager.loadFromJson(agents_filename)
    for agent in loaded_agents.agents:
        print(agent.identifier)

    relations.saveToJson(relations_filename)
    for relation in relations.topic_contributors:
        print(relation)
    
    loaded_rels=CoTopicRelations.loadFromJson(relations_filename)
    for relation in loaded_rels.topic_contributors:
        print(relation)
    print(relations==loaded_rels)
