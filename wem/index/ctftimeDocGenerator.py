from wem.index.spec.iDocGenerator import iDocGenerator
from wem.index.ctftimeScraper import ctftimeScraper
from wem.index.document import Document
from wem.index.fakeUserAgent import FakeUserAgent

import requests, time, re
from lxml import etree
from bs4 import BeautifulSoup
import copy

class ctftimeDocGenerator(iDocGenerator):
    def __init__(self, scrapper):
        super().__init__()
        self._scrapper = scrapper
        self._documents = None
        self._fakeUserAgent = FakeUserAgent()
        self._deepMeta = ['title','description','keywords','og:title', 'og:description', 'twitter:title', 'twitter:description']

    def createDocumentTuple(self):
        """
        Parse each page and store the information in a Document object
        """

        urls = self._scrapper.getUrlList()
        docs = []


        for url in urls:
            max_retry = 0
            while max_retry < 3:
                # Get ctftime url content
                try:
                    r = requests.get(url, timeout=5.0, headers=self._fakeUserAgent.random_headers())
                    if (r.status_code == 200):
                        metas = self.getCTFTimeMeta(r)

                        while max_retry < 3:

                            # Get article url
                            try:
                                metaUrl = requests.get(metas['url'], timeout=5.0, headers=self._fakeUserAgent.random_headers())
                                doc = Document(int(url.split("/")[-1]), metaUrl.content, self.getWriteupMeta(metaUrl.content, metas))

                                print(doc.getId())
                                print(doc.getMeta())

                                max_retry = 3

                                docs.append(doc)

                            except requests.exceptions.Timeout:
                                print("Timeout Error with :", url)
                                time.sleep(1)
                                max_retry += 1
                                continue
                            except requests.exceptions.ConnectionError:
                                print("Max retries exceeded with :", url)
                                max_retry = 3
                                continue
                            break
                except requests.exceptions.Timeout:
                    print("Timeout Error with :", url)
                    time.sleep(1)
                    max_retry+=1
                    continue
                except requests.exceptions.ConnectionError:
                    print("Max retries exceeded with :", url)
                    max_retry = 3
                    continue
                break

        self._documents = docs
        print(self._documents)

    def getDocumentTuple(self):
        return self._documents

    def getCTFTimeMeta(self, urlToTest):
        """
        Get Meta information from the website
        :param urlToTest: website URL
        :return: Dictionnary of meta informations
        """
        metas = {}

        elements = {
            "title": "/html/body/div[@class='container']/div[@class='page-header'][1]/h2/text()",
            "author": "/html/body/div[@class='container']/div[@class='page-header'][1]/a/text()",
            "tag": "/html/body/div[@class='container']/div[@class='row'][1]/div[@class='span8']/p[1]/span[@class='label label-info']/text()",
            "event": "/html/body/ul[@class='breadcrumb']/li[3]/a/text()",
            "url": "/html/body/div[@class='container']/div[3]/div[@class='well']/a/@href",
        }

        tree = etree.HTML(urlToTest.text)

        for key, value in elements.items():
            metas[key] = tree.xpath(value)[0] if (len(tree.xpath(value)) != 0) else ""

        metas['url'] = urlToTest.url if (metas['url'] == "") else metas['url']

        return metas

    def getWriteupMeta(self, text, metas):

        soup = BeautifulSoup(text, "lxml")

        # Get page title
        title = soup.find('title')
        try:
            title = str(title.contents[0]) if title.content else ""
            metas['tag_title'] = title
        except:
            metas['tag_title'] = ""

        # Get meta tags
        for c in self._deepMeta:
            content = soup.find("meta", property=c)
            metas['meta_'+c] = content["content"] if content else ""

        return metas