# coding:utf8
import time
import hashlib
import xml.etree.ElementTree as ET

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
        return 'Hello World!'

@app.route('/weixin', methods=['GET','POST'])
def check_signature():
    	if request.method == 'GET':
		token = 'guaiyunyun'
		query = request.args
		signature = query.get('signature','')
		timestamp = query.get('timestamp','')
		nonce = query.get('nonce','')
		echostr = query.get('echostr','')
		L = [timestamp, nonce, token]
    		L.sort()
    		s = ''.join(L)
		if hashlib.sha1(s).hexdigest() == signature:
			return make_response(echostr)
	else:
		xml_recv = ET.fromstring(request.data)
		ToUserName = xml_recv.find('ToUserName').text
		FromUserName = xml_recv.find('FromUserName').text
		Content = xml_recv.find('Content').text
		reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName>\
<FromUserName><![CDATA[%s]]></FromUserName>\
<CreateTime>%s</CreateTime>\
<MsgType><![CDATA[text]]></MsgType>\
<Content><![CDATA[%s]]></Content>\
<FuncFlag>0</FuncFlag></xml>"
		response = make_response( reply%(FromUserName, ToUserName, str(int(time.time())), Content ) )
		response.content_type = 'application/xml'
		return response
