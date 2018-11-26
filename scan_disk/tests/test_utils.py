#! /usr/bin/env python3

import pathlib
import sys
import unittest

file_path = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(file_path))

from scan_disk.utils import *


class UtilsTestCase(unittest.TestCase):
    """
        Checks the methods of the utils class.
    """
    def test_01_yaml_to_dict_ok(self):
        print('test 1')
        path = file_path / 'scan_disk' / 'tests' / 'data' / 'test.yml'
        expect = 'version'
        result = yaml_to_dict(path)
        self.assertIn(expect, result)

    def test_02_yaml_to_dict_ko(self):
        print('test 2')
        expect = 'erreur'
        path = file_path / 'scan_disk' / 'tests' / 'data' / 'tet.yml'
        result = yaml_to_dict(path)
        self.assertIn(expect, result)

    def test_03_render_template_ok_1(self):
        print('test 3')
        templ = '@template.j2'
        template_path = file_path / 'scan_disk' / 'tests' / 'data'
        kwargs = {'nom': 'Einstein', 'prenom': 'Albert'}
        expect = 'Bonjour Einstein Albert'
        result = render_templates(
            tmpl=templ,
            template_path=template_path,
            **kwargs)
        self.assertEqual(expect, result)

    def test_04_render_template_ok_2(self):
        print('test 4')
        templ = 'Bonjour {{ nom }} {{ prenom }}'
        kwargs = {'nom': 'Einstein', 'prenom': 'Albert'}
        expect = 'Bonjour Einstein Albert'
        result = render_templates(
            tmpl=templ,
            **kwargs)
        self.assertEqual(expect, result)

    def test_05_render_template_ko(self):
        print('test 5')
        templ = '@template.j2'
        template_path = 'data'
        kwargs = {'nom': 'Einstein', 'prenom': 'Albert'}
        expect = 'erreur'
        result = render_templates(
            tmpl=templ,
            template_path=template_path,
            **kwargs)
        self.assertIn(expect, result)



if __name__ == "__main__":
    unittest.main()
