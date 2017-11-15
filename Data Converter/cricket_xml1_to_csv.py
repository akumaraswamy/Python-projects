""" This script parsers a cricket data xml file and writes it into a csv file
which contains match level data.

This script was written for I590 Applied Data Science at Indiana University. 
It can be modified or used for any purpose, without restriction.

"""
import xml.etree.cElementTree as xml
import csv

if __name__ == "__main__":
  #HINT: This line picks the file to read
  tree = xml.parse('../data/cricket-xml-1.xml')
  root = tree.getroot()
  csv_matches = []
  for match in root:
    matchid = match.attrib['mid']
    runs = {}
    t1 = match.attrib['Team1']
    t2 = match.attrib['Team2']
    runs[t1] = 0
    runs[t2] = 0
    for ball in match:
      #HINT: This line is important
      runs[ball.attrib['batting']] += int(ball.attrib['runs'])
    csv_matches.append([matchid,t1,runs[t1],t2,runs[t2]])
  
  #This section writes the above data to a CSV file  
  with open('cricket-xml-1.csv','wb') as csvout:
    cric_writer = csv.writer(csvout)
    cric_writer.writerow(["id","team1","t1runs","team2","t2runs"])
    cric_writer.writerows(csv_matches)   
