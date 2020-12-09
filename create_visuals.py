import sqlite3
import os
import matplotlib.pyplot as plt

"""Creates two scatter plots using data from database"""

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_wl_data(cur, conn):
    cur.execute('SELECT w_percentage FROM win_loss')
    data = cur.fetchall()
    wl = [d[0] for d in data]
    return wl

def get_rz_data(cur, conn):
    cur.execute('SELECT rz_td_percent FROM rz_tds')
    data = cur.fetchall()
    rz = [d[0] for d in data]
    return rz

def get_turnover_data(cur, conn):
    cur.execute('SELECT turnover_margin FROM team_turnovers')
    data = cur.fetchall()
    t = [d[0] for d in data]
    return t

def create_visuals(wl, rz, t):
    fig = plt.figure(1, figsize = (10, 5))

    fig.suptitle('Team Statistics Compared to Win Ratio for 2020 NCAA Football Season').set_weight('bold')
    redzone = fig.add_subplot(121)
    turnover = fig.add_subplot(122)

    redzone.scatter(rz, wl, color = 'green')
    redzone.set_xlabel('Red Zone Touchdown Ratio').set_weight('bold')
    redzone.set_ylabel('Win Ratio').set_weight('bold')

    turnover.scatter(t, wl, color = 'red')
    turnover.set_xlabel('Tunover Margin').set_weight('bold')
    turnover.set_ylabel('Win Ratio').set_weight('bold')

    plt.show()



cur, conn = setUpDatabase('ncaa_football_stats.db')
win_loss_data = get_wl_data(cur, conn)
redzone_data = get_rz_data(cur, conn)
turnover_data = get_turnover_data(cur, conn)
create_visuals(win_loss_data, redzone_data, turnover_data)