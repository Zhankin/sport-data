import time
import datetime
import requests
import socket
import pickle
import struct
import pandas as pd
import json
import subprocess
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import six

def getdata(url):
	r=requests.get(url, headers={'X-Auth-Token': key})
	response=r.json()
	return response
def check_W(a,b):
	if a>b:
		return 1
	else:
		return 0
def check_L(a,b):
	if a<b:
		return 1
	else:
		return 0
def check_D(a,b):
	if a==b:
		return 1
	else:
		return 0
def check_1X(a,b):
	if a>=b:
		return 1
	else:
		return 0
def check_X2(a,b):
	if a<=b:
		return 1
	else:
		return 0
def check_TB15(a,b):
	if a+b>1.5:
		return 1
	else:
		return 0
def check_TB25(a,b):
	if a+b>2.5:
		return 1
	else:
		return 0
def check_TB35(a,b):
	if a+b>3.5:
		return 1
	else:
		return 0
def check_1TB05(a,b):
	if a+b>0.5:
		return 1
	else:
		return 0
def check_1TB15(a,b):
	if a+b>1.5:
		return 1
	else:
		return 0
def check_1ITB05(a,b):
	if a>0.5:
		return 1
	else:
		return 0
def check_1ITB15(a,b):
	if a>1.5:
		return 1
	else:
		return 0
def check_1B2(a,b,c,d):
	if a+b>c+d:
		return 1
	else:
		return 0
def check_1D2(a,b,c,d):
	if a+b==c+d:
		return 1
	else:
		return 0
def check_2B1(a,b,c,d):
	if c+d>a+b:
		return 1
	else:
		return 0
def check_I1B2(a,b):
	if a>b:
		return 1
	else:
		return 0
def check_I2B1(a,b):
	if b>a:
		return 1
	else:
		return 0
def check_I1D2(a,b):
	if a==b:
		return 1
	else:
		return 0

def render_mpl_table(data, col_width=10.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
	if ax is None:
		size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
		fig, ax = plt.subplots(figsize=size)
		ax.axis('off')

	mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

	mpl_table.auto_set_font_size(False)
	mpl_table.set_fontsize(font_size)

	for k, cell in six.iteritems(mpl_table._cells):
		cell.set_edgecolor(edge_color)
		if k[0] == 0 or k[1] < header_columns:
			cell.set_text_props(weight='bold', color='w')
			cell.set_facecolor(header_color)
		else:
			cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
	fig.savefig('test.png') 
	return ax


def addcolumn(data,stadium):
	data['time_2_goals_Team1']=data.apply(lambda row: row.Goals_Team1-row.time_1_goals_Team1, axis=1)
	data['time_2_goals_Team2']=data.apply(lambda row: row.Goals_Team2-row.time_1_goals_Team2, axis=1)

	data['Win']=data.apply(lambda row: check_W(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['Loss']=data.apply(lambda row: check_L(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['Draw']=data.apply(lambda row: check_D(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['1X']=data.apply(lambda row: check_1X(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['X2']=data.apply(lambda row: check_X2(row.Goals_Team1,row.Goals_Team2), axis=1)

	data['Total 1.5']=data.apply(lambda row: check_TB15(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['Total 2.5']=data.apply(lambda row: check_TB25(row.Goals_Team1,row.Goals_Team2), axis=1)
	data['Total 3.5']=data.apply(lambda row: check_TB35(row.Goals_Team1,row.Goals_Team2), axis=1)

	data['Total 1T 0.5']=data.apply(lambda row: check_1TB05(row.time_1_goals_Team1,row.time_1_goals_Team2), axis=1)
	data['Total 1T 1.5']=data.apply(lambda row: check_1TB15(row.time_1_goals_Team1,row.time_1_goals_Team2), axis=1)
	data['Total 2T 0.5']=data.apply(lambda row: check_1TB05(row.Goals_Team1-row.time_1_goals_Team1,row.Goals_Team2-row.time_1_goals_Team2), axis=1)
	data['Total 2T 1.5']=data.apply(lambda row: check_1TB15(row.Goals_Team1-row.time_1_goals_Team1,row.Goals_Team2-row.time_1_goals_Team2), axis=1)

	data['Total 1T>2T']=data.apply(lambda row: check_1B2(row.time_1_goals_Team1,row.time_1_goals_Team2,row.Goals_Team1-row.time_1_goals_Team1,row.Goals_Team2-row.time_1_goals_Team2), axis=1)
	data['Total 2T>1T']=data.apply(lambda row: check_2B1(row.time_1_goals_Team1,row.time_1_goals_Team2,row.Goals_Team1-row.time_1_goals_Team1,row.Goals_Team2-row.time_1_goals_Team2), axis=1)
	data['Total 1T=2T']=data.apply(lambda row: check_1D2(row.time_1_goals_Team1,row.time_1_goals_Team2,row.Goals_Team1-row.time_1_goals_Team1,row.Goals_Team2-row.time_1_goals_Team2), axis=1)    


	data['Team1 Total 1T 0.5']=data.apply(lambda row: check_1ITB05(row.time_1_goals_Team1,0), axis=1)
	data['Team1 Total 1T 1.5']=data.apply(lambda row: check_1ITB15(row.time_1_goals_Team1,0), axis=1)
	data['Team1 Total 2T 0.5']=data.apply(lambda row: check_1ITB05(row.Goals_Team1-row.time_1_goals_Team1,0), axis=1)
	data['Team1 Total 2T 1.5']=data.apply(lambda row: check_1ITB15(row.Goals_Team1-row.time_1_goals_Team1,0), axis=1)

	data['Team2 Total 1T 0.5']=data.apply(lambda row: check_1ITB05(row.time_1_goals_Team2,0), axis=1)
	data['Team2 Total 1T 1.5']=data.apply(lambda row: check_1ITB15(row.time_1_goals_Team2,0), axis=1)
	data['Team2 Total 2T 0.5']=data.apply(lambda row: check_1ITB05(row.Goals_Team2-row.time_1_goals_Team2,0), axis=1)
	data['Team2 Total 2T 1.5']=data.apply(lambda row: check_1ITB15(row.Goals_Team2-row.time_1_goals_Team2,0), axis=1)

	data['Team 1 Total 1T>2T']=data.apply(lambda row: check_I1B2(row.time_1_goals_Team1,row.Goals_Team1-row.time_1_goals_Team1), axis=1)
	data['Team 1 Total 2T>1T']=data.apply(lambda row: check_I2B1(row.time_1_goals_Team1,row.Goals_Team1-row.time_1_goals_Team1), axis=1)
	data['Team 1 Total 1T=2T']=data.apply(lambda row: check_I1D2(row.time_1_goals_Team1,row.Goals_Team1-row.time_1_goals_Team1), axis=1)

	data['Team 2 Total 1T>2T']=data.apply(lambda row: check_I1B2(row.time_1_goals_Team2,row.Goals_Team2-row.time_1_goals_Team2), axis=1)
	data['Team 2 Total 2T>2T']=data.apply(lambda row: check_I2B1(row.time_1_goals_Team2,row.Goals_Team2-row.time_1_goals_Team2), axis=1)
	data['Team 2 Total 1T=2T']=data.apply(lambda row: check_I1D2(row.time_1_goals_Team2,row.Goals_Team2-row.time_1_goals_Team2), axis=1)

	data2 = data[data.Home_Away == stadium].copy()

	return data,data2

def byteam(team,need_id,data):
	r=requests.get('http://api.football-data.org/v1/competitions/'+need_id+'/teams', headers={'X-Auth-Token': key})
	response=r.json()
	for x in response['teams']:
		if x['name']==team:
			fix=x['_links']['fixtures']['href']
			fix=getdata(fix)
			z=0
			for y in fix['fixtures']:
				if y['status']=='FINISHED':
					if y['_links']['competition']['href']=='http://api.football-data.org/v1/competitions/'+need_id:
						#if y['result'].has_key('halfTime')==True:
						if 'halfTime' in y['result']:
							if y['homeTeamName']==team:
							    data.loc[z]=[y['date'],y['homeTeamName'],y['awayTeamName'],'home',y['result']['goalsHomeTeam'],y['result']['goalsAwayTeam'],y['result']['halfTime']['goalsHomeTeam'],y['result']['halfTime']['goalsAwayTeam']]
							else:
							    data.loc[z]=[y['date'],y['awayTeamName'],y['homeTeamName'],'away',y['result']['goalsAwayTeam'],y['result']['goalsHomeTeam'],y['result']['halfTime']['goalsAwayTeam'],y['result']['halfTime']['goalsHomeTeam']]    
							z+=1
                
			break
	return data

def tabledata(a):
	return str(round(a.mean()*100,2))
def printdata(a,b):
	return str(round(b.mean()*100,2))+' % = '+a
def printdata_goals(a,b):
	return str(round(b.mean(),2))+' goals = '+a
def printall(data):
	output='__________'
	ls_name_export=['Win','Loss','Draw','1X','X2',
'Total 1.5','Total 2.5','Total 3.5',
'Total 1T 0.5','Total 1T 1.5','Total 2T 0.5','Total 2T 1.5',
'Total 1T>2T','Total 2T>1T','Total 1T=2T',
'Team1 Total 1T 0.5','Team1 Total 1T 1.5','Team1 Total 2T 0.5','Team1 Total 2T 1.5',
'Team2 Total 1T 0.5','Team2 Total 1T 1.5','Team2 Total 2T 0.5','Team2 Total 2T 1.5',
'Team 1 Total 1T>2T','Team 1 Total 2T>1T','Team 1 Total 1T=2T',
'Team 2 Total 1T>2T','Team 2 Total 2T>2T','Team 2 Total 1T=2T']
	ls_name_data=['Win','Loss','Draw','1X','X2',
'Total 1.5','Total 2.5','Total 3.5',
'Total 1T 0.5','Total 1T 1.5','Total 2T 0.5','Total 2T 1.5',
'Total 1T>2T','Total 2T>1T','Total 1T=2T',
'Team1 Total 1T 0.5','Team1 Total 1T 1.5','Team1 Total 2T 0.5','Team1 Total 2T 1.5',
'Team2 Total 1T 0.5','Team2 Total 1T 1.5','Team2 Total 2T 0.5','Team2 Total 2T 1.5',
'Team 1 Total 1T>2T','Team 1 Total 2T>1T','Team 1 Total 1T=2T',
'Team 2 Total 1T>2T','Team 2 Total 2T>2T','Team 2 Total 1T=2T']
	z=0
	ls_for_export=[]
	for x,y in zip(ls_name_export,ls_name_data):
		ls_for_export.append(tabledata(data[y]))
		z+=1

	return output,ls_for_export

def getleague(need):
	r=requests.get("http://api.football-data.org/v1/competitions", headers={'X-Auth-Token': key})
	response=r.json()
	for x in response:
		if x['caption']==need:
			return x['id']
           
def mainfunc(team1,team2,league):
	need_id=str(getleague(league))

	output=''

	data=pd.DataFrame(columns=['Date','TeamName', 'TeamName2', 'Home_Away', 'Goals_Team1', 'Goals_Team2', 'time_1_goals_Team1', 'time_1_goals_Team2'])
	data=byteam(team1,need_id,data)
	data,data2=addcolumn(data,'home')
	output=team1

	output_1,ls_for_export_1=printall(data)
	output=output+'\n'+output_1

	output_2,ls_for_export_2=printall(data2)
	output=output+'\n'+output_2

	data=pd.DataFrame(columns=['Date','TeamName', 'TeamName2', 'Home_Away', 'Goals_Team1', 'Goals_Team2', 'time_1_goals_Team1', 'time_1_goals_Team2'])
	data=byteam(team2,need_id,data)
	data,data2=addcolumn(data,'away')
	output=output+'\n'+team2

	output_3,ls_for_export_3=printall(data)
	output=output+'\n'+output_3

	output_4,ls_for_export_4=printall(data2)
	output=output+'\n'+output_4

	export_pd=pd.DataFrame(columns=['Bet',team1+' all matches',team1+' home matches',team2+' all matches',team2+' away matches'])
	ls_name_export=['Win','Loss','Draw','1X','X2','-',
'Total 1.5','Total 2.5','Total 3.5','-',
'Total 1T 0.5','Total 1T 1.5','Total 2T 0.5','Total 2T 1.5','-',
'Total 1T>2T','Total 2T>1T','Total 1T=2T','-',
'Team1 Total 1T 0.5','Team1 Total 1T 1.5','Team1 Total 2T 0.5','Team1 Total 2T 1.5','-',
'Team2 Total 1T 0.5','Team2 Total 1T 1.5','Team2 Total 2T 0.5','Team2 Total 2T 1.5','-',
'Team 1 Total 1T>2T','Team 1 Total 2T>1T','Team 1 Total 1T=2T','-',
'Team 2 Total 1T>2T','Team 2 Total 2T>2T','Team 2 Total 1T=2T']
	z=0
	z1=0
	for x in ls_name_export:
		if x=='-':
			export_pd.loc[z]=['-','-','-','-','-']
		else:
			export_pd.loc[z]=[x,ls_for_export_1[z1],ls_for_export_2[z1],ls_for_export_3[z1],ls_for_export_4[z1]]
			z1+=1
		z+=1
	render_mpl_table(export_pd, header_columns=0, col_width=4.0)
	return output

key='644aa8f8c2e74a0d8a30523677bfa6de'
def getallleague():
	r=requests.get("http://api.football-data.org/v1/competitions", headers={'X-Auth-Token': key})
	response=r.json()
	output=''
	for x in response:
		output=output+'\n'+x['caption']
	return output

def allcomands(need):
	r=requests.get("http://api.football-data.org/v1/competitions", headers={'X-Auth-Token': key})
	response=r.json()
	for x in response:
		if x['caption']==need:
			need_id=str(x['id'])
			break

	r=requests.get('http://api.football-data.org/v1/competitions/'+need_id+'/teams', headers={'X-Auth-Token': key})
	response=r.json()
	output=''
	for x in response['teams']:
		output=output+'\n'+x['name']
	return output
