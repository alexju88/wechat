# -*- coding: utf-8 -*-
#https://github.com/wenfengju/wechat
#Usage1:
#python wechat.py text "hello"
#Usage2:
#python wechat.py picture AI.jpg

import requests
import json
import urllib2
import ssl
import sys

#禁用SSL
ssl._create_default_https_context = ssl._create_unverified_context

ID="xxxxxxxxxx"
Secret="xxxxxxxxxxxxxxxx"

UserID = "userid" ##成员ID列表（消息接收者，多个接收者用'|'分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
PartyID= 2   ## 部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
AppID = 1000003  ##应用ID，默认是 企业小助手  企业应用的id，整型。可在应用的设置页面查看

def get_token():  ##获取TOKEN
    gurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(ID, Secret)
    r=requests.get(gurl)
    dict_result= (r.json())
    return dict_result['access_token']

def get_media_ID(path):  ##上传到临时素材  图片ID
    Gtoken = get_token()
    img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=image".format(Gtoken)
    files = {'image': open(path, 'rb')}
    r = requests.post(img_url, files=files)
    re = json.loads(r.text)
    return re['media_id']

def  send_text(text):  ##发送文字
    post_data = {}
    msg_content = {}
    msg_content['content'] = text  ## 消息内容，最长不超过2048个字节
    post_data['touser'] = UserID
    post_data['toparty'] = PartyID
    post_data['msgtype'] = 'text'
    post_data['agentid'] = AppID
    post_data['text'] = msg_content
    post_data['safe'] = '0'  #表示是否是保密消息，0表示否，1表示是，默认0
    Gtoken = get_token()
    purl1="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(Gtoken)
    json_post_data = json.dumps(post_data,False,False)
    #request_post = urllib.urlopen(purl,json_post_data.encode(encoding='UTF8'))
    request_post = urllib2.urlopen(purl1,json_post_data.encode(encoding='UTF8'))
    #request_post = request_post.decode('UTF-8')
    return request_post

def  send_tu(path):  ##发送图片
    img_id = get_media_ID(path)
    post_data1 = {}
    msg_content1 = {}
    msg_content1['media_id'] = img_id
    post_data1['touser'] = UserID
    post_data1['toparty'] = PartyID
    post_data1['msgtype'] = 'image'
    post_data1['agentid'] = AppID
    post_data1['image'] = msg_content1
    post_data1['safe'] = '0'
    Gtoken = get_token()
    purl2="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(Gtoken)
    json_post_data1 = json.dumps(post_data1,False,False)
    #request_post = urllib.urlopen(purl2,json_post_data1.encode(encoding='UTF8'))
    request_post = urllib2.urlopen(purl2,json_post_data1.encode(encoding='UTF8'))
    #request_post = request_post.decode('UTF-8')
    return request_post


#发送图片
type=sys.argv[1]
content=sys.argv[2]
if type == 'picture':
        send_tu(content)
        print('pic send ok!')
#发送消息
else:
        send_text(content)  ##文字内容
        print('msg send ok!')