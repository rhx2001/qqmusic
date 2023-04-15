from django.shortcuts import render
from index_page.models import Songs, Comments
from index_page.utils import WordCloud
import json
from collections import defaultdict
# Create your views here.
def index(requests, song_name, singer_name, list_name):
    info = {}
    lists = {}
    local_review = defaultdict(int)
    db = Songs.objects.filter(list_name=list_name)
    for j, i in enumerate(db):
        info[i.song_name] = {"number":j,
                    "singer": i.singer,
                   "list_name":list_name
                   }
        lists[j] = {
            'song_name':i.song_name,
            "singer": i.singer,
            "list_name": list_name
        }
    db = Songs.objects.filter(song_name=song_name, list_name=list_name)
    remark = Comments.objects.filter(song_name=song_name)
    str=""
    times = defaultdict(int)
    for i in remark:
        str += i.review
        times[i.review_time.split(":")[0][-2:]] += 1
        if not i.review_prov.isdigit():
            local_review[i.review_prov] += 1
    emo = WordCloud.create(str, song_name)
    print(emo)
    return render(requests, "index_page/index.html",
                  {'song_name': song_name,
                   'singer_name': singer_name,
                   'album_info': db.first().info_list,
                   'img_url': db.first().img_url,
                   'remark': [(i.review, i.reviewer_name) for i in remark],
                   'emotion': json.dumps(emo),
                   'song_url': db.first().song_url,
                   'times': json.dumps(times),
                   'song_list': json.dumps(info),
                   'change_list': lists,
                   'song_list2': info,
                   'review_num': json.dumps(local_review)
                   })


def frontpage(requests):
    names = ["飙升榜", "热歌榜", "新歌榜", "流行指数榜"]
    info = {}
    for name in names:
        db = Songs.objects.filter(list_name=name)
        info[name] = [i for i in db]
    print(info)
    return render(requests, "frontpage/frontpage.html", {"info": info,
                                                         "range": list(range(1,21))})
