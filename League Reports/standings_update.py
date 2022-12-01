import pandas as pd
import streamlit as st
import pipreqs
import numpy as np


league = 'SBC'
season = 2038
curr_date = '2038-11-01'
league_al_name = 'AL' 
league_nl_name = 'NL'

# NBC Tournament only. This needs to be updated once annually
tourney_start = '2023-07-04'
tourney_end = '2023-07-25'

path = 'C:/Users/night/OneDrive/Documents/Out of the Park Developments/OOTP Baseball 21/saved_games/'


leagues = {
    "SBC":[145, 
           '2038-04-04', 
           2038,
           path + 'SBC.lg/import_export/csv/'],
    "PBC":[146, 
           '2030-10-28',
           2030,
           path + 'PBC.lg/import_export/csv/'],
    "NBC":[153, 
           '2023-04-11',
           2024,
           path + 'NBC.lg/import_export/csv/'],
    "MVP":[153, 
           '2024-03-28', 
           2024,
           path + 'MVP.lg/import_export/csv/']
}

def comp_balance(league):
    team_history = pd.read_csv(leagues[league][3] + 'team_history.csv')
    team_history_financials = pd.read_csv(leagues[league][3] + 'team_history_financials.csv')
    team_history = team_history[(team_history['year'] == (leagues[league][2] - 1)) & 
                            (team_history['league_id'] == leagues[league][0])].set_index('team_id')

    team_history = team_history[['name', 'nickname', 'made_playoffs']]

    team_history_financials = team_history_financials[(team_history_financials['year'] == (leagues['SBC'][2] - 1)) & 
                            (team_history_financials['league_id'] == leagues['SBC'][0])].set_index('team_id')

    temp = pd.merge(team_history, team_history_financials, how = 'left', left_index = True, right_index = True)
    
    comp_bal = pd.DataFrame()
    comp_bal['Team'] = temp['name'] + ' ' + temp['nickname']
    comp_bal['Total Revenue'] = temp['gate_revenue'] + \
                                temp['season_ticket_revenue'] + \
                                temp['media_revenue'] + \
                                temp['merchandising_revenue'] + \
                                temp['playoff_revenue']
    comp_bal['Media Revenue'] = temp['media_revenue']
    comp_bal['Media Revenue %'] = round((comp_bal['Media Revenue']/comp_bal['Total Revenue'])*100,1)
    comp_bal['Other Revenue %'] = 100 - comp_bal['Media Revenue %']
    comp_bal['Market Size'] = temp['market']
    comp_bal['Playoffs'] = temp['made_playoffs']
    
    return comp_bal

sbc_comp_bal = comp_balance('SBC')
st.table(sbc_comp_bal)


def teams(league):
    teams = pd.read_csv(leagues[league][3] + 'teams.csv')[['name', 'nickname','team_id','sub_league_id', 'division_id']]
    teams = teams[teams['team_id'] < 80]
    teams['league'] = np.where(teams['sub_league_id'] == 0, "AL", "NL")
    teams['division'] = np.select(
    [
        (teams['sub_league_id'] == 0) & (teams['sub_league_id'] == 0),
        (teams['sub_league_id'] == 0) & (teams['sub_league_id'] == 1),
        (teams['sub_league_id'] == 0) & (teams['sub_league_id'] == 2),
        (teams['sub_league_id'] == 1) & (teams['sub_league_id'] == 0),
        (teams['sub_league_id'] == 1) & (teams['sub_league_id'] == 1),
        (teams['sub_league_id'] == 1) & (teams['sub_league_id'] == 2)
    ],
    [
        'East',
        'Central',
        'West',
        'East',
        'Central',
        'West'
    ],
    default = 'Unknown'
    )

    teams['team'] = teams['name'] + ' ' + teams['nickname']

    return teams[['team', 'league', 'division']].set_index(teams['team_id'])