import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import redis
import time

class SimpleCrawler:
    def __init__(self, redis_host='10.0.1.100', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.session = None

    async def fetch(self, url):
        # Fetch a single URL
        try: 
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def extract_links(self, html, base_url):
        # Extract all links from HTML
        soup = BeautifulSoup(html, 'lxml')  # lxml is the html parser
        links = []

        for link in soup.find_all('a', href=True):  # a is the anchor tag, clickable link
            url = urljoin(base_url, link['href'])
            # only keep http/https links
            if urlparse(url).scheme in ['http', 'https']:
                links.append(url)

        return links

    def extract_text(self, html):
        # Extract main text component
        soup = BeautifulSoup(html, 'lxml')

        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    async def crawl_url(self, url):
        # Crawl a single URL
        print(f"Crawling: {url}")

        # Check if already seen
        if self.redis_client.sismember('seen_urls', url):
            print(f"  Already seen: {url}")
            return
        
        # Mark as seen
        self.redis_client.sadd('seen_urls', url)

        # Fetch page
        html = await self.fetch(url)
        if not html: 
            return

        # Extract links and add to frontier
        links = self.extract_links(html, url)
        for link in links:
            if not self.redis_client.sismember('seen_urls', link):
                self.redis_client.lpush('url_frontier', link)

        # Extract text content
        text = self.extract_text(html)

        # As of now just print the stats about the html
        print(f"  Found {len(links)} links, extracted {len(text)} chars of text")

        # Store document url and text length for now
        doc_id = self.redis_client.incr('doc_counter')
        self.redis_client.hset(f'doc:{doc_id}', mapping={
            'url': url,
            'text_length': len(text),
            'crawled_at': time.time()
            })

        return doc_id

    async def run(self, seed_urls, max_pages=100):
        # Main crawler loop

        # Add seed URLs to frontier
        for url in seed_urls:
            self.redis_client.lpush('url_frontier', url)

        pages_crawled = 0

        async with aiohttp.ClientSession() as session:
            self.session = session
            
            while pages_crawled < max_pages:
                # Get URL from frontier
                url = self.redis_client.rpop('url_frontier')

                if not url:
                    print("Frontier empty")
                    break

                await self.crawl_url(url)
                pages_crawled += 1

                # small delay
                await asyncio.sleep(.5)

        print(f"\nCrawled {pages_crawled} pages")
        print(f"URLs in frontier: {self.redis_client.llen('url_frontier')}")
        print(f"Unique URLs seen: {self.redis_client.scard('seen_urls')}")


if __name__ == '__main__':
    crawler = SimpleCrawler()

    seed_urls = [
            'https://lite.cnn.com/'
             ]

    asyncio.run(crawler.run(seed_urls, max_pages = 20))




































