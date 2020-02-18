# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:12:11 2020

@author: Administrator
"""

import matplotlib.pyplot as plt
import tkinter as tk

from jieba import cut
from time import sleep
from snownlp import SnowNLP
from pandas import DataFrame
from bs4 import BeautifulSoup
from selenium import webdriver
from wordcloud import WordCloud
from collections import Counter

# 解決圖形的中文顯示問題
plt.rcParams['font.sans-serif'] = ['SimHei'] # 替換sans-serif字型
plt.rcParams['axes.unicode_minus'] = False   # 解決座標軸負數的負號顯示問題

def cupoyWebCrawler():

    url = str(url_.get())
    global articleSum
    articleSum = int(articleSum_.get())
    
    browser = webdriver.Chrome(executable_path='chromedriver')
    browser.get(url)
    sleep(5)

    count = 1
    global categorylist
    global titlelist
    global contentlist
    global hreflist
    categorylist = []
    titlelist = []
    contentlist = []
    hreflist = []
    while (count <= articleSum) :
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "html5lib")
    
        for artical in soup.find_all('div', class_ = "sc-eEieub sc-iuDHTM ibJqYc"):
        
            # 將文章標題、文章內容、文章種類、文章來源抓下來
            category = artical.find('div', class_ = "sc-gacfCG bPSpUf").text
            title = artical.find('h6', class_ = 'sc-erNlkL sc-ekulBa hDLssh').text
            content = artical.find('p', class_ = 'sc-FQuPU sc-ciodno bvnzOw').text
            href = artical.find("a").get('href')
        
            # 防止爬到重複的文章
            if title not in titlelist:
                # 將各資料存進list以供後續分析
                categorylist.append(category)
                titlelist.append(title)
                contentlist.append(content)
                hreflist.append(href)
                # count表文章爬到的數目
                count += 1
            # 停止條件，抓到500篇文章即終止程式
            if count == (articleSum + 1):
                break
    
        # 將網頁繼續向下滑
        sleep(0.7)
        browser.execute_script("window.scrollTo(0, 1000000);")
    browser.quit()
    
    show_text.insert('insert',"爬蟲結束, 爬文總數為 " + str(articleSum) + " , 爬文網址為 " + url)
    
def printTitle():
    show_text.insert('insert','\n\n')
    count = 1 
    for title in titlelist:
        show_text.insert('insert',str(count) + ' ' + title + '\n')
        count += 1
        
def printContent():
    show_text.insert('insert','\n\n')
    count = 1 
    for content in contentlist:
        try:
            show_text.insert('insert',str(count) + ' ' + content + '\n')
            count += 1
        except:
            show_text.insert('insert',str(count) + '無法顯示該新聞簡介內容' + '\n')
            count += 1
            continue

def printHref():
    show_text.insert('insert','\n\n')
    count = 1 
    for href in hreflist:
        try:
            show_text.insert('insert',str(count) + ' ' + href + '\n')
            count += 1
        except:
            show_text.insert('insert',str(count) + '無法顯示該新聞來源網址' + '\n')
            count += 1
            continue

def plotData():
    # 用Counter計算種類後排序顯示
    sourceDict = dict(Counter(categorylist))
    categoryDf = DataFrame(list(sourceDict.items()))
    
    # 繪出圓餅圖
    plt.figure(figsize=(11,11)) # 顯示圖框架大小
    #plt.title('新聞種類分布', fontsize = '25')
    labels = categoryDf[0]          # 製作圓餅圖的類別標籤
    size = categoryDf[1]            # 製作圓餅圖的數值來源
    patches,l_text,p_text = plt.pie(size, labels=labels, autopct = '%1.1f%%')
    # 調整字體
    for t in l_text:
        t.set_size(13)
    for t in p_text:
        t.set_size(13)
    plt.axis('equal')
    plt.show()
    
def plotCloudTitle():
    # 準備標題語料
    titleCorpus = ''
    for title in titlelist:
        titleCorpus += title 

    #停用詞設定
    with open('stopWords.txt', 'r') as f:
        stops = f.read().split('\n')

    # 對titleCorpus進行斷詞
    term_titleCorpus = []
    for word in cut(titleCorpus):
        if word not in stops:
            term_titleCorpus.append(word)
    titleCount = dict(Counter(term_titleCorpus))

    # 字體路徑設定
    font = "C:\\Windows\\Fonts\\simsun.ttc"

    # 標題文字雲繪圖
    title_wordcloud = WordCloud(background_color="white",font_path = font, collocations=False, width=1200, height=1200, margin=2)  
    title_wordcloud.generate_from_frequencies(frequencies = titleCount)
    plt.figure(figsize=(5,5))
    plt.title('新聞標題文字雲', fontsize = '18')
    plt.imshow(title_wordcloud,interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
def plotCloudContent():
    # 準備內容語料 
    contentCorpus = ''
    for content in contentlist:
        contentCorpus += content  

    #停用詞設定
    with open('stopWords.txt', 'r') as f:
        stops = f.read().split('\n')

    # 對contentCorpus進行斷詞
    term_contentCorpus = []
    for word in cut(contentCorpus):
        if word not in stops:
            term_contentCorpus.append(word)
    contentCount = dict(Counter(term_contentCorpus))

    # 字體路徑設定
    font = "C:\\Windows\\Fonts\\simsun.ttc"

    # 內容文字雲繪圖
    content_wordcloud = WordCloud(background_color="white",font_path = font, collocations=False, width=1200, height=1200, margin=2)  
    content_wordcloud.generate_from_frequencies(frequencies = contentCount)
    plt.figure(figsize=(5,5))
    plt.title('新聞簡介文字雲', fontsize = '18')
    plt.imshow(content_wordcloud,interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
def printEmotion():
    # 計算標題的情緒分數
    title_emotionScore = 0
    for title in titlelist:
        s = SnowNLP(title)
        title_emotionScore += s.sentiments
    show_text.insert('insert',"\n\n標題的情感分析平均分數 " + str(round(title_emotionScore / articleSum,3)) + '\n')

    # 計算文章內容的情緒分數
    content_emotionScore = 0
    for content in contentlist:
        try:
            ss = SnowNLP(content)
            content_emotionScore += ss.sentiments
        except:
            continue
            
    show_text.insert('insert',"簡介的情感分析平均分數 " + str(round(content_emotionScore / articleSum,3)) + '\n')        
    show_text.insert('insert','該分數表示文章為正面的機率為多少')
    
def deleteData():   
    show_text.delete("1.0",tk.END)
    
window = tk.Tk()
window.title('CUPOY 新聞爬蟲軟體')
window.geometry('1015x383')

# 以下為網址的輸入框
url_frame = tk.Frame(window)
url_frame.place(x = 10, y = 10)
url_label = tk.Label(url_frame, text = '爬蟲網址')
url_label.pack(side = tk.LEFT)
url_ = tk.Entry(url_frame, width = 9)
url_.pack()

# 以下為文章數目的輸入框
articleSum_frame = tk.Frame(window)
articleSum_frame.place(x = 10, y = 40)
articleSum_label = tk.Label(articleSum_frame, text = '欲爬數目')
articleSum_label.pack(side = tk.LEFT)
articleSum_ = tk.Entry(articleSum_frame, width = 9)
articleSum_.pack()

# 開始爬網頁的按鈕框
button_crawler = tk.Button(window, text = "開始爬網頁", command = cupoyWebCrawler)
button_crawler.place(x = 10, y = 70)

# 清除文字
button_clear = tk.Button(window, text = "清除右方方框的文字", command = deleteData)
button_clear.place(x = 10, y = 100)

# 顯示新聞資訊
button_title = tk.Button(window, text = "印出爬到的新聞標題", command = printTitle)
button_title.place(x = 10, y = 160)

# 顯示新聞簡介
button_content = tk.Button(window, text = "印出爬到的新聞簡介", command = printContent)
button_content.place(x = 10, y = 190)

# 顯示新聞網址
button_content = tk.Button(window, text = "印出爬到的新聞網址", command = printHref)
button_content.place(x = 10, y = 220)

# 繪製圖表
button_pie = tk.Button(window, text = "繪製種類統計圓餅圖", command = plotData)
button_pie.place(x = 10, y = 250)

# 繪製新聞標題文字雲
button_cloud_title = tk.Button(window, text = "繪製新聞標題文字雲", command = plotCloudTitle)
button_cloud_title.place(x = 10, y = 280)

# 繪製新聞簡介文字雲
button_cloud_content = tk.Button(window, text = "繪製新聞簡介文字雲", command = plotCloudContent)
button_cloud_content.place(x = 10, y = 310)

# 秀出情緒分析分數
button_emotion = tk.Button(window, text = "標題和簡介情緒分析", command = printEmotion)
button_emotion.place(x = 10, y = 340)

# 以下為 Show Text
show_text = tk.Text(window, height = 27, width = 120)
show_text.place(x = 150, y = 10)

window.mainloop()