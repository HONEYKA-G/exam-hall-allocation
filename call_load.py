import urllib.request

url = 'http://127.0.0.1:5000/admin/load_sample'
with urllib.request.urlopen(url, timeout=10) as r:
    data = r.read().decode('utf-8')
    print(data)
