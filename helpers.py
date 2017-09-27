from bs4 import BeautifulSoup
from math import ceil
import requests


# URL builder.
class UrlBuilder:
	'''Prepare the URL for a search request.'''
	base_url = 'https://pure.uvt.nl/portal/en/persons/search.html?'
	args = {
			'uri' 					: '',
			'organisationName' 	 	: '',
			'organisations' 		: ''}


	def __init__(self, search, page=0):
		'''Construct the dynamic arguments and the final URL.'''
		self.dynamic_args = self.dynamic_args(search)
		self.url = self.build_url(page)


	@property
	def static_args(self):
		'''Prepare the static query parameters.'''
		return ''.join(['%s=%s&' % (arg, val) for arg, val in self.args.items()])


	def dynamic_args(self, search):
		'''Prepare the dynamic query parameters.'''
		return 'search=%s' % search


	def build_url(self, page):
		'''Build the final URL.'''
		url = '%s%s%s' % (self.base_url, self.static_args, self.dynamic_args)
		# If there is pagination, append the current page.
		if page > 0:
			url = '%s&page=%s' % (url, page)
		return url



# URL fetcher.
class UrlFetcher:
	'''Execute a request for a given URL and fetches the HTML soup.'''

	def __init__(self, url):
		'''When initialized register the URL, send the request, and fetch the soup object.'''
		self.url = url
		self.request = self.dispatch_request()
		self.soup = self.fetch_html_soup()


	def dispatch_request(self):
		'''Send the HTTP request for the URL registered during initialization.'''
		return requests.get(self.url)


	def fetch_html_soup(self):
		'''Fetch the soup object for the contents of the request sent during initiaization.'''
		return BeautifulSoup(self.request.content, "html.parser")


	@property
	def metadata(self):
		'''Extract the metadata for URLs that list all the search results.
			Returns a tuple: (total papers found, number of pages)
		'''
		try:
			total = int(self.soup.find('span', {'class': 'portal_navigator_window_info'}).text.split('of')[1].strip().replace(',', ''))
			pages = int(ceil(total / 10))
			return total, pages
		except:
			raise ValueError('Metadata cannot be extracted for this URL: %s' % self.url)



# Register the list of people
class RegisterPeople:
	'''Prepare and store the list of people in the people.txt file.'''
	people = []


	def __init__(self, path='people.txt'):
		'''Register all the people from the file and prepare the list of links.'''
		self.register_people(path)


	def register_people(self, path):
		'''Store all the people from the .txt file as a working list.'''
		with open(path) as txt:
			self.people = [person.rstrip() for person in txt.readlines()]



# Register the links for the list of people
class RegisterLinksForPeople:
	'''Prepare and store the list of links for a given list of people.'''
	links = []


	def __init__(self, people):
		'''Prepare the list of links for the list of people provided.'''
		self.register_links(people)


	def register_links(self, list_people):
		'''Store all the links that will have requests sent for.'''
		for person in list_people:
			self.links.append(UrlBuilder(person).url)
