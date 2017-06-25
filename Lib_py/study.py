# -*- coding:utf-8 -*-

import Lib_py.params as params


def get_common_words():
    result = []
    with open("Res/common_words.txt", 'r') as f:
        for line in f:
            result.append(line[:line.find("[")])
    return result

def dump_get_words(words_list):
    with open("Res/recent_log.txt", 'a') as f:
        dump_str = "**************************************"
        for w in words_list:
            dump_str = dump_str + w + "\n"
        f.write(dump_str[:-1])
        
def get_encoding_error_words_list():
    return params.encoding_error_candidates()
        
def learn_common_words():
    common_words_tl = []
    with open("Res/common_words.txt", 'r') as commons_f:
        for line in commons_f:
            try:
                common_words_tl.append((line[:line.find("[")], int(line[line.find("[")+1:line.find("]")])))
            except:
                continue
        with open("Res/recent_log.txt", 'r') as f:
            pass

        
if __name__ == '__main__':
    learn_common_words()
        
