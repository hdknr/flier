# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
from django.core import serializers

import djclick as click
from flier.utils import echo
from flier.ses import models
from logging import getLogger

logger = getLogger('flier')
translation.activate(settings.LANGUAGE_CODE)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--id', '-i')
@click.option('--limit', '-l', default=20)
@click.pass_context
def sources(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Source.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))
