from render.deal_template import render_to_template, render_string
from src.client_part_class import Router
from src.response_data import Response

router = Router()


@router.view_router(url=b'/')
def index(response: Response):
    some_data = {'first': '<a href=/blog>link</a>',
                 'second': '<a href=/second>link</a>',
                 }
    return render_string(some_data)


@router.view_router(url=b'/blog')
def blog(response: Response):
    res = [1, 2, 3, 4]
    my_dict = {
        'name': 'Pablo',
        'reaction': 'good',
        'res': res
    }

    return render_to_template('blog.html', content=my_dict)


@router.view_router(url=b'/second')
def second(response: Response):
    data = '<h1>It`s  second page</h1>'
    return render_string(data)


@router.view_router(url=b'/third/<slug>')
def third(response: Response):
    third.kwarg = 123
    data = '<h1>It`s  second page</h1>'
    return render_string(data)
