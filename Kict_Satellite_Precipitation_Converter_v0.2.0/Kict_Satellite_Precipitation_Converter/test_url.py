import urllib.request

res = urllib.request.Request('ftp://rainmap:Niskur+1404@hokusai.eorc.jaxa.jp/standard/v8/hourly/2014/03/01')
try: 
    with urllib.request.urlopen(res) as response:
        data = response.read()
        print(data.decode('utf-8'))
except urllib.error.URLError as e:
    print(e.reason)