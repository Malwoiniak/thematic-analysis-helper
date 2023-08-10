#import modules, libraries
from bs4 import BeautifulSoup
import requests
import csv
import re
import os

#Create directory 'neverseconds scrape'
os.mkdir('libdem scrape')
#define years of blogging activity
years = ['2010','2011', '2012', '2013', '2014', '2015','2016', '2017']
for year in years:
	#Get content of each year's blog posts
	source = requests.get('http://libdemchild.blogspot.com/{0}/'.format(year)).text

	soup = BeautifulSoup(source, 'lxml')
	#Create .csv file with scraped content for each year
	csv_file = open('libdem scrape/libdem_scrape_{0}.csv'.format(year), 'w', newline='',encoding='utf-8')

	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['headline', 'summary', 'date'])

	#Get the content for each post in each year
	for article in soup.find_all('div', class_='date-outer'):
		#Get the post's headline (title) for each post in each year
		headline = article.find('div', class_='post hentry').h3.a.text
		headline = re.sub("\s+", " ", headline)
		#Print to see what is being scraped
		print(headline)
		#Get the post's summary (post's content) for each post in each year
		summary = article.find('div', class_='post-body entry-content').text
		summary = re.sub("\s+", " ", summary)
		#Print to see what is being scraped
		print(summary)
		#Get the post's date for each post in each year
		date = article.h2.text
		date = re.sub("\s+", " ", date)
		#Print to see what is being scraped
		print(date)
		print()

		csv_writer.writerow([headline, summary, date])

	csv_file.close()
