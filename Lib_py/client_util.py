# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

import Lib_py.params as params

def get_src(target_url):
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text)
    return (res.headers, res.text)

def get_urls_list(word_str):
    url_l = []
    #res = requests.get("http://search.yahoo.co.jp/search?p={}&amp;ei=UTF-8".format(word_str))
    res = requests.get("https://www.google.co.jp/search?q={}".format(word_str))
    print("-----------------------------------------------------------------")
    print("search results <{}>".format(word_str))
    soup = BeautifulSoup(res.text)
    refs = soup.find_all("a")
    for ref in refs:
        ref = ref.__str__()
        if ref.find("url?q=") == -1 or ref.find("class=") != -1:
            continue
        print(ref)
        is_non_trivial = True
        for w in params.trivial_words():
            if ref.find(w) != -1:
                is_non_trivial = False
        if is_non_trivial:
            target_url = ref[ref.find("url?q=")+6:ref.find("&amp;")]
            new_url_data = (target_url[:8+target_url[8:].find("/")+1], target_url)
            url_l.append(new_url_data)
            print(new_url_data)
    print("-----------------------------------------------------------------")
    return url_l
