from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import seaborn
import numpy as np

pd.set_option('display.max_columns', 30)

passing_df = pd.read_csv('Data/passing_df.csv')
receiving_df = pd.read_csv('Data/receiving_df.csv')
rushing_df = pd.read_csv('Data/rushing_df.csv')
tight_end_df = pd.read_csv('Data/tight_end_df.csv')
defense_df = pd.read_csv('Data/defense_df.csv')

# create new column for the player's team's score
def team_score(row):
    if row['team'] == row['home_team']:
        return row['home_score']
    else:
        return row['away_score']

def DK_passing_bonus(row):
    if row['passing_yds'] >= 300:
        row['DK points'] = 3
        return row['DK points']
    else:
        row['DK points'] = 0
        return row['DK points']

def DK_receiving_rush_bonus(row):
    if row['receiving_yds'] >= 100:
        row['DK points'] = 3
        return row['DK points']
    if row['rushing_yds'] >= 100:
        row['DK points'] = 3
        return row['DK points']
    else:
        row['DK points'] = 0
        return row['DK points']

# get team score for each player
passing_df['team_score'] = passing_df.apply(lambda row: team_score(row), axis=1)

receiving_df['team_score'] = receiving_df.apply(lambda row: team_score(row), axis=1)

rushing_df['team_score'] = rushing_df.apply(lambda row: team_score(row), axis=1)

tight_end_df['team_score'] = tight_end_df.apply(lambda row: team_score(row), axis=1)


# get touchdown points for each player
passing_df['total_td_points'] = passing_df['passing_tds'] * 6
receiving_df['total_td_points'] = receiving_df['receiving_tds'] * 6
rushing_df['total_td_points'] = rushing_df['receiving_tds'] * 6
tight_end_df['total_td_points'] = tight_end_df['receiving_tds'] * 6


# get score percentage
passing_df['td_score_percentage'] = passing_df['total_td_points']/passing_df['team_score']
receiving_df['total_score_percentage'] = receiving_df['total_td_points']/receiving_df['team_score']
rushing_df['total_score_percentage'] = rushing_df['total_td_points']/rushing_df['team_score']
tight_end_df['total_score_percentage'] = tight_end_df['total_td_points']/rushing_df['team_score']

drop_cols = ['home_team', 'home_score', 'away_team', 'away_score']

passing_df.drop(drop_cols, axis=1, inplace=True)
receiving_df.drop(drop_cols, axis=1, inplace=True)
rushing_df.drop(drop_cols, axis=1, inplace=True)
tight_end_df.drop(drop_cols, axis=1, inplace=True)


def plot_score_percentage():
    x = passing_df_2016_total['td_score_percentage']
    y = passing_df_2016_total['DK points']
    labels = passing_df_2016_total.index
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    for label, x, y in itertools.izip(labels, x, y):
            ax.annotate(label, xy = (x, y))
    ax.set_xlabel('TD score percentage')
    ax.set_ylabel('DK points')
    plt.show()

def plot_total_td_points():
    x = passing_df_2016_total['total_td_points']
    y = passing_df_2016_total['DK points']
    labels = passing_df_2016_total.index
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    for label, x, y in itertools.izip(labels, x, y):
            ax.annotate(label, xy = (x, y))
    ax.set_xlabel('TD score weighted value')
    ax.set_ylabel('DK points')
    plt.show()

def plot_td():
    x = passing_df_2016_total['passing_tds']
    y = passing_df_2016_total['DK points']
    labels = passing_df_2016_total.index
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    for label, x, y in itertools.izip(labels, x, y):
            ax.annotate(label, xy = (x, y))
    ax.set_xlabel('TDs')
    ax.set_ylabel('DK points')
    plt.show()

def DK_points(df):
    points = (df['passing_yds']/25) + (df['passing_tds']*4) + (df['passing_twoptm'] * 2) + (df['rushing_yds']/10) + (df['rushing_tds'] * 6) + (df['receiving_yds']/10) + (df['receiving_tds'] * 6) + (df['receiving_twoptm'] * 2) + (df['rushing_yds']/10) + (df['rushing_tds'] * 6) + (df['rushing_twoptm'] * 2) + (df['fumble_rec_tds'] * 6) + (df['kicking_rec_tds'] * 6) + (df['punt_ret_tds'] * 6 )- (df['passing_int'] * 2) - (df['fumbles_total']) - (df['rushing_loss_yds']/10)
    return points

def passing_point_data(df, year=None, week=None, player=None):
    if year:
        df = df[df['season_year'] == year]
    else:
        pass
    if week:
        df = df[df['week'] == week]
    else:
        pass
    if player:
        df = df[df['full_name'] == player]
    else:
        pass
    df['DK points'] = df.apply(lambda row: DK_passing_bonus(row), axis=1)
    df['tds_f_pts'] = df['passing_tds'] * 4
    df['yds_f_pts'] = df['passing_yds'] * 0.04
    df['DK points'] = df['DK points'] + (df['passing_yds']* 0.04) + (df['passing_tds']*4) + (df['passing_twoptm'] * 2) + (df['rushing_yds'] * 0.1) + (df['rushing_tds'] * 6) + (df['receiving_yds'] * 0.1) + (df['receiving_tds'] * 6) + (df['receiving_twoptm'] * 2) + (df['rushing_yds'] * 0.1) + (df['rushing_tds'] * 6) + (df['rushing_twoptm'] * 2) - (df['passing_int']) - (df['fumbles_total'])
    return df

def rec_rush_point_data(df, year=None, week=None, player=None):
    if year:
        df = df[df['season_year'] == year]
    else:
        pass
    if week:
        df = df[df['week'] == week]
    else:
        pass
    if player:
        df = df[df['full_name'] == player]
    else:
        pass
    df['DK points'] = df.apply(lambda row: DK_receiving_rush_bonus(row), axis=1)
    df['DK points'] = df['DK points'] + df['receiving_rec'] + (df['receiving_yds'] * 0.1) + (df['receiving_tds'] * 6) + (df['receiving_twoptm'] * 2) + (df['rushing_yds'] * 0.1) + (df['rushing_tds'] * 6) + (df['rushing_twoptm'] * 2) + (df['fumble_rec_tds'] * 6) + (df['kicking_rec_tds'] * 6) + (df['punt_ret_tds'] * 6 ) - (df['fumbles_total'])
    return df


# messing around with groupby
# rec_df = rec_rush_data(receiving_df)
# rec_2015 = rec_df[rec_df['season_year'] == 2015]
# grouped_2015 = rec_2015.groupby('full_name')
# grouped_mean_std = grouped_2015['DK points'].agg([np.mean, np.std]).sort_values('mean', ascending=False).reset_index()
# grouped_mean_std['std_diff'] = grouped_mean_std['mean'] - grouped_mean_std['std']

if __name__ == '__main__':
    # pass_2016 = passing_data(passing_df, year=2016)
    # rec_2016 = rec_rush_data(receiving_df, year=2016)
    # rush_2016 = rec_rush_data(rushing_df, year=2016)
    # tight_end_2016 = rec_rush_data(tight_end_df, year=2016)
    #
    # son_mon_teams = ['MIN', 'CHI', 'PHI', 'DAL']
    #
    # pass_son_mon_night = pass_2016[pass_2016['team'].isin(son_mon_teams)]
    # rec_son_mon_night = rec_2016[rec_2016['team'].isin(son_mon_teams)]
    # rush_son_mon_night = rush_2016[rush_2016['team'].isin(son_mon_teams)]
    # tight_end_son_mon_night = tight_end_2016[tight_end_2016['team'].isin(son_mon_teams)]
    #
    # # finding sun_mon_night_pass data
    # grouped_p = pass_son_mon_night.groupby(['full_name']).mean().reset_index()
    # grouped_rec = rec_son_mon_night.groupby(['full_name']).mean().reset_index()
    # grouped_rush = rush_son_mon_night.groupby(['full_name']).mean().reset_index()
    # grouped_tight_end = tight_end_son_mon_night.groupby(['full_name']).mean().reset_index()
