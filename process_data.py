import sqlite3
import csv
import os
import numpy as np

"""Creates text document 'summary_data.txt' that summarizes some of the data """

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def write_data(rz, turnover, dic):
    dir = os.path.dirname(__file__)
    fullpath = os.path.join(dir, 'summary_data.txt')
    f = open(fullpath, 'w')

    f.write(f"The average correlation between a ncaa football team's red zone touchdown percentage and their win/loss ratio in 2020 is {rz}.\n")
    f.write('\n')
    f.write('\n')

    f.write(f"The average correlation between a ncaa football team's turnover margin and their win/loss ratio in 2020 is {turnover}.\n")
    f.write('\n')
    f.write('\n')

    f.write(f"{dic['number of teams']} ncaa football teams have not lost a game in 2020. Their average redzone touchdown percentage is {dic['average rztd percentage']}. Their average turnover margin is {dic['average turnover margin']}.")

def get_correlation(x_lst, y_lst):
    table = np.corrcoef(x_lst, y_lst)
    if table[0][1] == table[1][0]:
        return round(table[0][1], 4)

def get_rz_correlation(cur, conn):
    rz = []
    cur.execute('SELECT rz_td_percent FROM rz_tds')
    data = cur.fetchall()
    for d in data:
        rz.append(d[0])

    wl = []
    cur.execute('SELECT w_percentage FROM win_loss')
    stats = cur.fetchall()
    for stat in stats:
        wl.append(stat[0])

    correlation =  get_correlation(wl, rz)
    return correlation

    

def get_turnover_correlation(cur, conn):
    turnover = []
    cur.execute('SELECT turnover_margin FROM team_turnovers')
    data = cur.fetchall()
    for d in data:
        turnover.append(d[0])

    wl = []
    cur.execute('SELECT w_percentage FROM win_loss')
    stats = cur.fetchall()
    for stat in stats:
        wl.append(stat[0])

    correlation =  get_correlation(wl, turnover)
    return correlation
    
def get_1000_teams_stats(cur, conn):
    
    cur.execute('SELECT teams.team FROM teams JOIN win_loss ON teams.id = win_loss.school_id WHERE win_loss.w_percentage = 1.0')
    data = cur.fetchall()
    teams = [d[0] for d in data]
    
    rz = []
    t = []
    for team in teams:
        cur.execute('SELECT rz_tds.rz_td_percent FROM rz_tds JOIN teams ON rz_tds.school_id = teams.id WHERE teams.team = ?', (team, ))
        d = cur.fetchone()
        rz.append(d[0])
        
        cur.execute('SELECT team_turnovers.turnover_margin FROM team_turnovers JOIN teams ON team_turnovers.school_id = teams.id WHERE teams.team = ?', (team, ))
        d = cur.fetchone()
        t.append(d[0])

    average_rz = round(sum(rz) / len(rz), 4)
    average_t = round(sum(t) / len(t), 4)
    
    dic = {}
    dic['number of teams'] = len(teams)
    dic['average rztd percentage'] = average_rz
    dic['average turnover margin'] = average_t
    
    return dic


cur, conn = setUpDatabase('ncaa_football_stats.db')
rz_corr = get_rz_correlation(cur, conn)
t_corr = get_turnover_correlation(cur, conn)
best_teams_dic = get_1000_teams_stats(cur, conn)
write_data(rz_corr, t_corr, best_teams_dic)


