from wem.index.spec.iScraper import iScraper
import time, pickle, requests, random
from wem.index.fakeUserAgent import FakeUserAgent

class ctftimeScraper(iScraper):
    """
    CTF TIME Scrapper will scrape each pages and store data into a
    Document object.
    When the parsing is done, all the information will be saved in
    a pickle file.
    """

    def __init__(self):
        super().__init__()
        self._rootUrl = "https://ctftime.org/writeup/"
        self._urlList = []
        self._pickleFile = "ctftime_urls_" + str(int(time.time())) + ".p"
        self._fakeUserAgent = FakeUserAgent()

    def getUrlList(self):
        """
        Get list of url
        :return: list of Document
        """
        return self.createUrlList() if (len(self._urlList) == 0) else self._urlList

    def createUrlList(self):
        """
        Create a list of urls
        :return: name of the file
        """

        urls = []
        error = 0
        counter = 1

        while (error < 10):

            urlToTest = self._rootUrl + str(counter)

            try:
                r = requests.get(urlToTest, timeout=2.0, headers=self._fakeUserAgent.random_headers())

                if (r.status_code == 200):
                    error = 0
                    urls.append(urlToTest)
                    print(urlToTest)
                else:
                    error += 1
                counter += 1

            except requests.exceptions.Timeout:
                print("Timeout Error with :", urlToTest)
                time.sleep(3)

            time.sleep(random.random())

        # Save url list
        self._urlList = urls
        self.saveToPickle(self._urlList)

        print("List saved in : " + "/save/" + str(self._pickleFile))
        return "/save/" + str(self._pickleFile)

    def saveToPickle(self, urls):
        """
        Save URLs in a pickle file
        :return: filename of the pickle
        """
        self._urlList = urls
        pickle.dump(self._urlList, open("/save/" + self._pickleFile, "wb"))
        return "/save/" + self._pickleFile

    def openPickle(self, filename):
        """
        Open a specific pickle file
        :param filename: file name
        :return: List of URLs
        """
        self._urlList = pickle.load(open(filename, "rb"))
        return self._urlList
