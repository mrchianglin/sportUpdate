
# coding: utf-8

# In[1]:

# This is an automated Sports Update app
# It will send a text message using the Twilio API 
# when ther's a score by using BeautifulSoup to 
# parse through SI.com's play-by-play site of a 
# certain game and send a message when there's an 
# update. 
from urllib.request import urlopen
from bs4 import BeautifulSoup
from twilio.rest import Client

def main():
    numberPlays = currentNumPlays()
    
    gameOver = False
    while not gameOver:
        url = 'http://www.si.com/nfl/game/1635754/play-by-play'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        playByPlay  = soup.find("div", "play-by-play-tab graphic-tab-content-group js-tab-content-group margin-16-tb scoring-tab-container inactive")
        conditional = isNewPlay(numberPlays, playByPlay)
        
        if  conditional is True:
            numberPlays += 1
            thePlay = findPlay(playByPlay)
            print("cheeeeeese")
            sendMessage(thePlay)
        gameOver = isGameOver(soup)


# In[2]:

def sendMessage(thePlay):
    accountSID = 'AC3898df86ee266d6ec62e1fd77c6f0794'
    authToken = 'c53d91396d9d94297709aacc05127a63'
    client = Client(accountSID, authToken)
    myTwilioNumber = '+16265514889'
    myCellPhone = '+16268332226'
    message = client.messages.create(body=thePlay, from_=myTwilioNumber, to=myCellPhone)
    print(message.sid)


# In[3]:

def isNewPlay(numberPlays, playByPlay):
    playNum = 0 
    tables = playByPlay.find_all("table", "schedules")
    for quarter in tables:
        quarterPlays = quarter.find_all("tr")[1:]
        for play in quarterPlays:
            playNum += 1
#     print(playNum, numberPlays)
    if numberPlays >= playNum:
        return False
    return True
    


# In[4]:

def currentNumPlays():
    url = 'http://www.si.com/nfl/game/1635754/play-by-play'
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    playByPlay  = soup.find("div", "play-by-play-tab graphic-tab-content-group js-tab-content-group margin-16-tb scoring-tab-container inactive")
    playNum = 0 
    tables = playByPlay.find_all("table", "schedules")
    for quarter in tables:
        quarterPlays = quarter.find_all("tr")[1:]
        for play in quarterPlays:
            playNum += 1
    return playNum


# In[5]:

def findPlay(playByPlay):
    playString = ""
    tables = playByPlay.find_all("table", "schedules")
    lastQuarter = tables[-1]

    plays = lastQuarter.find_all("tr")
    quarterInfo = plays[0].find_all("th")
    quarterNumber = quarterInfo[0].string
    awayTeam = quarterInfo[2].string
    homeTeam = quarterInfo[3].string

    thePlay = plays[-1]
    playTags = thePlay.find_all("td")
    timeLeft = playTags[0].string
    playDesc = playTags[2]
    awayScore = playTags[3].string
    homeScore = playTags[4].string

    for x in playDesc.stripped_strings:
        playString = playString + " " + repr(x)
    playString = playString.replace("'", "")
    playString = playString + " " + quarterNumber + " " + timeLeft + " " + awayTeam + " " + awayScore + " " + homeTeam + " " + homeScore
    return playString


# In[6]:

def isGameOver(soup):
    if soup.find("strong", "status-final margin-4-left") is None:
        return False
    return True


# In[7]:

if __name__ == "__main__": main()


# In[ ]:



