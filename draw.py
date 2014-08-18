
try: import simplejson as json
except ImportError: import json
import urllib2
from icalendar import Calendar
import re

LADDER_URL = "http://www.sportal.com.au/feeds/sss/afl_ladder.json"

TEAMS_DICT = {
"1":'Adelaide',
"2":'Brisbane',
"3":'Carlton',
"4":'Collingwood',
"5":'Essendon',
"6":'Fremantle',
"7":'Gold Coast',
"8":'Geelong',
"9":'Hawthorn',
"10":'Melbourne',
"11":'North Melbourne',
"12":'Port Adelaide',
"13":'Richmond',
"14":'St Kilda',
"15":'Sydney',
"16":'West Coast',
"17":'Western Bulldogs',
"30":'Greater Western Sydney'
}

TEAMS_LIST = [
'Adelaide Crows',
'Brisbane Lions',
'Carlton Blues',
'Collingwood Magpies',
'Essendon Bombers',
'Fremantle Dockers',
'Gold Coast Suns',
'Geelong Cats',
'Hawthorn Hawks',
'Melbourne Demons',
'North Melbourne Kangaroos',
'Port Adelaide Power',
'Richmond Tigers',
'Saint Kilda Saints',
'Sydney Swans',
'West Coast Eagles',
'Western Bulldogs',
'Greater Western Sydney Giants'
]

def parse_fixture_to_list():
	match_list = []
	g = open('fixture.ics','rb')
	gcal = Calendar.from_ical(g.read())
	for component in gcal.walk():
	   if component.name == "VEVENT":
	   		start_date = component.decoded('DTSTART')
	   		match = component.get('DESCRIPTION')
	   		year = start_date.year
	   		if year == 2014:
				match = match.replace('\n', ',')
				match_list.append(re.split(',|\sv\s',match))
	g.close()
	return match_list

def getladder():
	req = urllib2.Request(LADDER_URL)
	req.add_header('Accept', 'application/json')
	opener = urllib2.build_opener()
	f = opener.open(req)
	data = json.load(f)

	mydata = data['ladder']
	return mydata

def get_opponet_value(team_name):
	mydata = getladder()
	team_ranks = []
	i=0
	for entry in mydata:
		team_ranks.append([str(mydata[i]['name']),str(mydata[i]['friendly_name']),mydata[i]['rank']])
		#team_ranks = mydata[i]['rank']
		i += 1
	i=0
	for entry in team_ranks:
		friendly_name = team_ranks[i][1]
		if friendly_name == 'Roos':
			friendly_name = 'Kangaroos'
		the_team_name = team_ranks[i][0]
		if the_team_name == 'Western Bulldogs':
			the_team_name = 'Western'
		if the_team_name == 'St Kilda':
			the_team_name = 'Saint Kilda'
		full_team_name = the_team_name + " " + friendly_name
		if full_team_name == team_name:
			#print team_name
			rank = team_ranks[i][2]
		i += 1
	#print team_ranks.index(team_name)
	return rank


def calculate_draw_score():
	match_list = parse_fixture_to_list()
	#TEAMS_LIS = ['Adelaide Crows']
	team_scores = []
	for team in TEAMS_LIST:
		draw_score = 0
		for i in range(0,len(match_list)):
			if team in match_list[i][1]:
				#print "GETTING - ", match_list[i][2]
				draw_score += get_opponet_value(match_list[i][2])
			if team in match_list[i][2]:
				#print "GETTING - ", match_list[i][1]
				draw_score += get_opponet_value(match_list[i][1])
		team_scores.append([team, draw_score])
		#print draw_score
	return team_scores

def sort_list(the_list):
	sorted_list = sorted(the_list, key=lambda teams: int(teams[1]))
	return sorted_list


#getladder()
#get_opponet_value('Sydney Swans')
sort_list(calculate_draw_score())
#print parse_fixture_to_list()
