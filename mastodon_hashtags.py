import sys
import time
import json

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Beautifulsoup imports
from bs4 import BeautifulSoup

# Custom helper
from JPHTMLParser import JPHTMLParser

'''
Website related functions.
'''
# Get all posts from Mastodon
def get_all_hashtags(bs4_page):
	return JPHTMLParser.find_doms_by_class(bs4_page, "div", "trends__item__name")

# TODO: d

'''
Selenium functions
'''
# Get beautiful-soup HTML instance
def get_soup_html(driver, url):
	
	# request using selenium driver
	driver.get(url)

	# check if sleep required
	# time.sleep(5)

	# get html from selenium
	explore_home = driver.find_element(By.TAG_NAME, "html").get_attribute("innerHTML")

	# cast to beautifulsoup and return
	return BeautifulSoup(explore_home, "html.parser")

'''
Helper functions
'''
# Save data as json file
def save_as_json_file(obj, filename):
	with open(filename, "w") as f:
		f.write(json.dumps(obj, indent=4))


def main():
	# capturint output in file
	sys.stdout = open('out.html', 'w')

	# setup Selenium
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# get html
	hashtag_soup = get_soup_html(driver, "https://universeodon.com/explore/tags")

	# extract information from html
	all_hashtags_bs4 = get_all_hashtags(hashtag_soup)
	
	'''
	# building blocks
	single = JPHTMLParser.find_dom_by_class(all_hashtags_bs4[0], "a", "permalink")
	url = single.get('href')

	spans = JPHTMLParser.find_doms_by_class(all_hashtags_bs4[0], "span", None)
	hashtag = spans[0].contents[0]
	metainfo = [val.contents for val in spans[1].contents]
	print(spans, hashtag, metainfo)
	'''

if __name__ == "__main__":
	main()