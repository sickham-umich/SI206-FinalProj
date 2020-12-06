from bs4 import BeautifulSoup
import requests
import csv
import os

def write_data(lst):
    dir = os.path.dirname(__file__)
    fullpath = os.path.join(dir, 'team_list.json')
    f = open(fullpath, 'w')
    w = csv.writer(f)
    for item in lst:
        w.writerow([item])
    f.close()

def get_team_list():
    teams = []
    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    
    for url in urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'lxml')
        tags = soup.find_all('a', class_ = 'school')
        
        for tag in tags:
            school = tag.text
            teams.append(school)
   
    return teams

teams = get_team_list()
write_data(teams)