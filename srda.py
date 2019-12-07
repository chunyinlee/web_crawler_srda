import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError 
import pandas as pd
import time
#for mac users 告訴電腦ssl加密是有效的
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 準備空的 DataFrame 抓取每個人力資源調查的網址存成df
df = pd.DataFrame(columns=["survey_name", "url", "data_id"])
page = 1
#目前有五頁，就先抓五頁
while page <= 5:
    url = requests.post(
        "https://srda.sinica.edu.tw/browsingbydatatype_result.php",
        headers = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language" : "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        },
        params = {
            "category" : "surveymethod",
            "type" : "4",
            "csid" : "30",
        },
        data = {
            "pno" : str(page)
        }
    )
    print("現在處理的頁碼", page)

    html = BeautifulSoup(url.text, "html.parser")

    for r in html.find_all("div", class_ = "search-resulr--info"):
        a = r.find("a")
        s = pd.Series([a.text, "https://srda.sinica.edu.tw/" + a["href"][2:], a["href"][27:]],
            index=["survey_name", "url", "data_id"])
        df = df.append(s, ignore_index=True)

    page += 1
#df.to_html("./url.html", index = False)

#進入每個資料庫
head = "https://srda.sinica.edu.tw/"
df2 = pd.DataFrame(columns=["資料使用說明_中", "問卷_中", "過錄編碼簿_中", "報告書_中"]) 
df3 = pd.DataFrame(columns=["資料使用說明_英", "問卷_中", "過錄編碼簿_英"])
df4 = pd.DataFrame(columns=["檔名", "url"])
for id in df['data_id']:
    url = requests.post(
        "https://srda.sinica.edu.tw/datasearch_detail.php",
        headers = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language" : "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        },
        params = {
            "id" : id
        }
    )
    html = BeautifulSoup(url.text, "html.parser")

    for con_c in html.find_all("div", class_ = "content"):
        for blocks in con_c.find_all("div", class_ = "block-1"):
            for l in  blocks.find_all("dl", class_ = "browser_detail_content_dl"):
                for a in l.find_all("a"):
                    if "freedownload" in a["href"]:
                        s4 = pd.Series([a.text, head + a["href"]],
                                        index = ["檔名", "url"])
                        df4 = df4.append(s4, ignore_index=True)
#print(df4)
df4.to_html("./MS_pdf_url.html", index = False)
