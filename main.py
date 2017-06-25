# -*- coding:utf-8 -*-

import threading
import time
import copy
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import os

from Lib_py.cleature_manager import cleature_factory, cleature_info2str, CleatureManager
import Lib_py.params as params



g_first_html_src = ""
g_latter_html_src = ""
g_middle_html_src = ""
with open('Public/Html/index_first.html') as f:
    for line in f:
        g_first_html_src = g_first_html_src + line
with open('Public/Html/index_middle.html') as f:
    for line in f:
        g_middle_html_src = g_middle_html_src + line        
with open('Public/Html/index_latter.html') as f:
    for line in f:
        g_latter_html_src = g_latter_html_src + line
g_cleature_manager = CleatureManager()


#TODO:
def generate_tab_contents(num):
    return "<div id=\"canvas-frame_{}\"></div>".format(num)

def make_tabs_html_src(length):
    result = ""
    for i in range(length):
        result = result + "<div class=\"slide\" data-anchor=\"slide{}\">{}</div>\n".format(i+1, generate_tab_contents(i+1))
    return result

class MyRequestHandler(SimpleHTTPRequestHandler):
    global g_first_html_src
    global g_latter_html_src
    global g_cleature_manager
    
    def do_GET(self):
        try:
            # get query string and parse it
            print("[INFO] path  : {}".format(self.path))

            # contents generation phase
            body = bytes("", 'utf-8')
            content_type = ''
            if self.path.find(".css") + self.path.find(".js") != -2 and self.path.find("&feed=") == -1:
                print("[INFO] provide none html file")
                server_top_path = os.getcwd()
                print("[INFO] " + server_top_path + self.path)
                
                try:
                    f = open(server_top_path + self.path, 'r')
                    body = body + bytes(f.read(), 'utf-8')
                except Exception:
                    print("[ERROR] file not found")
                    err_message = bytes("file not found", 'utf-8')
                    self.send_response(404)
                    self.send_header('Content-type', 'text/plain')
                    self.send_header('Content-length', len(err_message))
                    self.end_headers()
                    self.wfile.write(err_message)
                    return
                    
                if self.path.find(".css") != -1:
                    content_type = 'text/css'
                else:
                    content_type = 'text/javascript'
            else:
                body = bytes(g_first_html_src +\
                             g_cleature_manager.get_cleatures_info_str() +\
                             g_middle_html_src +\
                             make_tabs_html_src(g_cleature_manager.get_cleatures_amount()) +\
                             g_latter_html_src, 'utf-8')
                content_type = 'text/html'

            # respond phase
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', len(body))
            self.end_headers()
            self.wfile.write(body)

            
        except Exception as e:
            print("[ERROR] exception occured : {}".format(e.__str__()))
            err_message = bytes("server internal error occured in GET request : {}".format(e.__str__()), 'utf-8')
            self.send_response(403)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-length', len(err_message))
            self.end_headers()
            self.wfile.write(err_message)
            return
            

        target_index = -1
        target_str = ""
        if self.path.find("index=") < self.path.find("feed="):
            target_index = self.path[self.path.find("index=")+6:self.path.find("&feed=")]
            target_str = self.path[self.path.find("feed=")+5:]
            g_cleature_manager.feed_cleature(int(target_index), target_str)
        elif self.path.find("feed=") < self.path.find("index="):
            target_index = self.path[self.path.find("index=")+6:]
            target_str = self.path[self.path.find("feed=")+5:self.path.find("&index=")]
            g_cleature_manager.feed_cleature(int(target_index), target_str)


        
if __name__ == '__main__':
    host = 'localhost'
    port = 19767
    Handler = MyRequestHandler
    server = HTTPServer((host, port), MyRequestHandler)
    print("[INFO] serving at the port {}".format(port))
    server.serve_forever()
