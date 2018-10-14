#! /usr/bin/python3
# coding:utf-8
import argparse
import pathlib

import scan_disk.scan_disk as scan_disk

message = '''Application permettant de scanner un répertoire et ses sous-répertoires.

Exemple de lancement :
    - depuis le repertoire racine :
    docker run -it --rm -v $PWD:/code registry.tools.edw.lan/edwtf/pyrt3.6:
    'tag' python -m liste -d <rep>
    - depuis le repertoire grap_data :
    docker run -it --rm -v $PWD:/code registry.tools.edw.lan/edwtf/pyrt3.6:
    'tag' python app.py -d <rep>

Si le nom du répertoire est omis, le répertoire racine est pris par défault.
'''
parser = argparse.ArgumentParser(
    description=message,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--directory', '-d',
                    help='Path of the directory to scan',
                    required=False)
parser.add_argument('--output', '-o',
                    help='Name of the output file',
                    required=False)

args = parser.parse_args()

if not args.directory:
    directory = pathlib.Path('/')
else:
    directory = pathlib.Path(args.directory)

output = args.output

scan_disk = scan_disk.ScanDisk.make(directory, output)
scan_disk.run()
