# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe as _S
from django.template import Context, Template, loader
import random
import djclick as click


def get_random_string(
    length=32,
    allowed_chars='abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  '0123456789'):
    return ''.join([random.choice(allowed_chars) for i in range(length)])


def render(src, **ctx):
    return _S(Template(src).render(Context(ctx)))


def render_by(name, **ctx):
    return _S(loader.get_template(name).render(Context(ctx)))


def echo(teml, fg="green", **kwargs):
    click.secho(render(teml, **kwargs), fg=fg)
