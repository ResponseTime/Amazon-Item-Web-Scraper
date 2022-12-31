import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from plyer import notification
load_dotenv()


class Base:
    def getPrices(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.name = self.soup.find_all(
            "span", {"class": "a-size-medium a-color-base a-text-normal"})
        if len(self.name) == 0:
            self.name = self.soup.find_all(
                "span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        self.price = self.soup.find_all("span", {"class": "a-price-whole"})
        self.p = []
        for i in self.price:
            self.p.append(int(i.text.replace(",", "_")))
        with open('prices.txt', 'w', encoding='utf-16') as prices:
            for i, j in zip(self.name, self.p):
                prices.writelines(i.text+"["+str(j)+"rs"+"\n")
        print("Put an * in front of the item you want to tag")
        os.system(r"prices.txt")

    def tagItem(self):
        self.items = []
        self.prices = []
        with open('prices.txt', 'r', encoding="utf-16") as pr:
            self.lines = pr.readlines()
            for i in self.lines:
                if i.startswith("*"):
                    self.items.append(i[1:i.index("[")])
                    self.prices.append(i[i.index("[")+1:i.index("rs")])
        with open("tagged.txt", "w", encoding="utf-16") as tag:
            for i, j in zip(self.items, self.prices):
                tag.writelines(i+"["+str(j)+"rs"+"\n")
        os.remove("prices.txt")

    def checkForAll(self):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.name = self.soup.find_all(
            "span", {"class": "a-size-medium a-color-base a-text-normal"})
        if len(self.name) == 0:
            self.name = self.soup.find_all(
                "span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        self.price = self.soup.find_all("span", {"class": "a-price-whole"})
        self.p = []
        for i in self.price:
            self.p.append(int(i.text.replace(",", "_")))

        with open("tagged.txt", "r", encoding="utf-16") as tag:
            self.items = tag.readlines()
            for i, j in zip(self.name, self.items):
                if i == j:
                    notification.notify(
                        title="Price Dropped",
                        message="The price of {} has dropped".format(
                            i.text),
                        timeout=5
                    )
                    print("Price dropped for {}".format(i.text))


if __name__ == "__main__":
    Scraper = Base()
    item = input("Enter the item you want to search: ")
    url = os.getenv("URL").format(item)
    Scraper.getPrices(url)
    Scraper.tagItem()
    Scraper.checkForAll()
