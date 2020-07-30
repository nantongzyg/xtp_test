import urllib2
import time

def get_data(url):
	u = urllib2.urlopen(url)
	return u.read()

if __name__ == '__main__':
	#print get_data('http://10.25.24.47:8080/localtime')
	#print get_data('http://10.25.24.47:8080/hello?name=sc')
	print get_data('http://10.25.24.47:8080/localexec?dir=MOCK&execfile=sse_mock_xtp2.exe')
	time.sleep(1)
	print get_data('http://10.25.24.47:8080/localexec?dir=MOCK&execfile=stopssemock.bat')
	time.sleep(1)
	print get_data('http://10.25.24.47:8080/localexec?dir=xogwsh-release&execfile=startxogwsh.bat')
	time.sleep(1)
	print get_data('http://10.25.24.47:8080/localexec?dir=xogwsh-release&execfile=stopxogwsh.bat')
