from server_part import Server

if __name__ == '__main__':
    server = Server('127.0.0.1', 7777, debug=True)
    server.run_server()
