from render.deal_template import render_to_template, render_string
from src.client_part_class import BaseHandler
import json

from src.client_part_class import Router

router = Router()

if __name__ == '__main__':

    @router.view_router(url=b'/')
    def index():
        some_data = {'first': '<a href=/blog>link</a>',
                     'second': '<a href=/second>link</a>'}
        return render_string(some_data)


    @router.view_router(url=b'/blog')
    def blog():
        my_dict = {
            'name': 'Pablo',
            'reaction': 'good',
        }
        return render_to_template('blog.html', content=my_dict)


    @router.view_router(url=b'/second')
    def second():
        data = '<h1>It`s  second page</h1>'
        return render_string(data)


    client = BaseHandler('127.0.0.1', 8000, debug=False)
    client()
