import sys
import time

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

# Get beautiful-soup HTML instance
def get_soup_html(driver, url):
	
	# request using selenium driver
	driver.get(url)

	# check if sleep required
	time.sleep(5)

	# get html from selenium
	explore_home = driver.find_element(By.TAG_NAME, "html").get_attribute("innerHTML")

	# cast to beautifulsoup and return
	return BeautifulSoup(explore_home, "html.parser")

def main():
	# capturint output in file
	# orig_stdout = sys.stdout
	# f = open('out.html', 'w')
	sys.stdout = open('out.html', 'w')

	# setup Selenium
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# get html
	explore_soup = get_soup_html(driver, "https://universeodon.com/explore")

	# extract information from html
	all_posts_bs4 = get_all_posts(explore_soup)
	all_posts = get_post_content(all_posts_bs4)
	print(all_posts)

	# Server Configuration and Initialization
	# w = JPFaktoryWrapper(faktory=config["fk_config"]["url"], queues=[config["fk_config"]["crawler_queue"], config["fk_config"]["s3_upload_queue"]], concurrency=config["fk_config"]["num_workers"])
	# w.register('thread_page_parser', thread_page_parser)
	# w.register('thread_s3_uploader', thread_s3_uploader)
	# w.run()

if __name__ == "__main__":
	main()