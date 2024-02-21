import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from time import sleep
import urllib3

from keep_alive import keep_alive


urllib3.disable_warnings()

TELEBOT_TOKEN = "7179610090:AAE0uIGodQ-_ZeXnCkkHBe7Db7o4QHvBzI0"
GROUP_ID = "sguethobo"
URL = "https://uet.vnu.edu.vn/category/sinh-vien/hoc-phi-hoc-bong/feed"


client = MongoClient("mongodb+srv://pknstudio2704:nguyenitdev2704@cluster1.oglll5m.mongodb.net/?retryWrites=true&w=majority")

db = client["UETHumanOfSGUET"]
news_collection = db["humans"]


def get_news():
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    item = soup.find("h3")
    title = item.a.get("title")
    url = item.a.get("href")
    new = {"title": title, "url": url}
    return new


def send_news():
    data = get_news()
    check_news = news_collection.find_one(data)
    if not check_news:
        result = news_collection.delete_many({})
        news_collection.insert_one(data)
        message = data["url"]
        telegram_api_url = f"https://api.telegram.org/bot{TELEBOT_TOKEN}/sendMessage?chat_id=@{GROUP_ID}&text={message}"
        update = requests.get(telegram_api_url)


keep_alive()
while True:
  sleep(40)
  send_news()

