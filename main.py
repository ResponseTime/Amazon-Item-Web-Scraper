import requests
from bs4 import BeautifulSoup
import os


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
            self.p.append(int(i.text.replace(",", "")))
        with open('prices.txt', 'w', encoding='utf-8') as prices:
            for i, j in zip(self.name, self.p):
                prices.writelines(i.text+" "+str(j)+"rs"+"\n")
        os.system(r"prices.txt")

    def tagItem(self, item, price):
        k = 0
        for i in self.name:
            if i.text == item:
                if self.p[k] < price:
                    print(f"The {item}'s price is less than your budget")
                    k += 1
                else:
                    print(f"The {item}'s price is more than your budget")


if __name__ == "__main__":
    Scraper = Base()
    item = input("Enter the item you want to search: ")
    url = f"https://www.amazon.in/s?k={item}&crid=2VMIAQAKD77AL&sprefix=%2Caps%2C229&ref=nb_sb_ss_recent_1_0_recent"
    Scraper.getPrices(url)
    Scraper.tagItem("2022 Apple MacBook Air Laptop with M2 chip: 34.46 cm (13.6-inch) Liquid Retina Display, 8GB RAM, 256GB SSD Storage, Backlit Keyboard, 1080p FaceTime HD Camera. Works with iPhone/iPad; Space Grey", 10000)
