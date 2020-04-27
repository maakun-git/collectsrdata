# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:43:22 2020

@author: masa
"""

from bs4 import BeautifulSoup
import AbsHtmlPage
import csv
from datetime import datetime
import pandas as pd

"""
プロフィールページからのデータ抽出
"""
class ContributionPage(AbsHtmlPage.AbsHtmlPage):
    pageDatetime = 'a'

    def getPage(self, address):
        print(address)
        #with open('Contribution.html', mode='r', encoding='utf-8') as f:
        #    text = f.read()
        text = super().getHtmlPage("/room/profile?room_id=" + str(self.roomId) )
        self.pageDatetime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        return text
    
    def extractData(self, text) :
        soup = BeautifulSoup(text, 'lxml')
        
        singleContributor = {'rank': 1, 'name': 'aa', 'point': 0}

        # ランキングのメンバー抽出
        memberTable = soup.find_all("table", class_="table-type-01")
        print(len(memberTable))
        members = memberTable[1].find_all("tr")
        #print(members)
        for member in members :
            if(member.find("td", class_="ta-r")):
                singleData = member.find_all("td")
                singleContributor = {'rank': singleData[0].text, 'name': singleData[1].text, 'point': singleData[2].text}
        #        print(singleContributor)
           # <span>1</span> <span>ひろふみ</span> <span>69373pt</span>
           #if(3 == len(contributor)):
           #    singleContributor = {'rank': contributor[0].text, 'name': contributor[1].text, 'point': contributor[2].text}
           #    print(singleContributor)
           #    #self.getSingleProfle(roomId)
    
if __name__ == "__main__":
    page = ContributionPage()
    text = page.getPage('test')
    dfs = pd.read_html(text)
    print(len(dfs))
    print(dfs[1])
    page.extractData(text)
#    profile.saveData()

#    print(profile.getData())
    
#print(text)
