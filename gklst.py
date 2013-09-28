#!/usr/bin/env python

'''
Geeklist Console
================

It is a console based client written in python to access content of https://geekli.st website. You can view micros, post micros etc in a geeky way now.

AUTHOR
Name : Bhavyanshu Parasher (https://geekli.st/bhavyanshu)						
Email : bhavyanshu.spl@gmail.com	
Geeklist handle : @bhavyanshu
'''
from rauth import OAuth1Service
try: import simplejson as json
except ImportError: import json
from json import *
import webbrowser
import os

try:
    read_input = raw_input
except NameError:
    read_input = input




#Initializing variables - These are the default entries for Geeklist Console App
CONSUMER_KEY='B_9C1WM-hC-JcVTVOUwyOwXB0PA'
CONSUMER_SECRET='RLEw2jBmlceHb02GobOnI-wtiyukg-in6lEgQIxMttI'
ACCESS_TOKEN_FILE = os.path.join(os.path.dirname(__file__), '.gklst_access_token')
Geeklist = OAuth1Service(
	    name='Geeklist',
	    consumer_key=CONSUMER_KEY,
	    consumer_secret=CONSUMER_SECRET,
	    request_token_url='http://api.geekli.st/v1/oauth/request_token',
	    access_token_url='http://api.geekli.st/v1/oauth/access_token',
	    authorize_url='https://geekli.st/oauth/authorize',
	    base_url='http://api.geekli.st/v1/')



INTRODUCTION = '''
**************************************************************************************************************
*                                           Please use the following commands:
*
* help() - Display help message.
* auth(Geeklist) - Authenticate with Geekli.st. 
* logout() - Expire the access token in case of any authentication or bad request error.
* userdetails() - Fetches your name and email address.
* getCards() - Fetches profile information of another geek.
* getStatus() - Fetches the list of your statuses.
**************************************************************************************************************
'''
#Ending initializing variables 



#################################################All Interactive Functions#################################################
def auth(Geeklist):
	auth_required = True
	if os.path.exists(ACCESS_TOKEN_FILE):
        	data = json.loads(open(ACCESS_TOKEN_FILE).read())
		global ACCESS_TOKEN
		global ACCESS_TOKEN_SECRET
        	ACCESS_TOKEN = data['access_token']
		ACCESS_TOKEN_SECRET = data['access_token_secret']
		userdetails()
        	auth_required = False
		print 'Authentication done.'


	if auth_required: 
		request_token, request_token_secret = Geeklist.get_request_token() #Step 1 - Got request Token
		authorize_url = Geeklist.get_authorize_url(request_token) 
		print 'Authorized'
		print 'Opening your web browser, please wait..' #Step 2 - Redirecting users for pin
		url=format(authorize_url)
		webbrowser.open(url,new=2)
		pin = read_input('Enter the numerical code from browser to complete the process: ')
		session = Geeklist.get_auth_session(request_token,
				                   request_token_secret,
				                   method='POST',
				                   data={'oauth_verifier': pin}) #Step 3 - Got token & token secret
		#print session.access_token, session.access_token_secret | Step 4 - Got access token & access token secret
		storetoken(session.access_token,session.access_token_secret)
		auth(Geeklist) #Recursive call in order to make access tokens global.
		

def userdetails():
	jsondata = getjson('user')
	userfullname = jsondata['data']['name']
	useremail = jsondata['data']['email']
	print "You are logged in as %s & your email is %s." % (userfullname,useremail)

def getCards():
	jsondata = getjson('user/cards')
	total_cards = jsondata['data']['total_cards']
	print "Total number of cards till now : %s." %total_cards
	if(total_cards>9): #Need to find a work around as the response only generates 10 items at once in the jsondata. For now this is the solution.
		total_cards=9 
		for i in range(0,total_cards):  
			headline = jsondata['data']['cards'][i]['headline']
			print "Title : %s." %headline
	else:
		for i in range(0,total_cards):  
			headline = jsondata['data']['cards'][i]['headline']
			print "Title : %s." %headline

def getStatus():
	jsondata = getjson('user/micros')
	total_micros = jsondata['data']['total_micros']
	print "Total number of micros till now : %s." %total_micros
	if(total_micros>9):
		total_micros=9
		for i in range(0,total_micros):
			status = jsondata['data']['micros'][i]['status']
			print "Status Messages : %s." % status
	else:
		for i in range(0,total_micros):
			status = jsondata['data']['micros'][i]['status']
			print "Status Messages : %s." % status

def getLinks():
	jsondata = getjson('user/links')
	total_links = jsondata['data']['total_links']
	print "Total number of links shared till now : %s." %total_links
	if(total_links>9):           
		total_links=9		
		for i in range(0,total_links):
			title = jsondata['data']['links'][i]['title']
			url = jsondata['data']['links'][i]['url']
			print "Title : %s. & URL : %s" % (title,url)
	else:
		for i in range(0,total_links):
			title = jsondata['data']['links'][i]['title']
			url = jsondata['data']['links'][i]['url']
			print "Title : %s. & URL : %s" % (title,url)


def logout():
    if os.path.exists(ACCESS_TOKEN_FILE):
        os.remove(ACCESS_TOKEN_FILE)
	print 'Session cleared!'


##########################################Non Interactive Functions#########################################

def storetoken(access_token,access_token_secret):
	global ACCESS_TOKEN_FILE
	data = {'access_token': access_token,'access_token_secret': access_token_secret}
	open(ACCESS_TOKEN_FILE,'w').write(json.dumps(data))
	print 'Access token stored'
	
def getjson(urlpath):
	access_token = ACCESS_TOKEN
	access_token_secret = ACCESS_TOKEN_SECRET
	session = Geeklist.get_session((access_token,access_token_secret))
	r = session.get(urlpath,verify=True)
	jsontext = json.loads(r.text)
	return jsontext


def shell():
    auth(Geeklist)
    try:
        from IPython.Shell import IPShellEmbed
        IPShellEmbed()(INTRODUCTION)
    except ImportError:
        import code
        code.InteractiveConsole(globals()).interact(INTRODUCTION)


def help():
    print '''
**************************************************************************************************************
*                                           Please use the following commands:
*
* help() - Display help message.
* auth(Geeklist) - Authenticate with Geekli.st. 
* logout() - Expire the access token in case of any authentication or bad request error.
* userdetails() - Fetches your name and email address.
* getStatus() - Fetches the list of your statuses.
**************************************************************************************************************
'''


if __name__ == '__main__':
    shell() 
