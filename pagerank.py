#  Kayla McKay (kaymckay)
import sys
import os


inlinks = {}
outlinks = {}


def calcPageRank(URLs, url):

	d = 0.85
	N = len(URLs)

	val1 = (1 - d) / N

	val2 = 0
	for u in inlinks[url]:
		# print("url")
		# print(url)
		val2 += URLs[u] / len(outlinks[u])

	return val1 + (d * val2)




def main(args):

	URLs = {}
	thres = float(args[1])


	with open(args[0], 'r') as f1: 
		Lines = f1.readlines()
		for line in Lines:
			line = line.strip()
			URLs[line] = 0.25
			inlinks[line] = []
			outlinks[line] = []

	with open(args[2], 'r') as f2: 
		Lines = f2.readlines()
		for line in Lines:
			left, right = line.split(" ")
			left = left.strip()
			right = right.strip()

			if left in URLs and right in URLs and not left == right:
				if not left in inlinks[right]:
					inlinks[right].append(left)
				if not right in outlinks[left]:
					outlinks[left].append(right)


	while True:
		newRanks = {}
		maxDiff = 0
		for url in URLs:
			newRanks[url] = calcPageRank(URLs, url) 

			if maxDiff < (abs(URLs[url] - newRanks[url])):
				maxDiff = (abs(URLs[url] - newRanks[url]))


		# check threshold
		URLs = newRanks.copy()
		if maxDiff < thres:
			break


	# print output
	out_file = open("pagerank.output", "w")		
	sys.stdout = out_file
	URLs = sorted(URLs.items(), key=lambda x: x[1], reverse=True)
	for url in URLs:
		print(url[0] + " " + str(url[1]))



if __name__ == '__main__':
    # run main
    # python pagerank.py crawler.output 0.001 edges.output
    main(sys.argv[1:])

