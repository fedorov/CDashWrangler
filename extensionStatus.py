from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib2, sys

def parseTable(table,extName,tableName):
  summaryHeaders = ["Build name","Config errors","Config warnings","Build errors","Build warnings","Tests failed"]
  summaryContent = []
  for row in table.findAll('tr'):
    allCols = row.findAll('td')
    for col in allCols:
      currentExtName = col.find('a',{'class':'buildinfo'})
      if currentExtName and currentExtName.getText().find(extName)>-1:
        #print row.prettify()
        buildName = allCols[1].get_text()
        configErrs = allCols[4].get_text()
        configWarn = allCols[5].get_text()
        buildErrs = allCols[7].get_text()
        buildWarn = allCols[8].get_text()
        testFails = allCols[12].get_text()

        summaryContent.append([buildName,configErrs,configWarn,buildErrs,buildWarn,testFails])

  return (summaryHeaders,summaryContent)

#f="/Users/fedorov/Downloads/tests.xml"

if len(sys.argv)!=2:
  print 'This script will report on the status of a selected Slicer extension from'
  print ' 3D Slicer extension dashboard (http://slicer.cdash.org/index.php?project=Slicer4)'
  print 'Usage:',sys.argv[0],' <name of Slicer extension>'
  sys.exit()

extensionName = sys.argv[1]

req = urllib2.Request("http://slicer.cdash.org/index.php?project=Slicer4")
resp = urllib2.urlopen(req)

print "Reading from CDash ...",
s=BeautifulSoup(resp.read())
print "done"

'''
Save CDash HTML into a readable form...
pretty=open("/Users/fedorov/Downloads/tests_pretty.xml",'w')
pretty.write(s.prettify().encode('UTF-8'))
'''

for p in s.find_all('a'):
  try:
    #print p.prettify()
    if p['class'][0] == "grouptrigger":
      assert isinstance(p.parent, object)
    else:
      continue
  except:
    continue

  table = p.parent.parent.parent.parent.parent
  #print p.get_text()
  #print table.prettify()
  (sHeader,sCont) = parseTable(table,"Reporting",p.get_text())
  if len(sCont):
    print 'Dashboard:',p.get_text()
    print tabulate(sCont,headers=sHeader)
    print
