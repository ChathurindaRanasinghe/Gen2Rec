from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape


def process_template(template_file: str, data: Dict[str, Any]) -> str:
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template(template_file)
    return template.render(**data)
