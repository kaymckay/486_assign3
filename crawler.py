from bs4 import BeautifulSoup
import requests
import sys
import os

URLS = set()
frontier = []
edges = []

def clean(path):
	dom1 = "eecs.umich"
	dom2 = "eecs.engin.umich"
	dom3 = "ece.engin.umich"
	dom4 = "cse.engin.umich"
	if dom1 in path or dom2 in path or dom3 in path or dom4 in path:
		check = path.split('//')
		if len(check) > 1:
			check = check[1]
			if 'www.' in check:
				check = check.replace('www.','', 1)

			if not check.endswith('/'):
				check = check + '/'
			check = 'http://' + check


			#  so I don't add a pdf/doc to an edge
			if '.pdf/' in check or '.doc/' in check.lower():
				return

			return check
	return




def main(args):

	# Add first url
	with open(args[0], 'r') as f: 
		Lines = f.readlines()
		for line in Lines:
			# clean url
			line = clean(line)
			frontier.append(line)

	out_file = open("crawler.output", "w")		
	sys.stdout = out_file

	headers = {'user-agent': 'kdogbot'}
	while len(URLS) < int(args[1]):
		url = frontier.pop(0)

		# check for duplicates and cycles 
		if url not in URLS:
			try:
				result = requests.get(url, headers=headers)
				#  check for 200 and redirect isn't in URLS and url is html
				if result and "text/html" in result.headers["content-type"] and result.url not in URLS:
					URLS.add(url)
					print(url)
					soup = BeautifulSoup(result.text, 'html.parser')
					for link in soup.find_all('a'):
						path = link.get('href')
						if path:

							# attempt to make sure all absolute paths
							if path.startswith('/'):
								path = requests.compat.urljoin(url, path)
							
							# cleaning for check
							path = clean(path)

							if path and path not in URLS and path not in frontier and not path == url:
								frontier.append(path)
							
							if path:
								edges.append(url + " " + path)
								
			except:
				continue

	# edges
	out_file = open("edges.output", "w")		
	sys.stdout = out_file
	for edge in edges:
		print(edge)








if __name__ == '__main__':
    # run main
    # python crawler.py myseedURLs.txt 2000
    main(sys.argv[1:])


