#! /usr/bin/env python3

import pathlib
import sys
import unittest

file_path = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(file_path))

from scan_disk.scan_render import *


class ScanRenderTestCase(unittest.TestCase):
    """
        Checks the methods of the scan_render class.
    """
    def setUp(self):
        self.directory = file_path / 'scan_disk' / 'tests'
        self.scan = {
            '/home/jean/Documents/python/scan_disk/scan_disk/tests': {
                'name': '/home/jean/Documents/python/scan_disk/scan_disk/tests',
                'repe': {
                    '__pycache__': {
                        'type': 'Rep ',
                        'droits': 'rwx rwx rwx ',
                        'inode': '893227',
                        'dev': '2054',
                        'uid': '1000',
                        'gid': '1000',
                        'size': '4 Ko',
                        'acces': '2018-11-15 18:51:44',
                        'modif': '2018-11-09 13:33:40',
                        'create': '2018-11-15 18:51:44'
                    }
                },
                'file': {
                    '__init__.py': {
                        'type': 'File ',
                        'droits': 'rwx rwx rwx ',
                        'inode': '831247',
                        'dev': '2054',
                        'uid': '1000',
                        'gid': '1000',
                        'size': '60 o',
                        'acces': '2018-11-15 18:56:44',
                        'modif': '2018-11-07 18:07:57',
                        'create': '2018-11-15 18:51:44'
                    },
                    'test_scan_disk.py': {
                        'type': 'File ',
                        'droits': 'rwx rwx rwx ',
                        'inode': '831278',
                        'dev': '2054',
                        'uid': '1000',
                        'gid': '1000',
                        'size': '4 Ko',
                        'acces': '2018-11-16 07:25:57',
                        'modif': '2018-11-16 07:25:57',
                        'create': '2018-11-16 07:25:57'
                    },
                    'test_scan_render.py': {
                        'type': 'File ',
                        'droits': 'rw- rw- r-- ',
                        'inode': '794068',
                        'dev': '2054',
                        'uid': '1000',
                        'gid': '1000',
                        'size': '950 o',
                        'acces': '2018-11-16 07:22:59',
                        'modif': '2018-11-16 07:22:59',
                        'create': '2018-11-16 07:22:59'
                    }
                }
            }, 
            '/home/jean/Documents/python/scan_disk/scan_disk/tests/__pycache__': {
                'name': '/home/jean/Documents/python/scan_disk/scan_disk/tests/__pycache__',
                'repe': {
                    'null': None
                },
                'file': {
                    '__init__.cpython-36.pyc': {
                        'type': 'File ',
                        'droits': 'rwx rwx rwx ',
                        'inode': '830524',
                        'dev': '2054',
                        'uid': '1000',
                        'gid': '1000',
                        'size': '184 o',
                        'acces': '2018-11-15 18:51:47',
                        'modif': '2018-11-09 08:13:51',
                        'create': '2018-11-15 18:51:44'
                    },
                    'test_scan_disk.cpython-36.pyc': {
                        'type': 'File ',
                        'droits': 'rwx rwx rwx ',
                        'inode': '831235',
                        'dev': '2054',
                        'uid': '2222',
                        'gid': '2222',
                        'size': '5 Ko',
                        'acces': '2018-11-15 18:51:47',
                        'modif': '2018-11-09 13:33:40',
                        'create': '2018-11-15 18:51:44'
                    }
                }
            }
        }
        self.scan_render = ScanRender(self.scan,
                                                  self.directory)

    def test_01_render_html_ok1(self):
        print('test 1')
        result = self.scan_render.render_html()[0]
        self.assertEqual(200, result)

    def test_02_render_html_ok2(self):
        print('test 2')
        output = 'test'
        render = ScanRender(scan_result=self.scan,
                            directory=self.directory,
                            output=output)
        result = render.render_html()[0]
        print(render.output)
        self.assertEqual(200, result)

    def test_03_render_html_ko1(self):
        print('test 3')
        render = ScanRender(scan_result=34,
                            directory=self.directory)
        result = render.render_html()[0]
        self.assertEqual(1001, result)

    def test_04_render_html_ko2(self):
        print('test 4')
        render = ScanRender(scan_result=self.scan,
                            directory=self.directory,
                            output=12)
        result = render.render_html()[0]
        self.assertEqual(1003, result)

    def test_05_render_html_ko3(self):
        print('test 5')
        render = ScanRender(scan_result=self.scan,
                            directory=self.directory,
                            output='/un/repertoire/vide.html')
        result = render.render_html()[0]
        self.assertEqual(1002, result)


if __name__ == "__main__":
    unittest.main()
