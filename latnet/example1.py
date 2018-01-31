from datetime import datetime,timedelta
from builder import Builder
from loader import Loader

if __name__=="__main__":
	start_date='08-08-2016'
	num_days=2
	date_list=[datetime.strptime(start_date,"%d-%m-%Y")+timedelta(days=x) for x in range(num_days)]

	builder=Builder()
	builder.addExtractor(LDAExtractor())
	db_params={'dbname':'moreover','username':'sam','password':'s.stern'}
	data=Loader(**db_params)
	query_file="some/file/name"

	for date in date_list:
		data.executeQuery(query_file,date)
		builder.process(data)

	builder.process(data)