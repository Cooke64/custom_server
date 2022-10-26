import json
import os
import typing as t

import jinja2

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/')
)


def render_to_template(template: str, content: dict,):
    filename, file_extension = os.path.splitext(template)
    if file_extension != '.html':
        raise TypeError('Файл должен быть формата html')
    template = environment.get_template(template)
    res = template.render(
            content,
        )
    return res


def render_string(data: t.Union[int, str, dict]):
    if isinstance(data, dict):
        data = json.dumps(data)
    template = environment.from_string(data)
    return template.render()
