from src.client_part_class import WorkServer, URLS

if __name__ == '__main__':
    client = WorkServer('127.0.0.1', 7777, debug=False)
    client.run_server()
