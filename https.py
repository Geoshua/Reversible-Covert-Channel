'''from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certthesis.crt','certthesis.key')
context.check_hostname = False

with HTTPServer(("localhost", 4443), SimpleHTTPRequestHandler) as httpd:
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import ssl
import optparse

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='')
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()

hostname = options.ip  # '127.0.0.1'
port = options.port  # 443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certthesis.crt','certthesis.key')

print('Loaded certificate and key..')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    print('Socket starting..')
    sock.bind((hostname, port))
    sock.listen(25)
    with context.wrap_socket(sock, server_side=True) as ssock:
        print('Socket connection established!')
        (conn, addr) = ssock.accept()

        f = open('server_output.txt', 'w')

        while True:
            message = conn.recv()
            if not message:
                break

            # message = message.decode()

            f.write('%s: %s\n' % (addr, message))
            f.flush()

            # print(message)
