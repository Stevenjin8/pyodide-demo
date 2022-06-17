"""We need to add an extra header to allow CORS. Copied and pasted from
this post https://stackoverflow.com/questions/12499171/can-i-set-a-header-with-pythons-simplehttpserver
"""

from http import server 

class MyHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()

        server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")


if __name__ == '__main__':
    server.test(HandlerClass=MyHTTPRequestHandler)