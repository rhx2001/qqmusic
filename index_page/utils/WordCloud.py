import jieba
import os
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import pandas as pd
from collections import defaultdict
import cntext as ct
import json
import paddle
#jieba的载入
path = ".\static\dir\\"
a = os.listdir(path) #词频语料库的地址

for i in a:#载入词频语料库：让分词更正准，防止过多的歧义
    jieba.load_userdict(path + i)
paddle.enable_static()
jieba.enable_paddle() #使用paddle框架来分词:(BILSTM双向GRU)
#paddle百度的深度学习框架
def rancolor(word, font_size, position, orientation, font_path, random_state):
    a = ["#a56cc1", "#a6acec", "#ace7ef", "#cefff1"]
    return a[random.randint(0, len(a)-1)]
def create(comments, song_name):
    if not os.path.exists(f'.\\static\\wordcloud\\{song_name}\\{song_name}.png'):#用于判断词云是否存在，如果不存在就进行运算，如果存在就直接调用
        #目的是生成离线数据，优化用户访问体验，同时降低服务器负担。
        img = Image.open(r".\static\img\background3.png").convert('RGBA')#img词云形状图片
        fontpath = r".\static\Font\STXINGKA.ttf"#词云字体
        backgroud_image = plt.imread(r".\static\img\colormap.jpg")
        stopword=["啊","我","一","的","了","好","是","啊啊啊","你","想","听","人","也","就","都","会","后","在"]#停止词，不让词云显示
        background = Image.new('RGBA', img.size, (255, 255, 255, 0))
        img = Image.alpha_composite(background, img)
        img_array = np.array(img)

        wc = WordCloud(#实例化词云
            background_color=None,
            mode='RGBA',
            max_words=100,
            width=800,
            height=1200,
            mask=img_array,  # 设置背景图片
            font_path=fontpath,
            stopwords=stopword,
            # color_func=rancolor,
        )
        path = ".\static\dir\\"
        a = os.listdir(path)
        cut = jieba.cut(comments)#使用jieba分词
        string = ' '.join(cut)
        wc.generate_from_text(string)  # 绘制图片
        # wc.recolor(color_func=ImageColorGenerator(backgroud_image))
        os.mkdir(rf'.\static\wordcloud\{song_name}')
        wc.to_file(rf'.\static\wordcloud\{song_name}\{song_name}.png')
    if not os.path.exists(rf'.\\static\\emotion\\{song_name}'):
        os.mkdir(rf'.\\static\\emotion\\{song_name}')
        cut = jieba.cut(comments)
        string = ' '.join(cut)
        emo = ct.sentiment(text=string,
                     diction=ct.load_pkl_dict('DUTIR.pkl')['DUTIR'],
                     lang='chinese')#七个指标 喜怒哀乐惧好惊
        with open(f".\\static\\emotion\\{song_name}\\{song_name}.json",'w') as f:
            json.dump(emo, f)
        return json.dumps(emo)
    else:
        emo = json.load(open(f".\\static\\emotion\\{song_name}\\{song_name}.json", 'r'))
        return emo
if __name__=="__main__":
    create("我们虔诚，旋动齿轮，一生只为见一个人”双笙献唱的插曲《只你》真的太甜啦！与剧情适配度好高！长月烬明好好看！")