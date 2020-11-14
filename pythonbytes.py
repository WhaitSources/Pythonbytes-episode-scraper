import requests
import os
from selectolax.parser import HTMLParser
import concurrent.futures

base_url = 'https://pythonbytes.fm'
headers = {}
output_dir = 'MP3s/'

if not os.path.isdir(output_dir):
	os.mkdir(output_dir)

def scrape_podcast(link):
	print('[*] Scraping', base_url + link)
	selectolax = HTMLParser(requests.get(base_url + link, headers=headers).content)
	dl_link = base_url + str(selectolax.css_first('a.btn.btn-default.subscribe-btn.btn-sm').attrs['href'])
	file_name = dl_link.split('/')[-1]
	print('[+] Downloading', file_name)
	with open(output_dir + file_name, 'wb') as file:
		file.write(requests.get(dl_link, headers=headers).content)

if __name__ == '__main__':
	with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		executor.map(scrape_podcast, [node.attrs['href'] for node in HTMLParser(requests.get(base_url+ '/episodes/all', headers=headers).content).css('tr > :nth-child(3) > a')])