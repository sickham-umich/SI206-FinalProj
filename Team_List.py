from bs4 import BeautifulSoup
import requests
import csv
import os

def get_team_names():

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    
    teams = []
    for url in urls:
        u = url
        resp = requests.get(u)
        if resp.ok:
            soup = BeautifulSoup(resp.content, 'lxml')
            tags = soup.find_all('a', class_ = 'school')
            for tag in tags:
                school = tag.text
                teams.append(school)
        else:
            print('---response error---')
    return teams

def write_data(lst):
    dir = os.path.dirname(__file__)
    fullpath = os.path.join(dir, 'team_list.json')
    f = open(fullpath, 'w')
    w = csv.writer(f)
    for item in lst:
        w.writerow([item])
    f.close()


team_list = get_team_names()
write_data(team_list)
    