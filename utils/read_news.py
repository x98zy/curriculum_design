# coding=utf8
import sys
import os

def read_news():
    current_path = os.getcwd() + u'/爬取的文章/'
    files = os.listdir(current_path)
    res=[]
    for file in files:
        current_content = {}
        with open(current_path + file, "r",encoding="GBK") as f:
            try:
                title = f.readline().strip("\n")
                current_content["title"] = title
                date = f.readline().strip("\n")
                current_content["date"] = date
                url = f.readline().strip("\n")
                current_content["url"] = url
                res.append(current_content)
            except Exception as e:
                pass
    return res

