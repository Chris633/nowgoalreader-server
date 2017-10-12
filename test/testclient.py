import urllib2
from xml.dom import minidom
url = "http://localhost:5000/nowgoalreader/basketball/score?europeId=289772"

req = urllib2.Request(url)
res = urllib2.urlopen(req).read()
dom = minidom.parseString(res)
print dom.getElementsByTagName('item')
