import os
import sqlite3
import requests
import json

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_teams():

    dir = os.path.dirname(__file__)
    fullpath = os.path.join(dir, 'team_list.json')
    f = open(fullpath, 'r')

    teams = []
    lines = f.readlines()
    for team in lines:
        teams.append(team.strip())

    return teams

def get_data(cur, conn):

    url = 'https://api.collegefootballdata.com/records?year=2020'
    resp = requests.get(url)
    data = resp.json()

    cur.execute('CREATE TABLE IF NOT EXISTS win_loss (school_id INTEGER PRIMARY KEY, win_percentage REAL)')

    dic = {}
    for d in data:
        team = d['team']
        if 'State' in team:
            team = team[:-3] + '.'
        dic[team] = round(d['total']['wins'] / d['total']['games'], 3)

    return dic

def add_wl_to_db(cur, conn, dic):
    i = 0
    for team in dic:
        if i == 25:
            break
        try:
            cur.execute('SELECT id from teams WHERE team = ?', (team, ))
            team_id = cur.fetchone()[0]
        except:
            None
        try:
            cur.execute('INSERT INTO win_loss (school_id, win_percentage) VALUES (?, ?)', (team_id, dic[team]))
            i += 1
        except:
            print('Team already in database')
    conn.commit()
    return None
    
    




cur, conn = setUpDatabase('ncaa_football_stats.db')
teams = get_teams()
dic = get_data(cur, conn)
add_wl_to_db(cur, conn, dic)


