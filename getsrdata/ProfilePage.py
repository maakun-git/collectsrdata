# -*- coding: utf-8 -*-
"""
プロフィール解析
"""

from bs4 import BeautifulSoup
import AbsHtmlPage
import csv
from datetime import datetime

"""
プロフィールページからのデータ抽出
"""
class ProfilePage(AbsHtmlPage.AbsHtmlPage):
    isActive = False
    livePagePass = '/'
    fanRoomPass = '/fan_club'
    roomName = 'name'
    roomId = 0
    followerNum = 0
    roomLevel = 0
    leagRank = 'A'
    pageDatetime = 'a'

    def getPage(self, roomId):
        self.roomId = roomId
        print(self.roomId)
        #with open('profile.html', mode='r', encoding='utf-8') as f:
        #    text = f.read()
        text = super().getHtmlPage("/room/profile?room_id=" + str(self.roomId) )
        self.pageDatetime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        return text
    
    def extractData(self, text) :
        soup = BeautifulSoup(text, 'lxml')
        
        # ルーム名
        self.roomName = soup.find("h2", attrs={"class": "room-profile-head-name"}).text

        # ルームID 取得
        self.roomId = soup.find("a", attrs={"id": "js-following-btn-l"})["data-room-id"]
        
        # 配信中か否か
        activeClass = soup.select(".room-profile-action-icon.is-active")
        #print(activeClass)
        if 0 < len(activeClass):
            self.isActive = True
        else:
            self.isActive = False
            
        # フォロワー数の抽出
        followerTag = soup.find_all("p", attrs={"class": "room-profile-info-follower"})
        self.followerNum = followerTag[0].text.split()[0]
        
        # ルームレベル
        terms = soup.find_all("dt", attrs={"class": "room-profile-status-term"})
        descs = soup.find_all("dd", attrs={"class": "room-profile-status-desc"})
        self.roomLevel = 0
        self.leagRank = 0

        if len(terms) == len(descs) :
            if terms[0].text == "ルームレベル" :
                # ルームレベル
                self.roomLevel = descs[0].text
            if terms[1].text == "リーグランク" :
                # リーグランク
                self.leagRank =  descs[1].text
    
    def saveData(self):
        with open('profile.csv', mode='a', encoding='utf8') as fileObj:
            writer = csv.writer(fileObj, delimiter=',', lineterminator='\n', skipinitialspace=True)
            writer.writerow(self.getData())
    
    def getData(self):
        return [self.pageDatetime, self.roomId, self.roomName, self.isActive, self.followerNum, self.roomLevel, self.leagRank]

if __name__ == "__main__":
   #roomIdList = [111316,194490,130606,257903,236954,264060,278279,259153,160173,282190,282880,235560]
    roomIdList = [268535,268963,60545,95851,213581,142666,292554,103793,223934,290134]
    for roomId in roomIdList:
        profile = ProfilePage()
        text = profile.getPage(roomId) 
        profile.extractData(text)
        profile.saveData()

#    print(profile.getData())
    
#print(text)
