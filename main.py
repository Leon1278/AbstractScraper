import requests
from bs4 import BeautifulSoup
import pandas as pd
from threading import Thread

# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
# class to screen the output from any library class against several keywords
# outputs an excel-file with all articles that are relevant after screening the abstracts
class Screener:

	def __init__(self):

		self.relevant_01 = {'Titles': [], 'Abstracts': []}
		self.relevant_02 = {'Titles': [], 'Abstracts': []}
		self.relevant_03 = {'Titles': [], 'Abstracts': []}
		self.relevant_04 = {'Titles': [], 'Abstracts': []}
		self.relevant_counter = 0

	def screen_abstract(self, abstract):

		points = 0

		keyword_01 = 'pet'
		keyword_02 = 'privacy enhancing'
		keyword_03 = 'privacy preserving'
		keyword_04 = 'smartphone'
		keyword_05 = 'sensor'

		if keyword_01 in abstract.lower():
			points += 1
		if keyword_02 in abstract.lower():
			points += 1
		if keyword_03 in abstract.lower():
			points += 1
		if keyword_04 in abstract.lower():
			points += 1
		if keyword_05 in abstract.lower():
			points += 1

		return points

	def screen(self, data_dict):

		for entry in data_dict:
			if self.screen_abstract(data_dict[entry]) == 1:
				self.relevant_01['Titles'].append(entry)
				self.relevant_01['Abstracts'].append(data_dict[entry])
				self.relevant_counter += 1
			if self.screen_abstract(data_dict[entry]) == 2:
				self.relevant_02['Titles'].append(entry)
				self.relevant_02['Abstracts'].append(data_dict[entry])
				self.relevant_counter += 1
			if self.screen_abstract(data_dict[entry]) == 3:
				self.relevant_03['Titles'].append(entry)
				self.relevant_03['Abstracts'].append(data_dict[entry])
				self.relevant_counter += 1
			if self.screen_abstract(data_dict[entry]) >= 4:
				self.relevant_04['Titles'].append(entry)
				self.relevant_04['Abstracts'].append(data_dict[entry])
				self.relevant_counter += 1

	def write_excel_01(self, file_name):

		df = pd.DataFrame(self.relevant_01)
		df.to_excel(f'C:\\Users\\Leon\\PycharmProjects\\web_scraper.py\\{file_name}.xlsx')

	def write_excel_02(self, file_name):

		df = pd.DataFrame(self.relevant_02)
		df.to_excel(f'C:\\Users\\Leon\\PycharmProjects\\web_scraper.py\\{file_name}.xlsx')

	def write_excel_03(self, file_name):

		df = pd.DataFrame(self.relevant_03)
		df.to_excel(f'C:\\Users\\Leon\\PycharmProjects\\web_scraper.py\\{file_name}.xlsx')

	def write_excel_04(self, file_name):

		df = pd.DataFrame(self.relevant_04)
		df.to_excel(f'C:\\Users\\Leon\\PycharmProjects\\web_scraper.py\\{file_name}.xlsx')


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
# Class to get all abstracts from results in the ACM Digital Library
class AcmSoup:

	def __init__(self, url_init):

		self.source = requests.get(url_init).text
		self.soup = BeautifulSoup(self.source, 'lxml')
		self.dois = list()
		self.data = {}

	# ACM
	def get_dois(self):

		for content in self.soup.find_all('div', class_='issue-item__content'):
			content_a = content.h5.span.a
			doi = content_a.get('href')
			self.dois.append(doi)

	def get_data(self):
		# ACM
		def get_abstract(source):

			abstract_div = source.find('div', class_='abstractSection')
			abstract_text = abstract_div.p.text

			return abstract_text

		# ACM
		def get_title(source):

			title_div = source.find('h1', class_='citation__title')
			title_text = title_div.text

			return title_text

		for doi in self.dois:
			url = 'https://dl.acm.org' + doi
			try:
				source_html = requests.get(url).text
				source_soup = BeautifulSoup(source_html, 'lxml')
				title = get_title(source_soup)
				abstract = get_abstract(source_soup)
				self.data.update({title: abstract})
			except:
				self.data.update({'None': 'None'})

		return self.data


# Class to get all abstracts from results in ScienceDirect
class ScienceDirectSoup:

	def __init__(self, url_init):

		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
		self.source = requests.get(url_init, headers=self.headers).text
		self.soup = BeautifulSoup(self.source, 'lxml')
		self.dois = list()
		self.data = {}

	# ScinceDirect
	def get_dois(self):

		for content in self.soup.find_all('div', class_='result-item-container'):
			content_a = content.h2.span.a
			doi = content_a.get('href')
			self.dois.append(doi)

	def get_data(self):
		# ScinceDirect
		def get_abstract(source):

			abstract_div = source.find('div', class_='author')
			abstract_text = abstract_div.find("div", {"id": lambda L: L and L.startswith('abs')}).text

			return abstract_text

		# ScinceDirect
		def get_title(source):

			title_div = source.find('span', class_='title-text')
			title_text = title_div.text

			return title_text

		for doi in self.dois:

			url = 'https://www.sciencedirect.com' + doi

			try:
				source_html = requests.get(url, headers=self.headers).text
				source_soup = BeautifulSoup(source_html, 'lxml')
				abstract = get_abstract(source_soup)
				title = get_title(source_soup)
				self.data.update({title: abstract})
			except:
				self.data.update({'None': 'None'})

		return self.data


# Class to get all abstracts from results in IEEE
class IEEESoup:

	def __init__(self, url_init):

		#self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
		self.source = requests.get(url_init).text
		self.soup = BeautifulSoup(self.source, 'lxml')
		self.dois = list()
		self.data = {}

	# IEEE
	def get_dois(self):

		for content in self.soup.find_all('h2'):
			content_a = content.h2.a
			doi = content_a.get('href')
			self.dois.append(doi)

	def get_data(self):
		# IEEE
		def get_abstract(source):

			abstract_div = source.find('div', class_='Abstracts')
			abstract_text = abstract_div.find("div", {"id": lambda L: L and L.startswith('abs')}).text

			return abstract_text

		# IEEE
		def get_title(source):

			title_div = source.find('span', class_='title-text')
			title_text = title_div.text

			return title_text

		for doi in self.dois:

			url = 'https://www.sciencedirect.com' + doi

			try:
				source_html = requests.get(url).text
				source_soup = BeautifulSoup(source_html, 'lxml')
				abstract = get_abstract(source_soup)
				title = get_title(source_soup)
				self.data.update({title: abstract})
			except:
				self.data.update({'None': 'None'})

		return self.data


# Class to get all abstracts from results in Springer
class SpringerSoup:

	def __init__(self, url_init):

		#self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
		self.source = requests.get(url_init).text
		self.soup = BeautifulSoup(self.source, 'lxml')
		self.dois = list()
		self.data = {}

	# Springer
	def get_dois(self):

		for content in self.soup.find_all('a', class_='title'):
			doi = content.get('href')
			self.dois.append(doi)

	def get_data(self):
		# Springer
		def get_abstract(source):

			abstract_div = source.find('section')
			abstract_text = abstract_div.p.text

			return abstract_text

		# Springer
		def get_title(source):

			title_div = source.find('h1', class_='ChapterTitle')
			if not title_div:
				title_div = source.find('h1', class_='c-article-title')
			title_text = title_div.text

			return title_text

		for doi in self.dois:

			url = 'https://link.springer.com' + doi

			try:
				source_html = requests.get(url).text
				source_soup = BeautifulSoup(source_html, 'lxml')
				abstract = get_abstract(source_soup)
				title = get_title(source_soup)
				self.data.update({title: abstract})
			except:
				self.data.update({'None': 'None'})

		return self.data


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
# function to check several sites of one library (class only screens one site)

def scan(name):

	page_size = 20
	screener = Screener()


	if name.lower() == 'acm':
		print('$$$$$$$$$$$$$$$$$$$$$$$ Scan Initialized (ACM) $$$$$$$$$$$$$$$$$$$$$$$')

		for page in range(page_size):
			try:
				soup = AcmSoup(f'https://dl.acm.org/action/doSearch?AllField=%28pet+OR+%22privacy+enhancing%22+OR+%22privacy+preserving%22%29+AND+smartphone+AND+sensor&startPage={page}&pageSize=50')
				soup.get_dois()
				data = soup.get_data()
				screener.screen(data)
				print(f'Aktuell gescannte Seite ({name}): ', page)
			except Exception as e:
				print(e)
				break

			if page % 10 == 0:
				print('Bisher als relevant eingestufte Artikel: ', screener.relevant_counter)
				screener.write_excel_01(f'{name}_output_01')
				screener.write_excel_02(f'{name}_output_02')
				screener.write_excel_03(f'{name}_output_03')
				screener.write_excel_04(f'{name}_output_04')

		screener.write_excel_01(f'{name}_output_01')
		screener.write_excel_02(f'{name}_output_02')
		screener.write_excel_03(f'{name}_output_03')
		screener.write_excel_04(f'{name}_output_04')

	elif name.lower() == 'sciencedirect':

		print('$$$$$$$$$$$$$$$$$$$$$$$ Scan Initialized (science) $$$$$$$$$$$$$$$$$$$$$$$')

		for page in range(page_size):
			try:
				soup = ScienceDirectSoup(f'https://www.sciencedirect.com/search?qs=%28pet%20OR%20%22privacy%20enhancing%22%20OR%20%22privacy%20preserving%22%29%20AND%20smartphone%20AND%20sensor&show=100&offset={str(page*100)}')
				soup.get_dois()
				data = soup.get_data()
				screener.screen(data)
				print(f'Aktuell gescannte Seite ({name}): ', page)
			except Exception as e:
				print(e)
				break

			if page % 10 == 0:
				print('Bisher als relevant eingestufte Artikel: ', screener.relevant_counter)
				screener.write_excel_01(f'{name}_output_01')
				screener.write_excel_02(f'{name}_output_02')
				screener.write_excel_03(f'{name}_output_03')
				screener.write_excel_04(f'{name}_output_04')

		screener.write_excel_01(f'{name}_output_01')
		screener.write_excel_02(f'{name}_output_02')
		screener.write_excel_03(f'{name}_output_03')
		screener.write_excel_04(f'{name}_output_04')

	elif name.lower() == 'ieee':
		pass
	elif name.lower() == 'springer':

		print('$$$$$$$$$$$$$$$$$$$$$$$ Scan Initialized (springer) $$$$$$$$$$$$$$$$$$$$$$$')

		for page in range(page_size):
			try:
				soup = SpringerSoup(f'https://link.springer.com/search/page/{page}?query=%28pet+OR+%22privacy+enhancing%22+OR+%22privacy+preserving%22%29+AND+smartphone+AND+sensor')
				soup.get_dois()
				data = soup.get_data()
				screener.screen(data)
				print(f'Aktuell gescannte Seite ({name}): ', page)
			except Exception as e:
				print(e)
				break

			if page % 10 == 0:
				print('Bisher als relevant eingestufte Artikel: ', screener.relevant_counter)
				screener.write_excel_01(f'{name}_output_01')
				screener.write_excel_02(f'{name}_output_02')
				screener.write_excel_03(f'{name}_output_03')
				screener.write_excel_04(f'{name}_output_04')

		screener.write_excel_01(f'{name}_output_01')
		screener.write_excel_02(f'{name}_output_02')
		screener.write_excel_03(f'{name}_output_03')
		screener.write_excel_04(f'{name}_output_04')

	else:
		print('Incorrect Database given!')


# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ MAIN §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
if __name__ == '__main__':
	acm = Thread(target=scan, args=('acm',))
	scienceDirect = Thread(target=scan, args=('sciencedirect',))
	springer = Thread(target=scan, args=('springer',))
	ieee = Thread(target=scan, args=('ieee',))
	acm.start()
	#scienceDirect.start()
	#springer.start()
	#ieee.start()
