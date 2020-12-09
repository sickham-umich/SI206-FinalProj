# These files will gather data from 2020 NCAA football teams and compare it to there win/loss ratio

# 1. create_team_list.py was used to create team_list.json to reference the teams throughout the project

# 2. Run create_team_db.py 6 times. It will initially create ncaa_football_stats.db and
# each time it will add 25 rows to 'teams' table in database

# 3. Run turnover_margin.py 6 times to add 25 rows to 'team_turnovers' 
# table in database each time

# 4. Same thing for rz_td_percentage.py and win_loss.py

# After that you will have your database with 4 tables, teams, team_turnovers, rz_tds, and win_loss

# 5. Run process_data.py to create text file summary_data.txt to crunch some numbers

# 6. Run create_visuals.py to create 2 scatter plots summarizing the statistics

# data will automatically update as season continues
