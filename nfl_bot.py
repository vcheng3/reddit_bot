import praw
import time
import bs4 as bs
import sys
import urllib.request

#must provide own keys from: https://www.reddit.com/prefs/apps/
username = ""
password = ""
client_id = ""
client_secret = ""

#read source page
nfl_source = urllib.request.urlopen("https://www.pro-football-reference.com/boxscores/game-scores.htm").read()

#BeautifulSoup4 object
soup = bs.BeautifulSoup(nfl_source,'lxml')

print(soup.find_all('p'))

def bot_login():
	r = praw.Reddit(username = username,
			password = password,
			client_id = client_id,
			client_secret = client_secret,
			user_agent = "nfl_redd_bot score poster v.1.0")
	print("Logged in successfully")

	return r

def run_bot(r, comments_replied_to):
    time.sleep(10)

def send_message(r, username, subject, body):
	try:
		r.redditor(username).message(subject, body)
	except praw.exceptions.APIException as e:
		if "USER_DOESNT_EXIST" in e.args[0]:
			print("redditor " + username + " not found, did not send a message.")
			return

