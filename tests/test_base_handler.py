from messages.test_mes import Messages
from src.client_part_class import Nums, get_slug, BaseHandler
from src.services import validate_url, check_params

correct_url = b'/index/slug/'
method_get = b'GET'
method_post = b'POST'
url = b'/'
status_code = 200
response = b'GET /'
correct_host = '127.0.0.0'
wrong_host = '1.1.1'


def test_get_slug(make_server: BaseHandler):
    slug_data = get_slug(correct_url)
    assert slug_data.slug == b'slug', Messages.SLUG_ERROR.value
    assert slug_data.url == b'index', Messages.SLUG_ERROR.value


def test_make_headers_get(make_server: BaseHandler):
    data = make_server._make_headers(method_get, b'/')
    assert make_server.is_not_url_in_dict(url) is False
    assert data == (make_server._HEADER_OK, Nums.STATUS_OK.value)


def test_make_headers_post(make_server: BaseHandler):
    data = make_server._make_headers(method_post, b'/')
    assert data == (make_server._NOT_ALLOWED, Nums.NOT_ALLOWED.value)


def test_get_view(make_server: BaseHandler):
    assert make_server.get_view(404, url, response) == '<h1>Not found </h1>'
    assert make_server.get_view(200, url, response) == 1
    assert len(make_server.URLS) == 1


def test_validate_url():
    assert validate_url('localhost') is True
    assert validate_url(wrong_host) is False
    assert validate_url(correct_host) is True


def test_check_params():
    assert check_params(correct_host, 400) is True
