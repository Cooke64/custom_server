import json

from services import router


@router(url=b'/')
def index():
    some_data = {'first': '<a href=/blog>link</a>',
                 'second': '<a href=/second>link</a>'}
    return json.dumps(some_data)


@router(url=b'/blog')
def blog():
    return '<h1>Hello, world and look at my code!</h1>'


@router(url=b'/second')
def blog():
    return '<h1>It`s a second page</h1>'

