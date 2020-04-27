# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:09:10 2020

イベントランキング
"""

from bs4 import BeautifulSoup
import AbsHtmlPage
import ProfilePage
from datetime import datetime
import csv
import pandas as pd
import json

class EventPage(AbsHtmlPage.AbsHtmlPage):
    eventPageName = 'event'
    pageDatetime = 'a'
    contribution_dfs = pd.DataFrame()
    ForDebug = False

    """
    イベントページの取得
    """
    def getPage(self, eventName, eventId):
        self.eventPageName = eventName
        self.eventId = eventId
        print(self.eventPageName)
        
        # for debug. 通信しないでファイルから読み込む.
        if(self.ForDebug == True):
            with open(self.eventPageName + ".html", mode='r', encoding='utf-8') as fileObj:
                text = fileObj.read()
        else:
            text = super().getHtmlPage("/event/" + eventName)
        self.pageDatetime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        return text

    """
    イベントページ参加者データの追加取得
    (30人以上の参加者の場合は追加ページが存在する)
    """
    def getNextPage(self, nextPage):
        print(nextPage)
        if(self.ForDebug == True):
            with open(self.eventPageName + str(nextPage) + ".json", mode='r', encoding='utf-8') as fileObj:
                text = fileObj.read()
        else:
            text = super().getHtmlPage("/event/room_list?event_id=" + str(self.eventId) + "&p=" + str(nextPage))
            
        return text
        
    """
    貢献ユーザリストページの取得
    """
    def getContributionPage(self, roomId):
        print(roomId)
        
        # for debug. 通信しないでファイルから読み込む.
        if(self.ForDebug == True):
            htmlfile = 'Contribution.html'
            if roomId == 268535 :
                htmlfile = 'Contribution2.html'
            with open(htmlfile, mode='r', encoding='utf-8') as f:
                text = f.read()
        else:      
            # 通信してhtmlを取得            
            text = super().getHtmlPage("/event/contribution/" + self.eventPageName + "?room_id=" + str(roomId) )
                
        # 取得した日付時刻を保持
        self.pageDatetime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        
        return text
    
    """
    単一メンバーの現在のイベントポイントを取得
    """
    def getMemberTotalPoint(self, roomId):
        print(roomId)
        # Jsonでページデータを取得する
        # for debug. 通信しないでファイルから読み込む.
        if(self.ForDebug == True):
            htmlfile = 'event_and_support.html'
            if roomId == 268535 :
                htmlfile = 'Contribution2.html'
            with open(htmlfile, mode='r', encoding='utf-8') as f:
                text = f.read()
        else:      
            # 通信してhtmlを取得            
            text = super().getHtmlPage("/api/room/event_and_support?room_id=" + str(roomId) )
        
        # 取得した日付時刻を保持
        self.pageDatetime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        
        #print text
    
    """
    イベントページからの情報抽出
    """
    def extractData(self, text) :
        soup = BeautifulSoup(text, 'lxml')
        
        # ランキングのメンバー抽出
        #RankingMembers = soup.find("ul", attrs={"class": "contentlist-rowlist", "id": "list-ranking"}).find_all("li")
        RankingMembers = soup.find_all("li", class_="js-follow-li")

        seeMore = soup.find_all("a", attrs={"class":"see-more", "data-type":"ranking"})
        nextPage = None
        
        if 0 < len(seeMore):
            nextPage = seeMore[0]['data-page']
            
        while nextPage != None:
            print(seeMore)
            if seeMore[0].text == "もっと見る":
                jsondata = self.getNextPage(nextPage)
                data = json.loads(jsondata)
                nextPage = data['next_page']
                soupdata = BeautifulSoup(data['html'], 'lxml')
                sublist = soupdata.find_all("li")
                RankingMembers.extend(sublist)
            else:
                print('nothing')
                break
       
        currentPointList = []
        
        with open(self.eventPageName + '.csv', mode='a', encoding='utf8') as fileObj:
            writer = csv.writer(fileObj, delimiter=',', lineterminator='\n', skipinitialspace=True)
            for member in RankingMembers:
               # 現在の順位
               roomRankingNum = member.find("div", class_="label-ranking")
               if roomRankingNum != None:
                   roomRankingNum = roomRankingNum.text.split()[0]
                   # ルーム名
                   roomName = member.find("h4", class_="listcardinfo-main-text").text
                   # イベント貢献ランキングへの相対リンク (/event/contribution/イベント名?room_id=XXXXX)
                   roomContributeLink = member.find("a", class_="room-ranking-link")["href"]
                   # プロフィールページへの相対リンク (/)
                   roomProfileLink = member.find("a", class_="profile-link")["href"]
                   
                   roomId = member.find("a", class_="js-follow-btn")["data-room-id"]
                   singleData = [roomRankingNum, self.pageDatetime, roomId, roomName]
                   print(singleData)
                   writer.writerow(singleData)
        
                   # 貢献ユーザリストの取得
                   dfs_new = self.extractContribution(roomId, roomName)
                   self.contribution_dfs = pd.concat([self.contribution_dfs, dfs_new], axis=1)
                   print(type(self.contribution_dfs), type(dfs_new))
                   print(self.contribution_dfs)
                   
                   # プロフィールページの解析
                   self.getSingleProfle(roomId)
                   
                   # 現在ポイント数を取得
                   #self.getMemberTotalPoint(roomId)
                   #currentPointList = 
                   
                   
        savetime = datetime.now().strftime('%Y%m%d_%H%M')
        self.contribution_dfs.to_csv('contributor_' + self.eventPageName + savetime + '.csv')
            
        return "aa"
    
    """
    プロフィールページの取得解析
    """
    def getSingleProfle(self, roomId):
        profile = ProfilePage.ProfilePage()
        text = profile.getPage(roomId) 
        profile.extractData(text)
        profile.saveData()

    """
    貢献ユーザリストの取得
    """
    def extractContribution(self, roomId, roomName):
        html = self.getContributionPage(roomId)
        dfs = pd.read_html(html)
        #print(len(dfs))
        idx = 0
        if 2 == len(dfs):
            idx = 1
        dfs_new = dfs[idx].add_prefix(str(roomId) + '_')
        #print(dfs_new)
        return dfs_new
        
 
#    def getSingleContribute(self, )
    
if __name__ == "__main__":
    eventPage = EventPage()
    events = [{'name': "spinnsfmodel_sa_final", 'id': 18460}, \
              {'name': "popentertainment_sr4_semif_b", 'id': 18578}] 
    text = eventPage.getPage(events[0]['name'], events[0]['id']) 
    eventPage.extractData(text)
    