import pandas as pd
import numpy as np


dk_data_root = '../Draft_Kings/Data/'
data_root = '../nfldb_queries/Data/'

class FinalDF(object):

    '''
    This creates the DataFrame that will be used in analysis. It combines the position dataframes with the salary and betting line dataframes.
    '''

    def __init__(self, season_type=None, position=None, year=None, week=None, load_lines=True):
        self.position = position
        self.year = year
        self.week = week
        self.season_type = season_type
        self.load_lines = load_lines

    def _load_salaries(self):
        '''
        Formats salary dataframes. Creates a dataframe from each individual salary file, then appends them together.
        '''
        df = pd.DataFrame()
        for y in range(2014, 2017):
            for w in range(1, 18):
                new_df = pd.read_csv(dk_data_root + '/player_scores/Week{}_Year{}_player_scores2.txt'.format(w, y), delimiter=';')
                new_df['Name'] = new_df['Name'].apply(lambda x: ' '.join(x.split(', ')[::-1]))
                new_df['h/a'] = new_df['h/a'].map({'h' : 0, 'a' : 1})
                new_df.rename(index=str, columns={'Name': 'full_name', 'Week': 'week', 'Year': 'season_year', 'Pos': 'position'}, inplace=True)
                new_df = new_df[['week', 'season_year', 'full_name', 'position', 'DK salary']]
                df = df.append(new_df)
        df['week'] = df['week'].astype(int)
        df['season_year'] = df['season_year'].astype(int)
        df['position'].replace(to_replace='Def', value='DST', inplace=True)
        df['full_name'].replace(to_replace='Odell Beckham Jr.', value='Odell Beckham', inplace=True)
        return df

    def _sal_position(self):
        '''
        Gets the correct position salary dataframe.
        '''
        df = self._load_salaries()
        if self.position:
            df = df[df['position'] == self.position]
        else:
            df = df
        return df

    def _load_lines(self):
        '''
        Adds the vegas lines to the dataframe.
        '''
        if self.load_lines:
            if self.season_type != 'Regular':
                return None
            if self.year == 2009:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2009.csv')
            if self.year == 2010:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2010.csv')
            if self.year == 2011:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2011.csv')
            if self.year == 2012:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2012.csv')
            if self.year == 2013:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2013.csv')
            if self.year == 2014:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2014.csv')
            if self.year == 2015:
                df = pd.read_csv(dk_data_root + 'NFL_lines/lines_2015.csv')
            else:
                df = pd.read_csv(dk_data_root + 'NFL_lines/all_lines.csv')
            if self.week:
                df = df[df['week'] == self.week]
            return df
        else:
            return None

    def _get_nfldb_df(self):
        '''
        Creates the correct position statistic dataframe.
        '''
        if self.position:
            if self.position == 'QB':
                df = pd.read_csv(data_root + 'passing.csv')
            elif self.position == 'WR':
                df = pd.read_csv(data_root + 'rec.csv')
            elif self.position == 'RB':
                df = pd.read_csv(data_root + 'rush.csv')
            elif self.position == 'TE':
                df = pd.read_csv(data_root + 'te.csv')
            elif self.position == 'DST':
                df = pd.read_csv(data_root + 'dst.csv')
        else:
            df = pd.read_csv(data_root + 'all_stats.csv')
        if self.season_type:
            df = df[df['season_type'] == self.season_type]
        if self.year:
            df = df[df['season_year'] == self.year]
        if self.week:
            df = df[df['week'] == self.week]
        return df

    def _merge_df(self):
        '''
        Merges the two dataframes.
        '''
        df1 = self._get_nfldb_df()
        df2 = self._sal_position()
        df = df1.merge(df2, on=['week', 'season_year', 'position', 'full_name'])
        return df

    def _add_lines(self):
        '''
        Add the spreads and lines to the dataframe.
        '''
        if self.load_lines:
            df1 = self._load_lines()
            df2 = self._merge_df()
            df = df1.merge(df2, on=['week', 'season_year', 'team'])
            return df
        else:
            return self._merge_df()


    def get_df(self):
        '''
        Allows the user to get the final dataframe.
        '''
        df = self._add_lines()
        df['points_per_dollar'] = (df['DK points'] / df['DK salary']) * 1000
        return df