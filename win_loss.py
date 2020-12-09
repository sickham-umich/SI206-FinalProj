from bs4 import BeautifulSoup
import requests
import os
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_win_loss(cur, conn):

    urls = ['https://www.ncaa.com/stats/football/fbs/current/team/742', 'https://www.ncaa.com/stats/football/fbs/current/team/742/p2', 'https://www.ncaa.com/stats/football/fbs/current/team/742/p3']
    
    cur.execute('CREATE TABLE IF NOT EXISTS win_loss (school_id INTEGER PRIMARY KEY, w_percentage REAL)')
    
    teams = []
    wl = []
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

            wl.append(lst[5])

    wl_dic = {}
    for i in range(len(teams)):
        team = teams[i]
        w = wl[i]
        wl_dic[team] = w

    return wl_dic

def add_wl_to_db(cur, conn, dic):
    
    i = 0
    for team in dic:
        if i == 25:
            break
        cur.execute('SELECT id from teams WHERE team = ?', (team, ))
        team_id = cur.fetchone()[0]
        try:
            cur.execute('INSERT INTO win_loss (school_id, w_percentage) VALUES (?, ?)', (team_id, dic[team]))
            i += 1
            print('added team data to database')
        except:
            print('Team already in database')
    conn.commit()
    return None


cur, conn = setUpDatabase('ncaa_football_stats.db')
wl_dic = get_win_loss(cur, conn)
add_wl_to_db(cur, conn, wl_dic)
