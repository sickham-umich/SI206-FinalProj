from bs4 import BeautifulSoup
import requests
import os
import sqlite3

"""Creates 'team_turnovers tables in database and adds 25 rows each time code is run"""

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_turnover_margin(cur, conn):

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    
    cur.execute('CREATE TABLE IF NOT EXISTS team_turnovers (school_id INTEGER PRIMARY KEY, turnover_margin INTEGER)')
    
    teams = []
    turnover_margin = []
    for url in urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'lxml')

        # finding tags with schools
        schools = soup.find_all('a', class_ = 'school')

        # finding stats for schools
        body = soup.find('tbody')
        tags = body.find_all('tr')

        for tag in schools:
            school = tag.text

            teams.append(school)

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

def add_turnovers_to_db(cur, conn, dic):
    
    i = 0
    for team in dic:
        if i == 25:
            break
        cur.execute('SELECT id from teams WHERE team = ?', (team, ))
        team_id = cur.fetchone()[0]
        try:
            cur.execute('INSERT INTO team_turnovers (school_id, turnover_margin) VALUES (?, ?)', (team_id, dic[team]))
            i += 1
            print('added team data to database')
        except:
            print('Team already in database')
    conn.commit()


cur, conn = setUpDatabase('ncaa_football_stats.db')
turnover_dic = get_turnover_margin(cur, conn)
add_turnovers_to_db(cur, conn, turnover_dic)
