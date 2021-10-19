from bs4 import BeautifulSoup
import gevent 
import gevent.queue
import requests
from urllib.parse import urlparse, urljoin
import urllib.request

class Crawler:
	def __init__(self, url, workers = 10):
		self.url = url
		self.workers = workers
		self.output_list = []
		self.q = gevent.queue.JoinableQueue()
		self.visited = set()

	def get_res(self, url):
		response = requests.get(url)
		return response

	def get_urls(self, url):
		response  = self.get_res(url)
		soup = BeautifulSoup(response.content, "html.parser")
		return soup

	def check_visited(self, url):
		return url in self.visited

	def check_if_valid_url(self, url):
		parsed = urlparse(url)
		return bool(parsed.netloc) and bool(parsed.scheme)

	def is_internal_url(self, child_url):
		domain = urlparse(self.url).netloc
		return domain in child_url

	def iterate_nodes(self, pid):
		for node in iter(self.q.get, None):
			urls = self.get_urls(node).find_all('a')
			self.iterate_urls(urls, node)
			self.q.task_done()
			gevent.sleep(0)
	
	def iterate_urls(self, urls_list, node):
		for url in urls_list:
			anchor = url.attrs.get("href")
			if anchor is None or anchor == "":
				continue
			else:
				out_url = urljoin(node, anchor)
				parsed_href = urlparse(out_url)
				out_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
				if out_url[-1] == '/':
					out_url = out_url[:-1]
				if (node, out_url) not in self.output_list:
					self.output_list.append((node, out_url))
				if self.check_if_valid_url(out_url):
					if self.is_internal_url(out_url) and not self.check_visited(out_url):
						self.q.put(out_url)
		self.visited.add(node)

	def print_output(self):
		for i in range(len(self.output_list)):
			print("#", i)
			print("Src: ", self.output_list[i][0], " Dest: ", self.output_list[i][1])
			print("\n")

	def process(self):
		if self.check_if_valid_url(self.url):
			self.q.put(self.url)
			for i in range(self.workers):
				gevent.spawn(self.iterate_nodes, i)
			self.q.join()
			self.print_output()
		else:
			print("Invalid URL\n")






