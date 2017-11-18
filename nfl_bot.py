import praw
import time
import bs4 as bs
import sys
import requests
import pandas as pd
import urllib.request

#must provide own keys from: https://www.reddit.com/prefs/apps/
username = ""
password = ""
client_id = ""
client_secret = ""

#team names to parse, does not include legacy teams.
teams = ("arizona cardinals", "atlanta falcons", "baltimore ravens", "buffalo bills", "carolina panthers", "chicago bears", "cincinnati bengals", "cleveland browns",
		 "dallas cowboys", "denver broncos", "detroit lions", "green bay packers", "houston texans", "indianapolis colts", "jacksonville jaguars", "kansas city chiefs",
		 "miami dolphins", "minnesota vikings", "new england patriots", "new orleans saints", "new york giants", "new york jets", "oakland raiders", "philadelphia eagles",
		 "pittsburgh steelers", "san diego chargers", "san francisco 49ers", "seattle seahawks", "st. louis rams", "tampa bay buccaneers", "tennessee titans", "washington redskins")

#read source page
nfl_source = urllib.request.urlopen("https://www.pro-football-reference.com/boxscores/game-scores.htm").read()

#BeautifulSoup4 object
soup = bs.BeautifulSoup(nfl_source,'lxml')

print(soup.find_all('p'))

#year token, might not be needed
youngest = 2002
recent = 2017

def main():
	r = bot_login()
	comments_replied_to = []

	while True:
		run_bot(r, comments_replied_to)

def bot_login():
	r = praw.Reddit(username = username,
			password = password,
			client_id = client_id,
			client_secret = client_secret,
			user_agent = "nfl_reddit_bot score poster v.1.0")
	print("Logged in successfully")

	return r

def run_bot(r, comments_replied_to):
    for comment in r.subreddit('test').comments(limit=100):
        if (contains_team(comment) and check_comment_criteria(comment)):
         #web scrape, then parse the data.
         time.sleep(10)

#simple check to see if the token is contained in the team's tuple
def contains_team(comment):
    for word in comment.split():
        if(word in teams):
            return True

#split the comment string and check if it meets the "call criteria" for a response
#ex: nfl_bot patriots vs falcons 2017
def check_comment_criteria(comment):
    text = comment.body
    comment_tokens = text.split()
    if(len(comment_tokens) == 5
        and (comment_tokens[0].lower == "nflbot" or comment_tokens[0].lower == "nfl_bot" or comment_tokens[0].lower == "nflbot!")
        and (comment_tokens[1].lower() in teams)
        and (comment_tokens[2].lower() == "v" or comment_tokens[2].lower() == "vs" or comment_tokens[2].lower() == "vs.")
        and (comment_tokens[3].lower() in teams and comment_tokens[3] != comment_tokens[1])
        and (comment_tokens[4] >= 2002)):
        print("test_successful")
    return True


def send_message(r, username, subject, body):
    try:
        r.redditor(username).message(subject, body)
        except praw.exceptions.APIException as e:
        if "USER_DOESNT_EXIST" in e.args[0]:
            print("redditor " + username + " not found, did not send a message.")
            return

if __name__ == '__main__':
    main()

