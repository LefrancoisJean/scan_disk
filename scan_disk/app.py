#! /usr/bin/python3
import argparse
import sys
import pathlib

project_path = pathlib.Path(__file__).resolve().parents

if sys.path[0] != str(project_path):
    sys.path.insert(0, str(project_path))

import scan_disk as scan_disk

message = '''Application permettant de scanner un répertoire et ses sous-répertoires.
Le chemin du repertoire et le nom du fichier de sortie sont optionnels.
Si le répertoire n'est pas saisi, la racine est prise par défault.
Le chemin du répertoire doit être le chemin complet.

Exemple de lancement :
    - depuis le repertoire racine :
    py -m scan_disk -d <rep> -o <output> pour Windows
    python3 -m scan_disk -d <rep> -o <output> pour Linux
    - depuis le repertoire scan_disk :
    py scan_disk -d <rep> -o <output> pour Windows
    python3 scan_disk -d <rep> -o <output> pour Linux

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
