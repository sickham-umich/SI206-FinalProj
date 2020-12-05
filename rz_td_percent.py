from bs4 import BeautifulSoup
import requests
import os

def get_td_percentage():

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/703', 'https://www.ncaa.com/stats/football/fbs/current/team/703/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/703/p3']
    
    teams = []
    tds = []
    for url in urls:
        u = url
        resp = requests.get(u)
        if resp.ok:
            soup = BeautifulSoup(resp.content, 'lxml')
            schools = soup.find_all('a', class_ = 'school')
            for tag in schools:
                school = tag.text
                teams.append(school)

            body = soup.find('tbody')
            tags = body.find_all('tr')
            for tag in tags:
                stats = tag.find_all('td')
                lst = []

                for stat in stats:
                    lst.append(stat.text)

                tds.append(lst[8])
        else:
            print('---response error---')

    team_td = {}
    for i in range(len(teams)):
        team = teams[i]
        tdp = tds[i]
        team_td[team] = tdp

    return team_td

get_td_percentage()