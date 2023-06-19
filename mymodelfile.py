
import pandas as pd
import numpy as np
import math


class MyModel:
    def __init__(self):

        self.a = 5

    def fit(self, data):

        df = data[0]
        match = data[1]
        match['Venue'] = match['Venue'].str.replace(
            'MA Chidambaram Stadium, Chepauk, Chennai', 'MA Chidambaram Stadium')
        match['Venue'] = match['Venue'].str.replace(
            'Wankhede Stadium, Mumbai', 'Wankhede Stadium')

        match['Venue'] = match['Venue'].str.replace(
            'Eden Gardens, Kolkata', 'Eden Gardens')

        match['Venue'] = match['Venue'].str.replace(
            'Punjab Cricket Association IS Bindra Stadium, Mohali', 'Punjab Cricket Association Stadium, Mohali')
        match['Venue'] = match['Venue'].str.replace(
            'Punjab Cricket Association IS Bindra Stadium', 'Punjab Cricket Association Stadium, Mohali')

        match['Venue'] = match['Venue'].str.replace(
            'Arun Jaitley Stadium, Delhi', 'Arun Jaitley Stadium')

        match['Venue'] = match['Venue'].str.replace(
            'Rajiv Gandhi International Stadium', 'Rajiv Gandhi International Stadium, Hyderabad')

        match['Venue'] = match['Venue'].str.replace(
            'Rajiv Gandhi International Stadium, Hyderabad, Uppal', 'Rajiv Gandhi International Stadium, Hyderabad')

        match['Venue'] = match['Venue'].str.replace(
            'M.Chinnaswamy Stadium', 'M Chinnaswamy Stadium')
        match['Venue'] = match['Venue'].str.replace(
            'MA Chidambaram Stadium, Chepauk', 'MA Chidambaram Stadium')
        match = match[match['method'] != 'D/L']
        match = match[match['WonBy'] != 'NoResults']
        merged_df = pd.merge(df, match, on='ID')
        global final
        final = merged_df[['ID', 'Date', 'innings', 'overs', 'ballnumber', 'batter', 'bowler', 'non-striker',
                           'batsman_run', 'extras_run', 'BattingTeam', 'Team1', 'Team2', 'Season', 'Venue', 'Team1Players', 'Team2Players']]
        final = final[final['innings'] < 3]

        final['BattingTeam'] = final['BattingTeam'].str.replace(
            'Daredevils', 'Capitals')
        final['BattingTeam'] = final['BattingTeam'].str.replace(
            'Deccan Chargers', 'Sunrisers Hyderabad')
        final['BattingTeam'] = final['BattingTeam'].str.replace(
            'Rising Pune Supergiants', 'Rising Pune Supergiant')
        final['BattingTeam'] = final['BattingTeam'].str.replace(
            'Kings XI Punjab', 'Punjab Kings')

        final['Team1'] = final['Team1'].str.replace('Daredevils', 'Capitals')
        final['Team1'] = final['Team1'].str.replace(
            'Deccan Chargers', 'Sunrisers Hyderabad')
        final['Team1'] = final['Team1'].str.replace(
            'Rising Pune Supergiants', 'Rising Pune Supergiant')
        final['Team1'] = final['Team1'].str.replace(
            'Kings XI Punjab', 'Punjab Kings')

        final['Team2'] = final['Team2'].str.replace('Daredevils', 'Capitals')
        final['Team2'] = final['Team2'].str.replace(
            'Deccan Chargers', 'Sunrisers Hyderabad')
        final['Team2'] = final['Team2'].str.replace(
            'Rising Pune Supergiants', 'Rising Pune Supergiant')
        final['Team2'] = final['Team2'].str.replace(
            'Kings XI Punjab', 'Punjab Kings')
        df = final

        df = df[df['BattingTeam'] != 'Pune Warriors']
        df = df[df['BattingTeam'] != 'Gujarat Lions']
        df = df[df['BattingTeam'] != 'Kochi Tuskers Kerala']
        df = df[df['BattingTeam'] != 'Rising Pune Supergiant']

        final = final[final['overs'] < 6]
        df = df[df['overs'] < 6]

        global piv
        piv = pd.pivot_table(df, values=['batsman_run', 'extras_run'], index=['ID', 'innings', 'BattingTeam', 'Team1', 'Team2', 'Venue', 'Season'],
                             aggfunc=np.sum)

        piv['PP'] = piv['extras_run']+piv['batsman_run']

        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)
        piv.reset_index(level=0, inplace=True)

    def predict(self, test_data):
        predictions = []

        def bowler_strikerate(batsman, bowler):
            h = final[final['batter'] == batsman]
            h = h[h['extras_run'] == 0]
            h = h[h['bowler'] == bowler]
            if h['batsman_run'].sum() == 0:
                return 1.35
            elif len(h) != 0:
                return h['batsman_run'].sum()/len(h)
            else:
                return 1.35

        def stadium_strikerate(batsman, venue):
            h = final[final['batter'] == batsman]
            h = h[h['extras_run'] == 0]
            venue = venue.lstrip()
            for i in final['Venue'].unique():
                if i in venue:
                    venue = i
            h = h[h['Venue'] == venue]
            if h['batsman_run'].sum() == 0:
                return 1.35
            elif len(h) != 0:
                return h['batsman_run'].sum()/len(h)
            else:
                return 1.35

        def innings_strikerate(batsman, innings):
            h = final[final['batter'] == batsman]
            h = h[h['extras_run'] == 0]
            h = h[h['innings'] == innings]
            if h['batsman_run'].sum() == 0:
                return 1.35
            elif len(h) != 0:
                return h['batsman_run'].sum()/len(h)
            else:
                return 1.35

        for i in range(2):
            aggr_score = 0,
            venue = test_data['venue'][i]
            innings = test_data['innings'][i]
            battingteam = test_data['batting_team'][i]
            bowlingteam = test_data['bowling_team'][i]
            batsmen = test_data['batsmen'][i].split(',')
            bowlers = test_data['bowlers'][i].split(',')

            if len(batsmen) > 3 and len(bowlers) < 3:
                aggr_score = -10
            elif len(batsmen) > 4:
                aggr_score = -8
            elif len(batsmen) == 2:
                aggr_score = 10
            elif len(batsmen) == 3:
                aggr_score = 8
            elif len(batsmen) == 4:
                aggr_score = 5

            strike = []
            for i in batsmen:
                s = 0
                for j in bowlers:
                    cur = bowler_strikerate(i.lstrip(), j.lstrip())
                    s += cur
                a = stadium_strikerate(i.lstrip(), venue)
                b = innings_strikerate(i.lstrip(), innings)
                s /= len(bowlers)
                strike.append((0.3*a)+(0.65*s)+(0.05*b))
            for i in range(len(strike)):
                strike[i] *= 36/len(batsmen)
            bat = piv
            tem = bat[bat['BattingTeam'] == battingteam]['PP'].mean()
            res = (((sum(strike)+tem)/2)+bat[(bat['BattingTeam'] != bowlingteam) & (
                (bat['Team1'] == bowlingteam) | (bat['Team2'] == bowlingteam))]['extras_run'].mean())
            predictions.append(math.ceil(0.6*res+0.4*bat[(bat['BattingTeam'] != bowlingteam) & (
                (bat['Team1'] == bowlingteam) | (bat['Team2'] == bowlingteam)) & (bat['Season'] == '2022')]['PP'].mean() + aggr_score))

        return predictions
