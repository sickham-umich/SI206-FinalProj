from bs4 import BeautifulSoup
import requests
import os

def get_turnover_margin():

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    
    teams = []
    turnover_margin = []
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

                turnover_margin.append(lst[9])
        else:
            print('---response error---')

    team_turnover = {}
    for i in range(len(teams)):
        team = teams[i]
        margin = turnover_margin[i]
        team_turnover[team] = margin

    return team_turnover

get_turnover_margin()