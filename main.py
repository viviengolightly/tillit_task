from src.crawler import Crawler

def main():
	url = "https://scrapethissite.com"
	crawler = Crawler(url)
	crawler.process()
	
if __name__ == "__main__":
    main()