import csv
from datetime import datetime


class StoreCsv:
	'''Write the results for the extracted links (i.e., the TESC KPI).'''

	def __init__(self, all_authors, path=''):
		"""Write all author data to a .csv file.
		Args:
		    all_authors (list): A list of dictionaries (i.e., each dictionary holds the data for a author).
		    path (str, optional): The path where to write the .csv file.
		"""
		self.date = datetime.today()
		self.data = [['#', 'Name', 'Email', 'Departments', 'Link']]
		self.path = path
		self.append_content(all_authors)


	def append_content(self, all_authors):
		for i, author in enumerate(all_authors):
			for key, value in author.items():
				if key == 'departments':
					department_string = ''
					for department, position in author[key].items():
						department_string = '%s %s (%s), ' % (department_string, department, position)
					author[key] = department_string
			self.data.append([str(i), author['name'], author['email'], author['departments'], author['author_url']])


	def save(self, filename=None):
		"""Commit the changes and save the author data to the file.
		Args:
		    filename (str, optional): The name of the .csv file to be written. Defaults to 'TESC_KPI_dd-mm-yyyy.csv'.
		"""
		if filename is None:
			filename='%s/TESC_AUTHORS_%s-%s-%s.csv' % (self.path, self.date.year, self.date.month, self.date.day)

		self.errors = []

		# with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
		with open(filename, 'w', newline='', encoding='UTF-8') as file:
			csv_writer = csv.writer(file)
			for line in self.data:
				try:
					csv_writer.writerow(line)
				except:
					self.errors.append(line)

		if not self.errors:
			print('\nFile "%s" has been written successfully.' % filename)
		else:
			print('\nFile "%s" has been written, but %s lines raised errors. Handle them manually.' % (filename, len(self.errors)))
