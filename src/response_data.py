from src.services import get_slug


class Response:
    def __init__(self, response_data: bytes,  *args, **kwargs):
        self._data = self._split_data(response_data)

    @staticmethod
    def _split_data(response_data):
        try:
            data = response_data.split()
            return data
        except AttributeError as e:
            raise e

    def get_pk(self):
        try:
            url = self._data[1]
            res = get_slug(url)
            return res.slug
        except IndexError as e:
            raise e

    def get_user(self):
        ...
