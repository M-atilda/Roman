from bs4 import BeautifulSoup
import requests
import sys    

def get():
    res = requests.get("http://localhost:19767/")
    print(res.text)

def generate(target_str):
    res = requests.get("localhost:19767/index=-1&feed={}".format(target_str))
    
def feed(target_str):
    res = requests.get("localhost:19767/index.html&index=0&feed={}".format(target_str))
    

if __name__ == '__main__':
    if sys.argv[1] == "get":
        get()
    elif sys.argv[1] == "new":
        generate(sys.argv[2])
    else:
        feed(sys.argv[2])
