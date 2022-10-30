from src.client_part_class import BaseHandler

if __name__ == '__main__':
    from views.test_views import *
    client = BaseHandler('127.0.0.1', 8000, False)
    client()

