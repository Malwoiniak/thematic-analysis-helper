#import modules, libraries
from bs4 import BeautifulSoup
import requests
import csv
import re
import os

#create directory 'jake scrape'
os.mkdir('jake scrape')
#define years of blogging activity
years=['2009','2010','2011','2012','2013','2014','2015','2016']
#Get content of each year's blog posts
for year in years:
	source1 = requests.get('http://www.jakes-bones.com/{0}/'.format(year)).text
	soup1 = BeautifulSoup(source1, 'lxml')
	#in each year, get each post's url and append it to list
	all_url = []
	for article in soup1.find_all('article'):
		post_url = article.find('h2', class_='post-title')
		post_url = post_url.find('a')
		post_url = post_url.get('href')
		all_url.append(post_url)

	#Create .csv file with scraped content for each year
	csv_file = open('jake scrape/jake_scrape_{0}.csv'.format(year), 'w', newline='', encoding='utf-8')

	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['headline', 'summary', 'date'])
	#Get the content for each post in each year 
	for url in all_url:
		source = requests.get(url).text

		soup = BeautifulSoup(source, 'lxml')
		#Get the headline (title) of each post in each year
		for article in soup.find_all('article'):
			headline = article.h2.a.text
			headline = re.sub("\s+", " ", headline)
			#print to see what is being scraped
			print(headline)
			#Get the summary (post's content) of each post in each year
			summary = article.find('div', class_='post-body')
			#remove unnecessary metadata scraped together with post's content
			meta1 = summary.p
			meta2 = summary.find(type="text/javascript")
			meta1.extract()
			meta2.extract()
			summary = summary.text
			summary = re.sub("\s+", " ", summary)
			#print to see what is being scraped
			print(summary)
			#Get the post's date for each post in each year
			date = article.find('span', itemprop='dateCreated').text
			date = re.sub("\s+", " ", date)
			#print to see what is being scraped
			print(date)
			print()
			#write a file with scraped content (title, post's content, date) for each year
			csv_writer.writerow([headline, summary, date])

	csv_file.close()