from icalendar import Calendar
import re
import datetime
from datetime import date

def find_round(match_date):
    start_date = datetime.datetime(2016, 3, 24)
    #dt = match_date.replace(tzinfo=None)
    date_difference = match_date - start_date
    return date_difference.days

def parse_fixture_to_list():
    match_list = []
    g = open('fixture.ics','rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        g_list = []
        game_list = []
        if component.name == "VEVENT":
            start_date = component.decoded('DTSTART')
            match = component.get('DESCRIPTION')
            year = start_date.year
            if year == 2016:
                match = match.replace('\n', ',')
                #print match
                g_tuple = (re.split(',|\sv\s',match))
                #print g_tuple
                game_list.append(g_tuple[0])
                game_list.append(g_tuple[1])
                start_date = start_date.replace(tzinfo=None)
                game_list.append(start_date)
                match_list.append(game_list)
    g.close()
    return match_list


match_list = parse_fixture_to_list()

"""
for i in range(0,len(match_list)):
    if "Hawthorn" in match_list[i][1]:
        print "Home"
        print match_list[i]
    if "Hawthorn" in match_list[i][2]:
        print "Away"
        print match_list[i]
"""
for i in range(0,len(match_list)):
    round = find_round(match_list[i][2]) / 7 + 1
    f = open('draw.txt','a')
    print "round: "+ str(round) +" home: " + str(match_list[i][0]) +"  away: "+ str(match_list[i][1]) + "  Date: " + str(match_list[i][2])
    f.write("round: "+ "," + str(round) + "," +" home: " + "," + str(match_list[i][0]) + "," +"  away: "+ "," + str(match_list[i][1]) + "," + "  Date: " + "," + str(match_list[i][2]) + "\n")
    f.close()
    #print find_round(match_list[i][2])/7
    #for x in range(0,len(match_list[i])):
    #    print match_list[i][x]