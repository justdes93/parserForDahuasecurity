import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

URL = "https://us.dahuasecurity.com/product-category/network-products/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
}
OUTPUT = "ouput2.xlsx"


def get_html(url, params=''):
    data = requests.get(url, params=params, headers=HEADERS)
    return data


def get_products(page):
    temp_url = URL + f"page/{page}/"
    html = get_html(temp_url).text
    soup = BeautifulSoup(html, "html.parser")

    products = soup.find_all("li", class_="product")

    data = []

    for product in products:
        img = product.find("img")
        link = img.get("data-nectar-img-src")

        title = product.find("h2", class_="woocommerce-loop-product__title").get_text()

        text = product.find("div", class_="product-meta").find('p').get_text()

        data.append({
            "img": link,
            "title": title,
            "text": text
        })
    return data


def format(data):
    result = {
        "img": [],
        "title": [],
        "text": []
    }

    for item in data:
        result["img"].append(item["img"])
        result["title"].append(item["title"])
        result["text"].append(item["text"])

    return result


def write_file(data):
    writer = pd.ExcelWriter(OUTPUT)
    parse_data = format(data)
    dataframe = pd.DataFrame(data=parse_data)
    dataframe.to_excel(writer, "list_1", index=False)

    writer._save()


def main():
    data = []
    for i in range(1, 10):
        data += get_products(i)

    write_file(data)


main()

