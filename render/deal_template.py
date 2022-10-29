import json
import os

import jinja2


environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/')
)


def get_extension(template: str) -> str:
    _, file_extension = os.path.splitext(template)
    return file_extension


def check_template(template: str) -> bool | None:
    match get_extension(template):
        case '.html':
            return True
        case _:
            raise TypeError('Файл должен быть формата html')


def render_to_template(template: str, content: dict, ):
    if check_template(template):
        template = environment.get_template(template)
        return template.render(content)


def render_string(data: int | str | dict):
    if isinstance(data, dict):
        data = json.dumps(data)
    template = environment.from_string(data)
    return template.render()
