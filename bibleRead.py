#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class bibleRead:
    def __init__(self, whichTranslation, whichBook, chapterNumber):
        self.translations = {'개역개정':'B_GAE', '개역한글':'B_RHV', '공동번역':'B_COGNEW',
                             '새번역':'B_SAENEW', '현대인':'B_HDB', 'NIV':'B_NIV',
                             'KJV':'B_KJV', 'NASB':'B_NASB'}
        self.bibleTranslation = self.translations[whichTranslation]
        self.url = f'http://www.holybible.or.kr/{self.bibleTranslation}/'

        self.getRequest1 = requests.get(self.url)
        self.getRequest1.encoding = None  # None 으로 설정
        # r.encoding='euc-kr'  # 한글 인코딩
        self.soup1 = BeautifulSoup(self.getRequest1.text, 'lxml')
        self.search = self.soup1.find_all('a', href=True)

        self.bookhref = self.bookToRead(whichBook)
        self.bookurl = f'http://www.holybible.or.kr/{self.bookhref}'
        self.whichChapter(chapterNumber)
        self.getRequest2 = requests.get(self.bookurl)
        self.getRequest2.encoding = None
        # r.encoding='euc-kr'
        self.soup2 = BeautifulSoup(self.getRequest2.text, 'lxml')
        self.phrases = []

    def bookToRead(self, whichBook):
        for i in range(0, len(self.search)):
            if self.search[i].text.find(whichBook) != -1:
                return self.search[i]['href']
        return 'Invalid book'

    def whichChapter(self, chapterNumber):
        chapterIndex = self.bookurl.index('CN=')
        chapterIndex += 3;
        l = list(self.bookurl)
        l[chapterIndex] = chapterNumber
        self.bookurl = "".join(l)

    def whichPhrases(self, start, end):
        phrase = self.soup2.find_all('li')
        self.phrases.clear()
        if end == -1:
            self.phrases.append(f"{start}. {phrase[start - 1].text}")
        else:
            for i in range(start - 1, end):
                self.phrases.append(f"{i + 1}. {phrase[i].text}")

    def displayPhrases(self):
        return self.phrases
        #s = "\n".join(self.phrases)
        #return s