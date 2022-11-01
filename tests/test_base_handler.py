from messages.test_mes import Messages
from src.client_part_class import BaseHandler, Nums, Router

base = BaseHandler()
router = Router()

correct_url = b'index/slug/'
method_get = b'GET'
method_post = b'POST'
url = b'/'
status_code = 200
response = b'GET /'


def func(resp):
    return 1


def test_get_slug():
    slug = base._get_slug(correct_url)
    assert isinstance(slug, tuple) is True, Messages.SLUG_ERROR.value


def test_make_headers_get():
    base.URLS[url] = (func, b'GET')
    data = base._make_headers(method_get, b'/')
    assert base.is_not_url_in_dict(url) is False
    assert data == (base._HEADER_OK, Nums.STATUS_OK.value)


def test_make_headers_post():
    base.URLS[url] = (func, b'GET')
    data = base._make_headers(method_post, b'/')
    assert data == (base._NOT_ALLOWED, Nums.NOT_ALLOWED.value)


def test_get_view():
    base.URLS[url] = (func, b'GET')
    assert base.get_view(404, url, response) == '<h1>Not found </h1>'
    assert base.get_view(200, url, response) == 1


def test_check_decorator():
    assert router.check_decorator() is True
