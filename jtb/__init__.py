import argparse
import json
import functools
import six
import copy
from .pushd import pushd

def main():
    parser = argparse.ArgumentParser(description='Simple json builder from json template.')
    parser.add_argument('template_file', type=argparse.FileType('r'))

    # parser.add_argument()

    args = parser.parse_args()
    print(args)
    content = json.load(args.template_file)
    print(content)


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


if __name__ == '__main__':
    main()
