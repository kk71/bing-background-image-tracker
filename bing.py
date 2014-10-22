#!/usr/bin/env python3
#coding=utf-8
'''
bing.com background image tracker
lovely written to Kingky:)
'''

import os
import re
from urllib import request
from datetime import datetime

try:
    import simplejson as json
except:
    import json


def get_image_and_text():
    '''
    fetch the main page of cn.bing.com and parse it with regexp
    :return:
    '''
    try:
        req=request.Request(
            url="http://cn.bing.com/",
            headers={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"deflate,sdch",
                "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                "Cache-Control":"max-age=0",
                "Connection":"keep-alive",
                "DNT":1,
                "Host":"cn.bing.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"
        })
        pageText=request.urlopen(req).read().decode()
    except:
        print("读取必应首页出错，请检查网络连接。")
        return False

    # get image url
    try:
        imageUrl=re.compile(r"g_img=\{url:'(.*?)',id").findall(pageText)[0]
        # if the background is a animation(sometimes an mp4 file)
        # the url may look like "//..."
        if imageUrl[:2]=="//":
           imageUrl="http:"+imageUrl
        # otherwise if the shortened url isn't started with // or http
        # add default header
        if not imageUrl[:4]=="http":
            imageUrl="http://cn.bing.com"+imageUrl
        imageContent=request.urlopen(imageUrl).read()
    except:
        print("下载图片时出错。")
        return False

    # write image file
    imageFile=open("image.jpg","bw")
    imageFile.write(imageContent)
    imageFile.close()

    # get text
    text=eval(re.compile(r'''var g_hot=(.*?);''').findall(pageText)[0])

    # return text result
    result=""
    for num in text:
        result+="".join(text[num].values())+"\r\n" # \r\n for windows line-ending.
    return result


def get_descriptions():
    '''
    get descriptions to today's story.
    :return:
    '''
    pageText=request.urlopen("http://cn.bing.com/cnhpm").read().decode()
    today_photo_story=re.compile(r'class="sc_light" id="sh_cp" title="(.*?)"').findall(pageText)[0]
    photo_description=re.compile(r'<h3>今日图片故事</h3><a href="(.*?)" target="_blank" h="(.*?)">(.*?)</a>').findall(pageText)[0][2]
    return "\r\n".join(["今日图片故事："+today_photo_story,photo_description])


if __name__=="__main__":
    # create the directory for today
    dtStr=datetime.now().strftime("%Y-%m-%d")
    try:os.mkdir(dtStr)
    except:pass
    os.chdir(dtStr)

    # get text and image
    description=get_descriptions()
    if not description:description=""
    text=get_image_and_text()
    if not text:exit()

    # write text and description into one txt file
    textFile=open("text.txt","w",encoding="utf-8")
    textFile.write(description)
    textFile.write("\r\n"*2)
    textFile.write(text)
    textFile.close()
    input("结束，回车退出。")
