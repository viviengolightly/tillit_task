import argparse
from src.crawler import Crawler

def main():
	parser = argparse.ArgumentParser(description="Usage: main.py --url url_to_crawl --num optional_num_of_workers")
	parser.add_argument("--url")
	parser.add_argument("--num")
	args = parser.parse_args()
	if args.url:
		if args.num:
			crawler = Crawler(args.url, args.num)
			crawler.process()
		else:
			crawler = Crawler(args.url)
			crawler.process()
	else:
		print("Url is required.")

if __name__ == "__main__":
    main()