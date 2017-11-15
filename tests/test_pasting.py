import unittest
from jtb import fill_json


class TestBuilding(unittest.TestCase):
    def test_with_subtemplate(self):
        import json
        with open('template.json', 'r') as f:
            data = json.load(f)
        result = fill_json(data, (), dict(Title='Main Title', Prefix='Some Blog', dynamic='content'))
        self.assertEqual(result, {
            'title': 'Some Blog - Main Title',
            'content': [
                {'title': 'Some Blog - red page', 'color': 'red'},
                {'title': 'Some Blog - green page', 'color': 'green'}
            ]})
