# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from Lib_py.client_util import get_src
import requests
import random


def get_page_colors(html_src, host_url):
    colors = []

    space_exist_index = html_src.find("color: #")
    non_space_index = html_src.find("color:#")
    if space_exist_index != -1:
        colors.append(html_src[space_exist_index+7:space_exist_index+14])
    if non_space_index != -1:
        colors.append(html_src[non_space_index+6:non_space_index+13])    

    soup = BeautifulSoup(html_src)
    css_l = [link.__str__() for link in soup.find_all("link") if (link.find(".css") != -1)]
    css_l = [link for link in css_l if (len(link) != 0) and (link.find(".css") != -1) and (len(link) < 300)]
    template_css_url_l = [link[link.find("href=\"")+6:link.find(".css")+4] for link in css_l if (link.find("http") != -1) and (link.find("http") != None)]
    normal_css_url_l = [link for link in css_l if (link.find("http") == -1)]
    css_urls_l = [host_url + link_str[link_str.find("href=\"")+6:link_str.find(".css")+4] for link_str in normal_css_url_l]
    css_urls_l.extend(template_css_url_l)

    print("(((((((((( {} ))))))))))".format(css_urls_l))
    def is_color_scheme(color_scheme_candidate):
        #NOTE: ignore #000 and #fff
        color_scheme_candidate_str = color_scheme_candidate.__str__()
        if ';' in color_scheme_candidate_str:
            return False
        for c in color_scheme_candidate_str[1:]:
            if ('0' <= c <= '9') or ('a' <= c <= 'f') or ('A' <= c <= 'F'):
                continue
            else:
                return False
        return True

    for url in css_urls_l:
        css_res = requests.get(url).text.__str__()
        space_exist_index = css_res.find("color: #")
        non_space_index = css_res.find("color:#")
        while space_exist_index + non_space_index != -2:
            if len(colors) > 10:
                break
            color_candidate = ""
            if max(space_exist_index+15, non_space_index+14) > len(css_res):
                break
            if space_exist_index != -1:
                color_candidate = css_res[space_exist_index+7:space_exist_index+14]
                if is_color_scheme(color_candidate):
                    colors.append(color_candidate)
                css_res = css_res[space_exist_index+15:]
            if non_space_index != -1:
                color_candidate = css_res[non_space_index+6:non_space_index+13]
                if is_color_scheme(color_candidate):
                    colors.append(color_candidate)
                css_res = css_res[non_space_index+14:]
            space_exist_index = css_res.find("color: #")
            non_space_index = css_res.find("color:#")
    print(colors)
    return colors
    
def decide_vector(header_info, num):
    results = []
    if len(header_info) < 3:
        raise Exception("lack of header information")
    for i in range(num):
        result = [1, 1, 1]
        if (len(header_info) % 2) == 0:
            result[0] = -1
        val_l = list(header_info.values())
        if len(header_info) == 0:
            return result
        if (random.randrange(len(val_l[random.randrange(len(header_info))])) % 2) == 0:
            result[1] = -1
        key_l = list(header_info.keys())
        if (random.randrange(len(key_l[random.randrange(len(header_info))])) % 2) == 0:
            result[2] = -1
        results.append(result)
    print("$$$$$$$$$$ {} $$$$$$$$$$".format(results))
    return results
