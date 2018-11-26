#! /usr/bin/env python3

import pathlib
import sys
import unittest

file_path = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(file_path))

from scan_disk import *


class ScanDiskTestCase(unittest.TestCase):
    """
        Checks the methods of the scan_disk class.
    """
    def setUp(self):
        self.directory = file_path / 'scan_disk' / 'tests'
        self.output = ''
        self.scan_disk = scan_disk.ScanDisk.make(self.directory,
                                                 self.output)

    def test_01_read_directory_ok(self):
        print('test 1')
        if str(self.directory).split('/')[1] == 'code':
            expect = '/code/scan_disk/tests'
        else:
            expect = '/home/jean/Documents/python/scan_disk/scan_disk/tests'
        result = self.scan_disk.read_directory(self.directory)
        self.assertIn(expect, result)

    def test_02_read_directory_ko1(self):
        print('test 2')
        expect = 'The name you enter is not a directory'
        directory = file_path / 'scan_disk' / 'texts'
        result = self.scan_disk.read_directory(directory)
        self.assertEqual(expect, result[str(directory)])

    def test_03_read_directory_ko2(self):
        print('test 3')
        directory = 53
        result = self.scan_disk.read_directory(directory)
        self.assertIsInstance(result[str(directory)], AttributeError)

    def test_04_search_data_ok(self):
        print('test 4')
        walk_name = ['__init__.py', 'test_scan_disk.py']
        result = self.scan_disk.search_data(walk_name, self.directory)
        self.assertIn('inode', result['__init__.py'])

    def test_05_search_data_ko(self):
        print('test 5')
        walk_name = []
        expect = {'null': None}
        result = self.scan_disk.search_data(walk_name, self.directory)
        self.assertEqual(expect, result)

    def test_06_search_stats_ok(self):
        print('test 6')
        name = '__init__.py'
        result = self.scan_disk.search_stats(name)
        self.assertIn('droits', result)

    def test_07_search_stats_ko1(self):
        print('test 7')
        name = 'init.py'
        result = self.scan_disk.search_stats(name)
        self.assertIsInstance(result['error'], FileNotFoundError)

    def test_08_search_stats_ko2(self):
        print('test 8')
        name = '54'
        result = self.scan_disk.search_stats(name)
        self.assertIsInstance(result['error'], OSError)

    def test_09_format_time_ok(self):
        print('test 9')
        date_time = 1541611448
        if str(self.directory).split('/')[1] == 'code':
            expect = '2018-11-07 17:24:08'
        else:
            expect = '2018-11-07 18:24:08'
        result = self.scan_disk.format_time(date_time)
        self.assertEqual(expect, result)

    def test_10_format_time_ko1(self):
        print('test 10')
        date_time = 'date'
        result = self.scan_disk.format_time(date_time)
        self.assertIsInstance(result, TypeError)

    def test_11_format_time_ko2(self):
        print('test 11')
        date_time = 999999999999999999999999999999999999999999999
        result = self.scan_disk.format_time(date_time)
        self.assertIsInstance(result, OverflowError)

    def test_12_format_time_ko3(self):
        print('test 12')
        date_time = None
        result = self.scan_disk.format_time(date_time)
        self.assertIsInstance(result, Exception)

    def test_13_calcul_droit_ok_file(self):
        print('test 13')
        mode = '0o100765'
        expect = ('File ', 'rwx rw- r-x ')
        result = self.scan_disk.calcul_droit(mode)
        self.assertEqual(expect, result)

    def test_14_calcul_droit_ok_rep(self):
        print('test 14')
        mode = '0o40432'
        expect = ('Rep ', 'r-- -wx -w- ')
        result = self.scan_disk.calcul_droit(mode)
        self.assertEqual(expect, result)

    def test_15_calcul_droit_ok_inconnu(self):
        print('test 15')
        mode = '0o30109'
        expect = ('Inconnu ', '--x --- calcul invalide')
        result = self.scan_disk.calcul_droit(mode)
        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main()
