from bs4 import BeautifulSoup
import requests
import os
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_turnover_margin():

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    
    cur.execute('CREATE TABLE IF NOT EXISTS team_turnovers (school_id INTEGER PRIMARY KEY, turnover_margin)')
    cur.execute('SELECT school_id from team_turnovers')

    # Checking teams in db and creating list
    data = cur.fetchall()
    keep_track_ids = []
    for d in data:
        keep_track_ids.append(d[0])

    
    teams = []
    turnover_margin = []
    for url in urls:
        resp = requests.get(url)
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


    team_turnover = {}
    for i in range(len(teams)):
        team = teams[i]
        margin = turnover_margin[i]
        team_turnover[team] = margin

    return team_turnover


cur, conn = setUpDatabase('ncaa_football_stats.db')

get_turnover_margin()