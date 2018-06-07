#coding:utf-8
import requests
import urllib
import ssl
import json
import time
import csv,codecs
if hasattr(ssl, '_create_unverified_context'): #SSL设置
           ssl._create_default_https_context = ssl._create_unverified_context

#初始参数
ID="wx877b960ce51532f5" #企业ID
SECRET="g76sFMV06eOm_FuXlZKjSijvcqudZxUMaLFP4HLIvgs" #审批应用secret
proxies = {"http": "http://19.12.32.11:83","https": "http://19.12.32.11:83"} #配置代理
endtime=int(time.time()) #获取当前时间戳
starttime=endtime-5*24*3600 #报告周期
process_name='班值调整'
process_status=2 #审批状态：1审批中；2 已通过；3已驳回；4已取消；6通过后撤销；10已支付
i=0
csv_content=[]

def get_token():
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(ID, SECRET)
    raw_data=requests.get(token_url,proxies=proxies)
    dict_result= (raw_data.json())
    return dict_result['access_token']

token=get_token()
data_url = "https://qyapi.weixin.qq.com/cgi-bin/corp/getapprovaldata?access_token={}".format(token)
post_data = {}
post_data['starttime'] = starttime
post_data['endtime'] = endtime


#字典转JSON格式
json_post_data = json.dumps(post_data,False,False)

#配置代理
proxy1 = urllib.request.ProxyHandler({'http':'http://19.12.32.11:83'})
opener1 = urllib.request.build_opener(proxy1)
urllib.request.install_opener(opener1)
proxy2 = urllib.request.ProxyHandler({'https':'http://19.12.32.11:83'})
opener2 = urllib.request.build_opener(proxy2)
urllib.request.install_opener(opener2)

#以UTF8格式+JSON格式提交数据
request_post = urllib.request.urlopen(data_url,json_post_data.encode(encoding='UTF8'))

#获取元数据
result_raw=request_post.read()

#将元数据从unicode转码为utf-8
result_utf8=result_raw.decode('utf-8')

#从字节转为字典
result_dict=json.loads(result_utf8)

while i < len(result_dict['data']):
 if result_dict['data'][i]['spname']==process_name and result_dict['data'][i]['sp_status']==process_status:
  s=json.loads(result_dict['data'][i]['comm']['apply_data'])
  banzhi_user='CFME'+s['item-1522391303637']['value']
  banzhi_date=time.strftime('%d/%m/%Y',time.localtime(int(str(s['item-1522328069438']['value'])[0:10]))) #截取时间戳的前10位
  banzhi_code=s['item-1522327314438']['value'][0:2] #截取班值代码的前2位
  csv_line=[] #创建列表
  csv_line.append(banzhi_user) #逐个添加列元素
  csv_line.append(banzhi_date)
  csv_line.append(banzhi_code)
  csv_content.append(csv_line) #创建一行
 i=i+1 #递归

with codecs.open('Banzhi_weekly.csv','w','utf_8_sig') as csvfile:
 writer = csv.writer(csvfile)
 #writer.writerow(["标题1","标题2","标题3"])
 writer.writerows(csv_content)


