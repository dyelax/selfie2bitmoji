import requests
import shutil


url = 'https://render.bitstrips.com//render/6688424/122369389_1_s4-v1.png'
for i in xrange(1000):
    print i
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('data/', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print r.status_code