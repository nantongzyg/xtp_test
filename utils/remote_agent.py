import time
import os
import json

_hello_resp = '''\
<html>
	<head>
		<title>Hello {name}</title>
	</head>
	<body>
		<h1>Hello {name}</h1>
	</body>
</html>'''

def hello_world(environ, start_response):
	start_response('200 ok', [ ('Content-type', 'text/html')])
	params = environ['params']
	resp = _hello_resp.format(name=params.get('name'))
	yield resp.encode('utf-8')

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
	<year>{t.tm_year}</year>
	<month>{t.tm_mon}</month>
	<day>{t.tm_mday}</day>
	<hour>{t.tm_hour}</hour>
	<minute>{t.tm_min}</minute>
	<second>{t.tm_sec}</second>
</time>'''

def localtime(environ, start_response):
	start_response('200 OK', [('Content-type', 'application/xml')])
	resp = _localtime_resp.format(t=time.localtime())
	yield resp.encode('utf-8')


def localexec(environ, start_response):
	start_response('200 OK', [('Content-type', 'text/html')])
	params = environ['params']
	output = os.popen(params.get('order'))
	_localexec_resp = {}
	_localexec_resp['status'] = 0 
	_localexec_resp['content'] = output.read()
	resp = json.dumps(_localexec_resp, indent=2)
	yield resp.encode('utf-8')

if __name__ == '__main__':
	from resty import PathDispatcher
	from wsgiref.simple_server import make_server

	dispatcher = PathDispatcher()
	dispatcher.register('GET', '/hello', hello_world)
	dispatcher.register('GET', '/localtime', localtime)
	dispatcher.register('GET', '/localexec', localexec)

	httpd = make_server('', 8080, dispatcher)
	print 'Serving on port 8080...'
	httpd.serve_forever()