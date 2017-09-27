from threading import Thread
from queue import Queue
from time import time
from helpers import UrlFetcher


# Author data.
class AuthorDataWorker(Thread):
	'''Extracts the data for the TESC authors.'''

	all_authors = []
	all_fails = []


	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue


	def run(self):
		while True:
			# Get the work (i.e., the author URL) from the queue.
			author_url = self.queue.get()
			# Extract the author data.
			AuthorDataWorker.extract_author_data(UrlFetcher(author_url))
			# Mark job as completed.
			self.queue.task_done()


	@classmethod
	def extract_author_data(cls, url_fetcher):
		"""Extracts data for a author.
		Args:
		    url_fetcher (UrlFetcher): UrlFetcher object.
		"""
		# Get the HTML soup.
		soup = url_fetcher.soup

		# Determine if there are multiple authors with the same name.
		author_count = url_fetcher.metadata[0]

		if author_count > 0:
			# The context: the first author in the results of a search page.
			ctx_author = soup.find('ol', class_='portal_list').find('li', class_='portal_list_item')


			# The storage per author where the data is temporary placed. 
			author_data = {'departments': {}}


			# Search URL.
			author_data['search_url'] = url_fetcher.url


			# Name.
			try:
				author_data['name'] = ctx_author.find('h2', class_='title').text
			except:
				author_data['name'] = 'Error: name.'
			

			# Author URL.
			try:
				author_data['author_url'] = ctx_author.find('h2', class_='title').find('a', rel='Person')['href']
			except:
				author_data['author_url'] = 'Error: author URL.'


			# Email.
			try:
				author_data['email'] = ctx_author.find('ul', class_='email').find('li', class_='email').text
			except:
				author_data['email'] = 'Error: email.'


			# Departments.
			try:
				departments = ctx_author.find('ul', class_='organisations').find_all('li')
				for department in departments:
					if department.find('a') is not None:
						if department.find('span', class_='minor') is not None:
							author_data['departments'][department.find('a').text] = department.find('span', class_='minor').text[3:]
						else:
							author_data['departments'][department.find('a').text] = 'n.a.'
			except:
				author_data['departments'] = 'Error: departments.'


			# Append the author data if it we only found one matching result.
			cls.all_authors.append(author_data)
			print('\t- Succeeded for author: %s' % str(author_data['name']))
		else:
			cls.all_fails.append(url_fetcher.url)
			print('\t- Failed for link: %s' % str(url_fetcher.url))


	@staticmethod
	def extract_all_author_data(all_links):
		"""Extract the data for all authors in the list in a multi-threaded fashion.
		Args:
		    all_links (list): A list of URLs.
		"""
		time_start = time()

		queue = Queue()

		print('\nStarting extracting the author data...')
		for thread in range(20):
			worker = AuthorDataWorker(queue)
			worker.daemon = True
			worker.start()

		for author_link in all_links:
			queue.put(author_link)

		queue.join()

		print('Extraction completed...')
		print('\nFound: %s authors.' % len(AuthorDataWorker.all_authors))
		print('\nFailed for %s authors.' % len(AuthorDataWorker.all_fails))
		print('\nTook: %s seconds.' % str(time() - time_start))
		print('\nDone with all.')
