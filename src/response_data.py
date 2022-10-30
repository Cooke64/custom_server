

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
            return self._data[1]
        except IndexError as e:
            raise e

    def get_user(self):
        ...
