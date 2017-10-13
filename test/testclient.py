import etcd
import sys
import urllib2
from xml.dom import minidom

if __name__ == '__main__':
    ARGS = sys.argv
    client = etcd.Client(host=(('127.0.0.1', 2379), ('192.168.137.100', 2379), ('192.168.137.101', 2379), ('192.168.137.102', 2379)),
                         allow_reconnect=True)
    if len(ARGS) == 4:
        url = "http://" + client.read('nowgoalreader').value + "/nowgoalreader/" + ARGS[1] + "/" + ARGS[2] + \
              "?europeId=" + ARGS[3]
    else:
        url = "http://" + client.read('nowgoalreader').value + "/nowgoalreader/" + ARGS[1] + "/" + ARGS[2] + \
              "?europeId=" + ARGS[3] + "&companyId=" + ARGS[4]
    req = urllib2.Request(url)
    res = urllib2.urlopen(req).read()
    print res
