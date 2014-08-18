from icalendar import Calendar
import re

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


match_list = parse_fixture_to_list()

for i in range(0,len(match_list)):
	if "Hawthorn" in match_list[i][1]:
		print "Home"
		print match_list[i]
	if "Hawthorn" in match_list[i][2]:
		print "Away"
		print match_list[i]