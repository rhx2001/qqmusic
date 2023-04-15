import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql.connector


cnx = mysql.connector.connect(
    user="QQmusic", password="dyz123", host="43.142.31.98", database="QQmusic"
)

# cnx = mysql.connector.connect(user='root', password='wpc123456',
#                               host='localhost', database='QQMusic')
cursor = cnx.cursor()

index = [62, 26, 27, 4]
name = ["飙升榜", "热歌榜", "新歌榜", "流行指数榜"]
base_url = "https://y.qq.com/n/ryqq/toplist/{}"
headerList = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400",
]
header = {"user-agent": random.choice(headerList)}

for i, idx in enumerate(index):
    list_name = name[i]
    print("--------------------开始爬取{}数据--------------------".format(list_name))
    url = base_url.format(idx, headers=header)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # 爬取所有歌曲
    for j, li in enumerate(soup.find("ul", class_="songlist__list").find_all("li")):
        if j < 3:
            rank = li.find("div", class_="songlist__number songlist__number--top").text
        else:
            rank = li.find("div", class_="songlist__number").text

        rank_ration = (
            "-" + li.find("div", class_="songlist__rank").text
            if li.find("div", class_="icon_rank_down")
            else li.find("div", class_="songlist__rank").text
        )

        song_name = li.find("span", class_="songlist__songname_txt").find_all("a")[-1][
            "title"
        ]

        singers = "/".join(
            [singer.text for singer in li.find_all("a", class_="playlist__author")]
        )

        song_time = li.find("div", class_="songlist__time").text

        # 进一步爬取歌曲信息
        time.sleep(0.5)

        song_url = "https://y.qq.com" + li.find_all("a", title=song_name)[-1].get(
            "href"
        )

        song_response = requests.get(song_url, headers=header)
        song_soup = BeautifulSoup(song_response.content, "html.parser")

        info_list = "+".join(
            [item.text for item in song_soup.find_all("li") if ("：" in item.text)]
        )  # 添加if解决该处class会改变的问题

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent={}".format(random.choice(headerList)))

        service = Service(r"F:\QQ缓存\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(song_url)

        for _ in range(20):
            try:
                driver.execute_script("window.scrollBy(0, 2000);")
                time.sleep(0.5)
            except:
                break
        time.sleep(3)

        comment_num = driver.find_elements(
            By.XPATH, "//span[@class='c_tx_thin part__tit_desc']"
        )[0].text

        img_url = driver.find_elements(By.XPATH, "//img[@class='data__photo']")[
            0
        ].get_attribute("src")

        try:
            cursor.execute(
                "INSERT INTO songs ("
                "list_name, `rank`, song_name, rank_ration, singer, song_time, img_url, info_list, song_url, comment_num)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    list_name,
                    rank,
                    song_name,
                    rank_ration,
                    singers,
                    song_time,
                    img_url,
                    info_list,
                    song_url,
                    comment_num,
                ),
            )
        except mysql.connector.errors.IntegrityError:
            cursor.execute(
                "UPDATE songs SET "
                "song_name=%s, rank_ration=%s, singer=%s, song_time=%s, "
                "img_url=%s, info_list=%s, song_url=%s, comment_num=%s "
                "WHERE list_name=%s AND `rank`=%s",
                (
                    song_name,
                    rank_ration,
                    singers,
                    song_time,
                    img_url,
                    info_list,
                    song_url,
                    comment_num,
                    list_name,
                    rank,
                ),
            )
            print("\n更新数据:\t榜单:{}\t排名:{}\t歌曲:{}".format(list_name, rank, song_name))

        except mysql.connector.errors.DataError:
            print("榜单:{}\t歌曲:{}".format(list_name, song_name))
            print("\n检查以下数据格式是否规范:")
        finally:
            cnx.commit()

        for i, item in enumerate(
            driver.find_elements(
                By.XPATH, "//li[@class='comment__list_item c_b_normal']"
            )
        ):

            reviewer_name = item.find_elements(By.XPATH, ".//a[@class='c_tx_thin']")[
                0
            ].text

            TimeAndAddress = item.find_elements(
                By.XPATH, ".//div[@class='comment__date c_tx_thin']"
            )[0].text.split()
            review_time = TimeAndAddress[0] + TimeAndAddress[1]
            review_prov = TimeAndAddress[-1][-2:]
            review = item.find_elements(By.XPATH, ".//p[@class='comment__text ']/span")[
                0
            ].text
            zan = item.find_elements(By.XPATH, ".//a[@class='comment__zan ']")[0].text

            try:
                cursor.execute(
                    "INSERT INTO comments ("
                    "reviewer_name, review_time, song_name, review_prov, zan, review) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (reviewer_name, review_time, song_name, review_prov, zan, review),
                )
            except mysql.connector.errors.IntegrityError:
                cursor.execute(
                    "UPDATE comments SET "
                    "zan=%s "
                    "WHERE reviewer_name=%s AND review_time=%s",
                    (zan, reviewer_name, review_time),
                )
            except mysql.connector.errors.DataError:
                print("\n检查以下数据格式是否规范:")
                print("歌曲:{}\t评论:{}".format(song_name, review))
            finally:
                cnx.commit()

        print("榜单:{}\t歌曲:{}\t爬取完成".format(list_name, song_name))
        driver.quit()
