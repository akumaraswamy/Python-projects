""" This script parsers a cricket data xml file and writes it into json which
contains match level data.

This script was written for I590 Applied Data Science at Indiana University.
It can be modified or used for any purpose, without restriction.

"""
import xml.etree.cElementTree as xml
import json

if __name__ == "__main__":
  #HINT: This line picks the file to read
  tree = xml.parse('../data/cricket-xml-4.xml')
  root = tree.getroot()
  json_matches = {}
  for match in root:
    matchid = match.attrib['mid']
    wickets = {}
    t1 = match.attrib['Team1']
    t2 = match.attrib['Team2']
    wickets[t1] = 0
    wickets[t2] = 0
    for ball in match:
      #HINT: This line is important
      wickets[ball.attrib['bowling']] += int(ball.attrib['wickets'])
    json_matches[matchid] = {t1:wickets[t1],t2:wickets[t2]}
  
  #This section writes the above data to a JSON file
  with open('cricket-xml-4.json','w') as jsonout:
    json.dump(json_matches, jsonout, 
                    sort_keys=True,indent=2,separators=(',',': '))
