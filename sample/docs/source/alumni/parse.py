from docutils.core import publish_doctree
import sys
from bs4 import BeautifulSoup as Soup
import yaml
import json


def to_yaml(result):
    # YAML
    print yaml.dump(
        yaml.load(json.dumps(result)), default_flow_style=False,
        allow_unicode=True)


def to_json(result):
    # JSON
    print json.dumps(result, ensure_ascii=False, indent=2)


def to_source(rows):
    print "#", ", ".join(['u"%s"' % s for s in rows[0]])
    for row in rows[1:]:
        print "[", ", ".join(['u"%s"' % s for s in row]), "],"

doctree = publish_doctree(open(sys.argv[1]).read())
dom = doctree.asdom()
soup = Soup(dom.toprettyxml(encoding='utf8'))

rows = []
for row in soup.select('tbody row'):
    rows.append([
        e.select('paragraph') and e.select('paragraph')[0].text or ''
        for e in row.select('entry')])

result = []
for row in rows[1:]:
    result.append(dict(zip(rows[0], row)))

to_source(rows)
