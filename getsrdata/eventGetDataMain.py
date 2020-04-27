# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 18:51:54 2020

@author: masa
"""

import geteventRanking



if __name__ == "__main__":

# イベントページ取得
#html = geteventRanking.getEventRandingPage("showfilm_seiyu")
#geteventRanking.extractFromEventRanking(html)
    
# 順位取得
    
# 各参加者の貢献ユーザリスト取得
    
# 各参加者のフォロワーとルームランクなどを取得
    roomList = []
    profile = ProfilePage()
    text = profile.getPage(242067) 
    profile.extractData(text)
    profile.saveData()
    