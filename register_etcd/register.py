import etcd
import threading
from ConfigParser import ConfigParser
import time

conf = ConfigParser()
conf.read("nowgoalreader_server.conf")


def splithost(host):
    return tuple([host.split(":")[0], int(host.split(":")[1])])
client = etcd.Client(host=tuple(map(splithost, conf.get("etcd", "hostlist").split("|"))), allow_reconnect=True)


def regist():
    while True:
        try:
            client.read('/nowgoalreader').value
        except etcd.EtcdKeyNotFound:
            client.write('/nowgoalreader', conf.get("server", "host") + ':' + conf.get("server", "port"), ttl=3)
            time.sleep(1)
            if client.read('/nowgoalreader').value == conf.get("server", "host") + ':' + conf.get("server", "port"):
                t = threading.Thread(target=refresh)
                t.setDaemon(True)
                t.start()
                break
        watch()


def refresh():
    while True:
        client.refresh('/nowgoalreader', ttl=2)
        time.sleep(1)


def watch():
    for event in client.eternal_watch('/nowgoalreader'):
        if event.action == 'expire':
            break
