import urllib.request, urllib.parse
data = {
    "index": -1,
    "feed": "test"
}

data = urllib.parse.urlencode(data).encode("utf-8")
with urllib.request.urlopen("http://localhost:19767/", data=data) as res:
    result = res.read().decode("utf-8")
    print(result)
