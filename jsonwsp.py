import requests
from pprint import pprint
try:
    import json as json
except:
    import simplejson as json

class JSONWSPError(Exception):
    pass

class JSONWSP:
    """Excelent class provides awesome and pretty simple realization of jsonwsp client
    as it shown at http://en.wikipedia.org/wiki/Jsonwsp
    Usage:
      >>> cl = JSONWSP('http://localhost/mymountpoint')
      >>> cl.testmethod(arg1='testarg', arg2='test2')
      Yes, it works, testarg, test2
    """
    headers = {'Content-Type': 'application/json; charset=utf-8',
              'Accept': 'application/json' }
    def __init__(self, url):
        self.url = url
        self.funcurl = url + '/jsonwsp'
        self.desc = None
    def description(self):
        """Return dict with methods and they descriptions"""
        if self.desc == None:
            req = requests.get(self.funcurl + '/description')
            if req.ok:
                self.desc = json.loads(req.content)
                return self.desc
            raise JSONWSPError('Wrong url or something with a server')
        else:
            return self.desc
    def __iter__(self):
        return iter(self.__dir__)
    def __dir__(self):
        return self.description()['methods'].keys()        
    def __getattr__(self, name):
        def w(**args):
            req = requests.post(self.funcurl, 
                    json.dumps(dict(
                        methodname = name,
                        args = args
                    )),
                    headers = self.headers)
            if req.ok:
                try:
                    q = json.loads(req.content)
                    return q['result']
                except ValueError:
                    raise JSONWSPError('Error on a server side\n' + req.content)
        return w

if __name__ == '__main__':
    cl = JSONWSP('http://127.0.0.1:8090/EpubBuilder')
    print dir(cl)
