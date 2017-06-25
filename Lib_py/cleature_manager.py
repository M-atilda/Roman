# -*- coding:utf-8 -*-

import random
import copy
import threading
import time

import Lib_py.params as params
from Lib_py.page_info import *
from Lib_py.client_util import get_src, get_urls_list
from Lib_py.str_management import *


def cleature_factory(first_str):
    return Cleature_operator(Cleature(first_str))

def cleature_info2str(co):
    result_str = ""
    next_strs_l = co.get_next_search_targets_list()
    body_lll = co.get_body_structure()
    return (next_strs_l.__str__(), body_lll.__str__())

class Cleature_operator:
    def __init__(self, cl):
        self._cleature_o = cl
        self._is_alive_b = True

    def get_next_search_targets_list(self):
        return self._cleature_o.search_target_l
    def get_body_structure(self):
        return self._cleature_o.get_cleature_body()
    def add_search_target(self, new_str):
        self._cleature_o.add_search_target(new_str)
        
    def prompt_growth(self):
        try:
            #TODO:
            search_target = self._cleature_o.get_next_search_target()
            urls_l = get_urls_list(search_target) # [(host_url, full_url)]
            if len(urls_l) == 0:
                raise Exception("no result found about the word <{}>".format(search_target))
            target_info = urls_l[random.randrange(len(urls_l))]
            print("########## for debug ##########")
            print(target_info)
            html_src = get_src(target_info[1])

            colors = get_page_colors(html_src[1], target_info[0]) # all src
            feed_colors = []
            if colors == []:
                raise Exception("no css found")
            else:
                feed_colors = colors[:random.randrange(len(colors))]
            vector = decide_vector(html_src[0]) # only header
            for color in feed_colors:
                self._cleature_o.grow(color, vector)
            print("[[[[[[[[[[ growth ]]]]]]]]]]")
            next_search_candidate = get_next_search_candidate(html_src[1])
            if next_search_candidate in study.get_encoding_error_words_list():
                raise Exception("maybe encoding failed")
            self._cleature_o.add_search_target(next_search_candidate)
            print("\n\
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\
target\n\
    word      : {}\n\
    host_name : {}\n\
    url       : {}\n\
growth\n\
    colors    : {}\n\
    vector    : {}\n\
    nexts     : {}\n\
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\
".format(search_target, target_info[0], target_info[1], feed_colors, vector, next_search_candidate))
            self._cleature_o.life = max(self._cleature_o.life+1, params.life())

        except Exception as e:
            self._cleature_o.life = self._cleature_o.life - 1
            if self._cleature_o.life < 0:
                self._is_alive_b = False
            print("exception occured in growing process : {}".format(e.__str__()))
    def is_alive(self):
        return self._is_alive_b

class Cleature:
    def __init__(self, first_str):
        self.search_target_l = [first_str]
        self.body_structure_lll = [[[0 for i in range(params.x_length())]\
                                    for j in range(params.y_length())]\
                                   for k in range(params.z_length())]
        # first core block
        self.body_structure_lll\
            [params.z_length() // 2]\
            [params.y_length() // 2]\
            [params.x_length() // 2] = '#ffffff'
        self.last_grew_pos_l = [params.x_length() // 2, params.y_length() // 2, params.z_length() // 2]

        self.life = params.life()

    def get_cleature_body(self):
        return self.body_structure_lll
        
    def get_next_search_target(self):
        index = random.randrange(len(self.search_target_l))
        return self.search_target_l[index]

    def add_search_target(self, new_str):
        self.search_target_l.append(new_str)
        if len(self.search_target_l) > params.cache_amount():
            del self.search_target_l[0]

    def grow(self, color, vector):
        if (self.last_grew_pos_l[0] + vector[0]) > params.x_length() - 1:
            vector[0] = 0
        if (self.last_grew_pos_l[1] + vector[1]) > params.y_length() - 1:
            vector[1] = 0
        if (self.last_grew_pos_l[2] + vector[2]) > params.z_length() - 1:
            vector[2] = 0
        
        self.body_structure_lll\
            [self.last_grew_pos_l[0] + vector[0]]\
            [self.last_grew_pos_l[1] + vector[1]]\
            [self.last_grew_pos_l[2] + vector[2]] = color
        self.last_grew_pos_l = [\
                                self.last_grew_pos_l[0] + vector[0],\
                                self.last_grew_pos_l[1] + vector[1],\
                                self.last_grew_pos_l[2] + vector[2]]


class CleatureManager:
    co_l = []
    _cut = None

    class CleatureUpdateThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.lock = threading.Lock()
        def run(self):
            while True:
                temp_co_l = copy.deepcopy(CleatureManager.co_l)
                for copy_c in temp_co_l:
                    copy_c.prompt_growth()
                with self.lock:
                    CleatureManager.co_l = temp_co_l
                    wait_time = (params.loop_time() / 2) + random.randrange(params.loop_time())
                time.sleep(wait_time)

    
    def __init__(self):
        CleatureManager._cut = CleatureManager.CleatureUpdateThread()
        CleatureManager._cut.start()

    def get_cleatures_info_str(self):
        result_str = "var cleature_num = {};\n".format(len(CleatureManager.co_l))
        next_targets_list_str = " "
        bodys_list_str = " "
        for (i, c) in enumerate(CleatureManager.co_l):
            result = cleature_info2str(c)
            next_targets_list_str = next_targets_list_str + result[0] + ","
            bodys_list_str = bodys_list_str + result[1] + ","

        result_str = result_str + "var next_search_words_l = [{}];\n".format(next_targets_list_str[:-1])
        result_str = result_str + "var body_structures_l = [{}];\n".format(bodys_list_str[:-1])
        return result_str

    def feed_cleature(self, index, new_str):
        if index == -1:
            CleatureManager.co_l.append(cleature_factory(new_str))
        else:
            CleatureManager[index].add_search_target(new_str)
