'''
Geeklist Console
================

It is a console based client written in python to access content of https://geekli.st website. You can view micros, post micros etc in a geeky way now.

AUTHOR
Name : Bhavyanshu Parasher						
Email : bhavyanshu.spl@gmail.com	

'''
from rauth import OAuth1Service
import simplejson as json
import webbrowser
import os

try:
    read_input = raw_input
except NameError:
    read_input = input


#Initializing variables - These are the default entries for Geeklist Console App
CONSUMER_KEY='B_9C1WM-hC-JcVTVOUwyOwXB0PA'
CONSUMER_SECRET='RLEw2jBmlceHb02GobOnI-wtiyukg-in6lEgQIxMttI'
ACCESS_TOKEN_FILE = '.gklst_access_token'
INTRODUCTION = '''

Welcome to https://geekli.st Command Line Application. 

Options available: 

help() - Display help message.
auth(Geeklist) - Authenticate with Geekli.st. On startup, the application will automatically authenticate.
logout() - Expire the access token.
'''
#Ending initializing variables 

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

Geeklist = OAuth1Service(
	    name='Geeklist',
	    consumer_key=CONSUMER_KEY,
	    consumer_secret=CONSUMER_SECRET,
	    request_token_url='http://api.geekli.st/v1/oauth/request_token',
	    access_token_url='http://api.geekli.st/v1/oauth/access_token',
	    authorize_url='https://geekli.st/oauth/authorize',
	    base_url='http://api.geekli.st/v1/')


def auth(Geeklist):
	auth_required = True
	if os.path.exists(ACCESS_TOKEN_FILE):
        	data = json.loads(open(ACCESS_TOKEN_FILE).read())
		global ACCESS_TOKEN
		global ACCESS_TOKEN_SECRET
        	ACCESS_TOKEN = data['access_token']
		ACCESS_TOKEN_SECRET = data['access_token_secret']
		#print ACCESS_TOKEN,ACCESS_TOKEN_SECRET | Printed them just to debug.
		userdetails()
        	auth_required = False
		print 'Authentication not required.'


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
	access_token = ACCESS_TOKEN
	access_token_secret = ACCESS_TOKEN_SECRET
	session = Geeklist.get_session((access_token,access_token_secret))
	print 'Session Created'
	r = session.get('user',verify=True)
	#print r  Returns response status | Used only to test.
	jsondata = json.loads(r.text)
	userfullname = jsondata['data']['name']
	useremail = jsondata['data']['email']
	print "You are logged in as %s & your email is %s." % (userfullname,useremail)

def getStatus():
	access_token = ACCESS_TOKEN
	access_token_secret = ACCESS_TOKEN_SECRET
	session = Geeklist.get_session((access_token,access_token_secret))
	print 'Session Created'
	r = session.get('user/micros',verify=True)
	jsondata = json.loads(r.text)
	total_micros = jsondata['data']['total_micros']
	status = jsondatamicros[u'status']
	print "Total number of micros till now : %s." %total_micros
	print "Status Messages : %s." % status

def storetoken(access_token,access_token_secret):
	global ACCESS_TOKEN_FILE
	data = {'access_token': access_token,'access_token_secret': access_token_secret}
	open(ACCESS_TOKEN_FILE,'w').write(json.dumps(data))
	print 'Access token stored'
	


def shell():
    auth(Geeklist)
    try:
        from IPython.Shell import IPShellEmbed
        IPShellEmbed()(INTRODUCTION)
    except ImportError:
        import code
        code.InteractiveConsole(globals()).interact(INTRODUCTION)

def logout():
    if os.path.exists(ACCESS_TOKEN_FILE):
        os.remove(ACCESS_TOKEN_FILE)
	print 'Logged out!'

if __name__ == '__main__':
    shell() 
