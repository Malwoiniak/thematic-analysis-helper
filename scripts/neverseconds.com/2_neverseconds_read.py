import pandas as pd
from textblob import TextBlob
import csv
import os 
def get_sentiment(df):
	"""Returns sentiment's polarity for each post in given dataframe's summary column 

	Parameters:
	Summary(dataframe): text to perform above

	Returns: List of sentiments' polarity in given dataframe's summary column
	"""
	i=0
	all_senti = []
	for post in df.summary:
		sentiment = TextBlob(df.summary[i]).sentiment[0]
		all_senti.append(sentiment)
		i=i+1
	return all_senti

#Create directory 'neverseconds final'
os.mkdir('neverseconds scrape/neverseconds final')
#define suffixes for file names (years_months of blogging activity)
names=['2012_06','2012_07', '2012_08', '2012_09', '2012_10', '2012_11','2012_12', '2013']
for name in names:
	#Read .csv files of scraped post's content for each year as dataframe 
	df = pd.read_csv('neverseconds scrape/neverseconds_scrape_{0}.csv'.format(name))
	#Convert date to pandas datetime format
	df['date'] = pd.to_datetime(df['date'], format='%A, %d %B %Y')
	#Get list of sentiment's polarity for all posts content in each year
	all_senti = get_sentiment(df)
	#Create .csv file for polarity values in each year
	csv_file = open('neverseconds scrape/neverseconds final/neverseconds_{0}_headline_polarity.csv'.format(name), 'w', newline='', encoding='utf-8')

	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['headline', 'polarity', 'sentiment', 'date'])
	#Get headline (post's title), polarity value, sentiment assesment(neg,pos,neu)and date for each post in each year
	i=0
	for item in df.headline:
		headline = df.headline[i]
		polarity = all_senti[i]
		if polarity > 0:
			sent = 'positive'
		elif polarity == 0:
			sent = 'neutral'
		else:
			sent = 'negative'
		date = df.date[i]
		#print to see what is being saved 
		print(headline, polarity, sent, date)
		i=i+1

		csv_writer.writerow([headline, polarity, sent, date])

	csv_file.close()