#Import libraries, modules
from bs4 import BeautifulSoup
import requests
import csv
import re
import os 

#Create directory 'neverseconds scrape'
os.mkdir('neverseconds scrape')
#define years of blogging activity
years = ['2012/06','2012/07', '2012/08', '2012/09', '2012/10', '2012/11','2012/12', '2013']
#define suffixes for file names
names=['2012_06','2012_07', '2012_08', '2012_09', '2012_10', '2012_11','2012_12', '2013']
i=0
for year in years:
	#Get content of each year's blog posts
	source = requests.get('http://neverseconds.blogspot.com/{0}/'.format(year)).text

	soup = BeautifulSoup(source, 'lxml')
	#Create .csv file with scraped content for each year
	csv_file = open('neverseconds scrape/neverseconds_scrape_{0}.csv'.format(names[i]), 'w', newline='', encoding='utf-8')

	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['headline','summary', 'date'])

	#Get the content for each post in each year 
	for article in soup.find_all('div', class_='date-outer'):
		#Get the post's date for each post in each year
		date = article.h2.text
		date = re.sub("\s+", " ", date)
		#Print to see what is being scraped
		print(date)
		#Get the headline (title) of each post in each year
		try:
			headline = article.find('div', class_='post hentry uncustomized-post-template').h3.a.text
			headline = re.sub("\s+", " ", headline)
			
		#save headline as none when post does not have title
		except Exception as e:
			headline = None
		#Print to see what is being scraped
		print(headline)
		#Get the summary (post's content) of each post in each year
		summary = article.find('div', class_='post-body entry-content').text
		summary = re.sub("\s+", " ", summary)
		#Print to see what is being scraped
		print(summary)
		#write a file with scraped content (title, post's content, date) for each year
		csv_writer.writerow([headline, summary, date])

		
	csv_file.close()
	i=i+1