# from django.conf import settings
from django.http import HttpResponse    # , HttpResponseRedirect
# from django.template.response import TemplateResponse
from django.core.files import File
from django.contrib.admin.views.decorators import staff_member_required
import os
import mimetypes
import re


def _path(path):
    path = re.sub('^(.+)/_images', '_images', path)
    return os.path.join(
        os.path.dirname(__file__),
        os.path.join('build/html/', path))


def publish(request, path):
    if path == '' or path.endswith('/'):
        path = path + "index.html"

    abspath = _path(path)
    mt, dmy = mimetypes.guess_type(abspath)
    return HttpResponse(
        File(open(abspath)), content_type=mt)


@staff_member_required
def protected(request, path):
    return publish(request, path)


@staff_member_required
def help(request, module, entry):
    return publish(request, "{0}/{1}.html".format(module, entry))


def public(request, path):
    return publish(request, path)
