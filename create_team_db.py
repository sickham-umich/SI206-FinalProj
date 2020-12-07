from bs4 import BeautifulSoup
import requests
import csv
import os
import sqlite3

'''FINISHED THIS WITH ADDING 25 TEAMS EACH TIME TO TEAMS TABLE IN DB'''

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_team_names(cur, conn):

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/29', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/29/p3']
    

    cur.execute('CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, team TEXT)')
    cur.execute('SELECT team from teams')

    # Checking teams in db and creating list
    data = cur.fetchall()
    keep_track_teams = []
    for d in data:
        keep_track_teams.append(d[0])

    teams = []
    for url in urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'lxml')
        tags = soup.find_all('a', class_ = 'school')
        
        for tag in tags:
            school = tag.text
            if school not in keep_track_teams:
                teams.append(school)
            if len(teams) == 25:
                break
        if len(teams) == 25:
            break

    return teams

def add_teams_db(cur, conn, teams):
    for team in teams:
        cur.execute('INSERT INTO teams (team) VALUES (?)', (team,))
    conn.commit()

    print(f'Added {len(teams)} new teams to teams table in database')
    return None





cur, conn = setUpDatabase('ncaa_football_stats.db')
team_list = get_team_names(cur, conn)
add_teams_db(cur, conn, team_list)




    