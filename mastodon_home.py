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
def get_all_posts(bs4_page):
	return JPHTMLParser.find_doms_by_class(bs4_page, "div", "status__wrapper")

# Get dictionary of extracted data
def get_post_content(bs4_page):

	# one type of post
	def post_pattern_visible(post):
		display_name = JPHTMLParser.find_dom_by_class(post, "strong", "display-name__html").contents[0]
		post_content = JPHTMLParser.find_dom_by_class(post, "div", "status__content__text")
		post_content = JPHTMLParser.find_dom_by_class(post, "p", None)
		return display_name, post_content

	# another type of post
	def post_pattern_collapse(post):
		status_spans = JPHTMLParser.find_doms_by_class(post, "span", None)
		display_name, post_content = status_spans[0].contents[0], status_spans[1]
		return display_name, post_content

	pretty_posts = []

	# loop over all posts
	for post in bs4_page:
		status_public = JPHTMLParser.find_dom_by_class(post, "div", "status-public")
		if status_public is None:
			display_name, post_content = post_pattern_collapse(post)
		else:
			display_name, post_content = post_pattern_visible(post)
		
		pretty_posts.append({
			"display_name": display_name,
			"post_content": JPHTMLParser.remove_all_tags(post_content),
		})

	return pretty_posts

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
	# sys.stdout = open('out.html', 'w')

	# setup Selenium
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# get html
	explore_soup = get_soup_html(driver, "https://universeodon.com/explore")

	# extract information from html
	all_posts_bs4 = get_all_posts(explore_soup)
	all_posts = get_post_content(all_posts_bs4)

	# save file
	save_as_json_file(all_posts, "universeodon_explore.json")

if __name__ == "__main__":
	main()