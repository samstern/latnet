from datetime import datetime, timedelta
from builder import Builder
from loader import Loader
from extractor import LDAExtractor, KeywordSentimentExtractor
from agentManager import AgentManager
from agent import TopicSentimentAgent
from relations import CoTopicRelations

if __name__ == "__main__":
    start_date = '08-08-2016'
    num_days = 20
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
        print(date)
        data.executeQuery(query_file, date)  # obtain the data for the given query
        print('pricessing articles')
        builder.process(data, publishers, agent_field_name='source')  # extract the relevant information from the data
        print('updating extractors')
        builder.updateExtractors()
        agents = publishers.agents
        relations.updateRelations(agents)

    agents_filename = '../data/trial1_agents.json'
    relations_filename = '../data/trial1_relations.json'
    extractor_dirname = '../data/extractors/'
    publishers.saveToJson(agents_filename)
    relations.saveToJson(relations_filename)
    builder.saveExtractors(extractor_dirname)

