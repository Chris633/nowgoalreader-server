import sys
from ConfigParser import ConfigParser
from register_etcd.register import regist
from flask import Flask, request, make_response
from reader import entrance

default_encoding = 'utf-8'
reload(sys)
sys.setdefaultencoding(default_encoding)

app = Flask(__name__)
conf = ConfigParser()
conf.read("nowgoalreader_server.conf")


@app.route('/nowgoalreader/basketball/score', methods={'GET'})
def basketball_score():
    if request.args.get('europeId') is None:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>ID Parameter Error</h1>
<p>Not found parameter 'europeId'. Did you type 'europeId'?</p>
'''
    else:
        return entrance.start("basketball", "score", request.args.get('europeId'))


@app.route('/nowgoalreader/basketball/odds', methods=['GET'])
def basketball_odds():
    if request.args.get('europeId') is None or request.args.get('companyId') is None:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>ID Parameter Error</h1>
<p>Not found parameter 'europeId' or 'companyId'. Did you type 'europeId' and 'companyId'?</p>
'''
    else:
        return entrance.start("basketball", "odds", request.args.get('europeId'), request.args.get('companyId'))


@app.route('/nowgoalreader/soccer/score', methods=['GET'])
def soccer_socre():
    if request.args.get('europeId') is None:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>ID Parameter Error</h1>
<p>Not found parameter 'europeId'. Did you type 'europeId'?</p>
'''
    else:
        return entrance.start("soccer", "score", request.args.get('europeId'))


@app.route('/nowgoalreader/soccer/inplay', methods=['GET'])
def soccer_inplay():
    if request.args.get('europeId') is None or request.args.get('companyId') is None:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>ID Parameter Error</h1>
<p>Not found parameter 'europeId' or 'companyId'. Did you type 'europeId' and 'companyId'?</p>
'''
    else:
        return entrance.start("soccer", "inplay", request.args.get('europeId'), request.args.get('companyId'))


@app.route('/nowgoalreader/soccer/early', methods=['GET'])
def soccer_early():
    if request.args.get('europeId') is None or request.args.get('companyId') is None:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>ID Parameter Error</h1>
<p>Not found parameter 'europeId' or 'companyId'. Did you type 'europeId' and 'companyId'?</p>
'''
    else:
        return entrance.start("soccer", "early", request.args.get('europeId'), request.args.get('companyId'))


@app.errorhandler(404)
def not_found(error):
    return make_response('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Error</title>
<h1>Main Parameter Error</h1>
<p>You should check url:</p>
<p>'/nowgoalreader/soccer/score?europeId=***'</p>
<p>'/nowgoalreader/soccer/inplay?europeId=***&companyId=***'</p>
<p>'/nowgoalreader/soccer/early?europeId=***&companyId=***'</p>
<p>'/nowgoalreader/basketball/score?europeId=***'</p>
<p>'/nowgoalreader/basketball/odds?europeId=***&companyId=***'</p>''', 404)

if __name__ == '__main__':
    regist()
    app.run(host=conf.get("server", "host"), port=conf.get("server", "port"))