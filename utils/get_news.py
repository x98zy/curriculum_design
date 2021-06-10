import io
import os
import sys
import requests
from bs4 import BeautifulSoup


url="http://www.agricoop.net/"   #爬取中国农业科技推广网

def urlBS(url):
    resp=requests.get(url)
    html=resp.content.decode(resp.encoding)
    soup=BeautifulSoup(html,"lxml")
    return soup

def get_news(url):
    soup=urlBS(url)
    lis=soup.find("div",class_="layui-tab-item layui-show").find("div",class_="info_show").find("ul").find_all("li")

    path=os.getcwd()+u'/爬取的文章/'
    if not os.path.isdir(path):
        os.mkdir(path)
    for i in lis:
        newurl=i.find('a')['href']
        result=urlBS(url+newurl)
        title=result.find("div",class_="newsDetail").find("h3").get_text()
        date=result.find("div",class_="nD_label").find("ul").find("li").get_text()

        filename=path+title+".txt"

        try:
            new_file = open(filename, "w")  # 创建一个新文件
            new_file.write(title + '\n')  # 写入标题
            new_file.write(date + '\n')  # 写入日期
        except OSError as e:
            pass
        try:
            new_file.write(url+newurl)
        except Exception as e:
            pass



get_news(url)
