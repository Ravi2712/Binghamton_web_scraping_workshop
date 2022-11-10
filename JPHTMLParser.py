import re
import bs4

'''
This is early world of Beautiful Soup Wrapper.
'''

class JPHTMLParser:

	@staticmethod
	def __object_validation(html_page):
		if not isinstance(html_page, bs4.element.Tag):
			html_page = bs4.BeautifulSoup(html_page, 'html.parser')
		return html_page

	@staticmethod
	def find_doms_by_regex(html_page, regex=None):
		html_page = JPHTMLParser.__object_validation(html_page)
		matches = html_page.find_all(id=re.compile(regex))
		return matches

	@staticmethod
	def find_dom_by_id(html_page, dom_id=None):
		pass

	@staticmethod
	def find_doms_by_class(html_page, html_tag, css_class):
		html_page = JPHTMLParser.__object_validation(html_page)
		matches = html_page.find_all(html_tag, class_=css_class)
		return matches

	@staticmethod
	def find_dom_by_class(html_page, html_tag, css_class):
		html_page = JPHTMLParser.__object_validation(html_page)
		matches = html_page.find(html_tag, class_=css_class)
		return matches

	@staticmethod
	def find_dom_by_tag(html_page, html_tag):
		html_page = JPHTMLParser.__object_validation(html_page)
		matches = html_page.find(html_tag)
		return matches

	@staticmethod
	def remove_all_tags(html_page):
		# NOTE: html_page might change the original reference. But, we are not making a clone to respect the time complexity.
		for data in html_page(['style']):
			data.decompose()
		return ' '.join(html_page.stripped_strings)