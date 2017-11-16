import argparse
import copy
import functools
import json
import logging
import sys

import six

from .pushd import pushd

__all__ = ['main', 'fill_json']
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Simple json builder from json template.')
    parser.add_argument('template_file', type=argparse.FileType('r'))

    parser.add_argument('--parameters')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    content = json.load(args.template_file)
    params = {}
    if args.parameters:
        logging.info('Got args: %s', args.parameters)
        try:
            params = json.loads(args.parameters)
        except:
            for arg in args.parameters.split(','):
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

    if isinstance(template, six.string_types):
        return template.format(*args, **kwargs)

    elif isinstance(template, dict):
        if 'JTBTemplate' in template:
            sub_template_name = template['JTBTemplate']
            with open(sub_template_name, 'r') as f:
                sub_template = json.load(f)
            new_kwargs = copy.deepcopy(kwargs)
            new_kwargs.update(template)
            with pushd(sub_template_name):
                return fill_json(sub_template, args=args, kwargs=new_kwargs)
        return {same_args(k): same_args(v) for k, v in template.items()}

    elif isinstance(template, list):
        return [same_args(v) for v in template]
