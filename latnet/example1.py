from datetime import datetime,timedelta
from builder import Builder
from loader import Loader
from extractor import LDAExtractor,KeywordSentimentExtractor
from agentManager import AgentManager
from agent import TopicSentimentAgent

if __name__=="__main__":
	start_date='08-08-2016'
	num_days=2
	date_list=[datetime.strptime(start_date,"%d-%m-%Y")+timedelta(days=x) for x in range(num_days)]

	builder=Builder()
	builder.addExtractor(LDAExtractor())
	builder.addExtractor(KeywordSentimentExtractor())
	publishers=AgentManager(TopicSentimentAgent)
	db_params={'dbname':'moreover','username':'sam','password':'s.stern'}
	data=Loader(**db_params)
	query_file="simple query"

	for date in date_list:
		data.executeQuery(query_file,date) #obtain the data for the given query
		builder.process(data,publishers,agent_field_name='source') #extract the relevant information from the data