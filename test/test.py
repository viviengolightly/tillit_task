import unittest
from io import StringIO
from unittest.mock import patch
from src.crawler import Crawler
from bs4 import BeautifulSoup
import responses

class TestCrawler(unittest.TestCase):

    def test_get_res(self):

    	responses.add(**{
    		'method'         : responses.GET,
    		'url'            : 'http://example.com/api/123',
    		'body'           : '{"error": "reason"}',
    		'status'         : 404,
    		'content_type'   : 'text/html',
    	})

    	crawler = Crawler('http://example.com/api/123')
    	response = crawler.get_res('http://example.com/api/123')

    	self.assertEqual(404, response.status_code)

    def test_check_visited(self):
    	crawler = Crawler("http://test.com")
    	crawler.visited.add("http://test.com")
    	test_urls = ["http://test.com", "", "http://one.com", "http://test.com/"]
    	expexted_outputs = [True, False, False, False]
    	for i in range(len(test_urls)):
    		self.assertEqual(crawler.check_visited(test_urls[i]), expexted_outputs[i])

    def test_check_if_valid_url(self):
    	crawler = Crawler("http://test.com")
    	test_urls = ["http://test.com", "", "http://one.com", "http://test.com/", "1223", "abcd.de"]
    	expexted_outputs = [True, False, True, True, False, False]
    	for i in range(len(test_urls)):
    		self.assertEqual(crawler.check_if_valid_url(test_urls[i]), expexted_outputs[i])

    def test_is_internal_url(self):
    	crawler = Crawler("http://test.com")
    	test_childs = ["http://test.com/", "", "http://test.com/test1/test2", "https://test.com", "http://tests.com", "http://something.com", "http://test.com"]
    	expexted_outputs = [True, False, True, True, False, False, True]
    	for i in range(len(test_childs)):
    		self.assertEqual(crawler.is_internal_url(test_childs[i]), expexted_outputs[i])

    def test_iterate_urls(self):
    	node = 'http://test.com'

    	urls = '<a href="/pages/"></a><a href="/test/"></a><a href=""></a><a></a>'
    	soup = BeautifulSoup(urls, 'html.parser')
    	tags = soup.find_all('a')
    	
    	visited = set()
    	visited.add('http://test.com')

    	output = [('http://test.com','http://test.com/pages'), ('http://test.com','http://test.com/test')]

    	crawler = Crawler("http://test.com")
    	crawler.iterate_urls(tags, node)

    	self.assertEqual(crawler.visited, visited)
    	self.assertEqual(crawler.output_list, output)

    def test_print_output(self):
    	crawler = Crawler("http://test.com")
    	crawler.output_list = [("http://test.com", "http://test.com")]
    	with patch('sys.stdout', new = StringIO()) as fake_out:
    		crawler.print_output()
    		self.assertEqual(fake_out.getvalue(), "# 0\nSrc:  http://test.com  Dest:  http://test.com\n\n\n")
        

if __name__ == '__main__':
    unittest.main()