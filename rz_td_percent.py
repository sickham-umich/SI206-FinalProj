from bs4 import BeautifulSoup
import requests
import os
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_td_percentage(cur, conn):

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/703', 'https://www.ncaa.com/stats/football/fbs/current/team/703/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/703/p3']
    
    cur.execute('CREATE TABLE IF NOT EXISTS rz_tds (school_id INTEGER PRIMARY KEY, rz_td_percent REAL)')

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


def add_percents_to_db(cur, conn, dic):
    
    i = 0
    for team in dic:
        if i == 25:
            break
        cur.execute('SELECT id from teams WHERE team = ?', (team, ))
        team_id = cur.fetchone()[0]
        try:
            cur.execute('INSERT INTO rz_tds (school_id, rz_td_percent) VALUES (?, ?)', (team_id, dic[team]))
            i += 1
            print('added team data to database')
        except:
            print('Team already in database')
    conn.commit()
    return None

cur, conn = setUpDatabase('ncaa_football_stats.db')
tds = get_td_percentage(cur, conn)
add_percents_to_db(cur, conn, tds)
