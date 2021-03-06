import argparse
import copy
import functools
import json
import logging
import os
import subprocess
import sys

import six

from .pushd import pushd

__all__ = ['main', 'fill_json']
logger = logging.getLogger('jtb')
logger.setLevel(logging.DEBUG if os.environ.get('JTB_DEBUG') else logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.handlers[0].setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s'))
logger.handlers[0].setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Simple json builder from json template.')
    parser.add_argument('template_file', type=argparse.FileType('r'))

    parser.add_argument('--parameters', action='append', default=[])
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    content = json.load(args.template_file)
    params = {}
    for p in args.parameters:
        try:
            params = json.loads(p)
        except:
            for arg in p.split(','):
                name, value = arg.split('=', 1)
                params[name.strip()] = value.strip()

    path = '.'
    if hasattr(args.template_file, 'name'):
        path = args.template_file.name
    with pushd(path):
        result = fill_json(content, (), params)
    json.dump(result, args.output)


def fill_json(template, args, kwargs):
    same_args = functools.partial(fill_json, args=args, kwargs=kwargs)
    logger.debug('Got args: %s', kwargs)

    if isinstance(template, six.string_types):
        return template.format(*args, **kwargs)

    elif isinstance(template, dict):
        if 'JTBTemplate' in template:
            sub_template_name = template['JTBTemplate']
            logger.debug('Current dir: %s', os.getcwd())
            with open(sub_template_name, 'r') as f:
                sub_template = json.load(f)
            new_kwargs = copy.deepcopy(kwargs)
            new_kwargs.update(template)
            with pushd(sub_template_name):
                return fill_json(sub_template, args=args, kwargs=new_kwargs)
        elif 'JTBEval' in template:
            return subprocess.getoutput(template['JTBEval'])
        return {same_args(k): same_args(v) for k, v in template.items()}

    elif isinstance(template, list):
        return [same_args(v) for v in template]

    return template
