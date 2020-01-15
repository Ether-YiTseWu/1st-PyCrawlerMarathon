import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    target_urls = [
        'https://www.ptt.cc/bbs/Gossiping/M.1559788476.A.074.html',
        'https://www.ptt.cc/bbs/Gossiping/M.1557928779.A.0C1.html'
    ]
    process = CrawlerProcess(get_project_settings())
    process.crawl('PTTCrawler', start_urls=target_urls, filename='test.json')
    process.start()

if __name__ == '__main__':
    main()
