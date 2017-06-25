# -*- coding:utf-8 -*-

from natto import MeCab
import collections as cl
import random
from bs4 import BeautifulSoup

import Lib_py.params as params
import Lib_py.study as study

# global instance
mc_g = MeCab('-F%m,%f[0],%h')


def get_next_search_candidate(html_src):
    target_str = get_str_from_http(html_src)
    if len(target_str) == 0:
        raise("can't extract strings from html source")
    parsed_words_l = get_words_list(target_str)
    print(parsed_words_l)
    study.dump_get_words(parsed_words_l)
    common_words_l = study.get_common_words()
    common_removed_words_l = [w for w in parsed_words_l if not w in common_words_l]
    freq_words_l = get_freq_words_list(common_removed_words_l)
    return select_next_search_word_candidate(freq_words_l)

def get_str_from_http(html_src):
    soup = BeautifulSoup(html_src)
    result_str = ""

    for target_dom in params.doms():
        for factor in soup.find_all(target_dom):
            result_str = result_str + get_row_str(factor) + " "

    if len(soup.find_all("title")) != 0:
        title = get_row_str(soup.find_all("title")[0])
        result_str = result_str + title
    return result_str

#TODO: more robust
def get_words_list(target_str):
    words = []
    for n in mc_g.parse(target_str, as_nodes=True):
        node = n.feature.split(',')
        if len(node) != 3:
            continue
        if node[1] == '名詞':
            words.append(node[0])
    return words

def get_freq_words_list(words_l):
    count_o = cl.Counter(words_l)
    freq_words_tl = count_o.most_common(params.candidate_amount())
    candidate_l = []
    for word_t in (freq_words_tl):
        candidate_l.extend([word_t[0] for i in range(word_t[1])])
    return candidate_l

def select_next_search_word_candidate(freq_words_tl):
    if len(freq_words_tl) == 0:
        return []
    return freq_words_tl[random.randrange(len(freq_words_tl))]

def get_row_str(domed):
    new_str = domed.__str__()
    while new_str.find("<") != -1:
        #remove first found bracket
        new_str = new_str[:new_str.find("<")] + " " + new_str[new_str.find(">")+1:]
    return new_str
