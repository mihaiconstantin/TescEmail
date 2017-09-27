from helpers import RegisterPeople, RegisterLinksForPeople
from workers import AuthorDataWorker
from storage import StoreCsv


def run():
	'''Scraps the http://pure.uvt.nl database for the TESC authors contact info.'''

	# Determine who are the authors.
	register_people = RegisterPeople('people.txt')
	
	# Collect the links for all authors.
	register_links = RegisterLinksForPeople(register_people.people)

	# Collect the data for each author link.
	AuthorDataWorker.extract_all_author_data(register_links.links)

	# Save a .csv file with the results.
	storage = StoreCsv(AuthorDataWorker.all_authors, path = 'data')
	storage.save()


if __name__ == '__main__':
	run()