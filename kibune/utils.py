from fastapi.encoders import jsonable_encoder
from jinja2 import Environment, Template


def get_j2_template(template_str) -> Template:
    return Template(template_str)


def render_j2_template(template: Template, **kwargs):
    env = Environment()
    env.filters["to_json"] = jsonable_encoder

    new_template = env.get_template(template)
    return new_template.render(**kwargs)
