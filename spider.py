from urllib.request import *
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    def __init__(self, base_url):
        self.base_url = base_url
        self.domain_name = get_domain_name(base_url)
        self.social_links = {'twitter':'', 'facebook':'', 'instagram':'', 'pinterest':'', 'youtube':''}
        self.queue = set()
        self.queue.add(base_url)
        self.crawled = set()

    def socialLinks(self):
        return self.social_links

    def crawl_page(self, thread_name):
        while True:
            if(len(self.crawled) == 50):
                break
            if(len(self.queue) == 0):
                break
            page_url = self.queue.pop()
            if page_url not in self.crawled:
                links = self.gather_links(page_url)
                self.add_links_to_queue(links)
                self.crawled.add(page_url)
                if(self.findSocialLinks(links)):
                    self.queue = set()
                    self.crawled = set()
                    break

    def gather_links(self, page_url):
        html_string = ''
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            req = Request(url=page_url, headers=headers)
            response = urlopen(req)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(self.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print ('EXCEPTION has BEEN REACHED')
            print(str(e))
            return set()
        links = finder.page_links()
        return links

    # Saves queue data to project files
    def add_links_to_queue(self, links):
        for url in links:
            if (url in self.queue) or (url in self.crawled):
                continue
            if self.domain_name != get_domain_name(url):
                continue
            self.queue.add(url)

    def findSocialLinks(self, links):
        content = links
        twitter = min([s for s in content if'twitter' in s], key=len, default='')
        facebook = min([s for s in content if'facebook' in s], key=len, default='')
        instagram = min([s for s in content if'instagram' in s], key=len, default='')
        pinterest = min([s for s in content if'pinterest' in s], key=len, default='')
        youtube = min([s for s in content if'youtube.com/channel' in s], key=len, default='')

        socialLinksDict = {'twitter':twitter, 'facebook': facebook, 'instagram':instagram, 'pinterest':pinterest, 'youtube':youtube}
        completed = True

        for key, value in socialLinksDict.items():
            if self.social_links[key] == '' and value == '':
                completed = False
            else:
                self.social_links[key] = value

        return completed
