# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 13:58:53 2021

@author: lasin
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Grabbing the table from the website and preparing it for cleaning
BBRef=pd.read_html('https://www.basketball-reference.com/leagues/NBA_2021_shooting.html', header=None)
len(BBRef)
cleanBBRef=BBRef[0]
cleanBBRef.columns=cleanBBRef.iloc[28]
cleanBBRef.dropna(axis=1, thresh=7, inplace=True)
FinalTable=cleanBBRef.fillna(0)
FinalTable.drop_duplicates(subset='Player', inplace=True)
FinalTable=FinalTable.drop(FinalTable.index[20])


NBAshooting=FinalTable.iloc[:,9:21]

#Separating Columns for ease
PlayerName= FinalTable.loc[:,'Player']
PlayerPos = FinalTable.loc[:, 'Pos']
PlayerTeam = FinalTable.loc[:,'Tm']
PlayerGames = FinalTable.loc[:,'G']
PlayerMinutes = FinalTable.loc[:,'MP']

# Renaming columns for % of FGA by Distance to distinguish
FGAttemptsbyDistance=FinalTable.iloc[:,9:15]
FGAttemptsbyDistance.rename(columns={
    '2P':'2PA', 
    '0-3':'0-3A',
    '3-10':'3-10A',
    '10-16':'10-16A',
    '16-3P':'16-3PA',
    '3P': '3PA'}, inplace=True)

# Same for FG% by Distance
FGbyDistance=FinalTable.iloc[:,15:21]
FGbyDistance.insert(0, 'Name', PlayerName)
FGbyDistance.insert(1, 'Position', PlayerPos)
FGbyDistance.insert(2, 'Team', PlayerTeam)
FGbyDistance.insert(3, 'GP', PlayerGames)
FGbyDistance.insert(4, 'Minutes', PlayerMinutes)



#Casting appropriate datatypes
FGbyDistance['2P'] = FGbyDistance['2P'].astype(float)
FGbyDistance['10-16'] = FGbyDistance['10-16'].astype(float)
FGbyDistance['0-3'] = FGbyDistance['0-3'].astype(float)
FGbyDistance['3-10'] = FGbyDistance['3-10'].astype(float)
FGbyDistance['16-3P'] = FGbyDistance['16-3P'].astype(float)
FGbyDistance['3P'] = FGbyDistance['3P'].astype(float)
FGbyDistance['Team'] = FGbyDistance['Team'].astype(str)
FGbyDistance['Name'] = FGbyDistance['Name'].astype(str)
FGbyDistance['GP'] = FGbyDistance['GP'].astype(int)
FGbyDistance['Minutes'] = FGbyDistance['Minutes'].astype(int)
FGbyDistance['Position'] = FGbyDistance['Position'].astype(str)

#Casting datatypes for % of FGA
FGAttemptsbyDistance['2PA'] = FGAttemptsbyDistance['2PA'].astype(float)
FGAttemptsbyDistance['10-16A'] = FGAttemptsbyDistance['10-16A'].astype(float)
FGAttemptsbyDistance['0-3A'] = FGAttemptsbyDistance['0-3A'].astype(float)
FGAttemptsbyDistance['3-10A'] = FGAttemptsbyDistance['3-10A'].astype(float)
FGAttemptsbyDistance['16-3PA'] = FGAttemptsbyDistance['16-3PA'].astype(float)
FGAttemptsbyDistance['3PA'] = FGAttemptsbyDistance['3PA'].astype(float)

#Combining combo positions into a single position
CleanShootingTable = pd.concat([FGbyDistance, FGAttemptsbyDistance], axis=1)
CleanShootingTable['Position'].replace({
   'PF-SF':'PF',
   'SG-SF':'SG',
   'SG-PG':'SG',
   'PG-SG':'PG',
   'PF-C':'PF',
   'SF-PF':'SF',
   'SF-SG': 'SG',
   'C-PF':'C'}, inplace=True)

#Updating tables to be converted from wide form to long form and saved to CSV
FigGraphDrop = CleanShootingTable.drop(columns = ['GP','Minutes', 'Position'])
FigGraph = pd.melt(FigGraphDrop, id_vars = ['Name'], value_vars = ['2P', '0-3', '3-10', '10-16', '16-3P', '3P'],
                   var_name = 'Shot Distance', value_name = 'FG%')
FigGraph.to_csv(r'C:/Users/lasin/NBAFigDisplay.csv', index = False, header = True)

#Same for the other tables 
FigDrop2 = CleanShootingTable.drop(columns = ['GP','Minutes', 'Position'])
FigGraph2 = pd.melt(FigDrop2, id_vars = ['Name'], value_vars = ['2PA', '0-3A', '3-10A', '10-16A', '16-3PA', '3PA'],
                   var_name = 'Shot Distance', value_name = '% of FG taken')
FigGraph2.to_csv(r'C:/Users/lasin/NBAFigDisplay2.csv', index = False, header = True)


CleanShootingTable.to_csv(r'C:/Users/lasin/NBA_Table1.csv', index=False, header=True)
sns.set(style='ticks')

#Example/Test plot
plt.xlabel('% of FGA by Distance', fontsize=20)
plt.ylabel('FG% by Distance', fontsize=18)
sns.set_palette('gnuplot2_r')
NBA=sns.relplot(data=CleanShootingTable, x='10-16A', y='10-16', col='Team', col_wrap=5, 
            hue='Position', size='Minutes')


##Any plotting that wants to be done
#plt.set_ylabel('FG% by Distance', fontsize=18)
#plt.locator_params(axis='both', nbins=50)
#plt.show()
#sns.set(rc={'figure.figsize':(20, 8.27)})
#g=sns.FacetGrid(FGbyDistance, col='Team', margin_titles=True)
#print(g.map(sns.regplot, 'Name', '10-16', color='purple', fit_reg=False, x_jitter=.1))
#sns.despine(left=True)
#plt.legend(bbox_to_anchor=(21, 8.27), loc='upper left', borderaxespad=0)
#plt.show()