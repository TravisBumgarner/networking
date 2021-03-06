import socket

from utils import pretty_print_message, Request
from url import get_body_content

class Server:
    def __init__(
            self,
            host='0.0.0.0',  # Empty string so we can receive requests from other computers, use 0.0.0.0 for localhost
            desired_port=8000,
            max_listen_queue=5
    ):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        is_no_port = True
        while is_no_port:
            try:
                self.socket.bind((host, desired_port))
                is_no_port = False
                print('Bound to {} on port {}'.format(host, desired_port))

            except OSError:
                desired_port += 1

        self.socket.listen(max_listen_queue)
        self.listen()

    def listen(self):
        print('Listening...')
        try:
            while True:
                try:
                    conn, addr = self.socket.accept()
                    print('\nConnection received from {}'.format(addr))

                    is_connected = True

                    while is_connected:
                        request = conn.recv(1024)
                        if request:
                            pretty_print_message('Request', request)
                            r = Request(request_byte_str=request)
                            print(r)

                            headers = {}
                            body = get_body_content(r)

                            response = self.format_response(headers=headers, body=body)
                            pretty_print_message('Response', response)
                            conn.sendall(response)
                            is_connected = False

                finally:
                    conn.close()
                    print('\nClosing connection from {}'.format(addr))

        except KeyboardInterrupt:
            print('\nClosing Socket')
            self.socket.close()

        finally:
            print('\nClosing Socket')
            self.socket.close()

    def format_response(self, status_code='200 OK', protocol='HTTP/1.1', headers={}, body=''):
        response = "{} {}\r\n".format(protocol, status_code)
        for h in headers.keys():
            response += "{}: {}\r\n".format(h, headers[h])
        response += '\r\n'
        response += body
        return str.encode(response)


