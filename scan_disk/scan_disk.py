#! /usr/bin/python3
# coding:utf-8

"""
    Programme permettant de lire le contenu d'un ou plusieurs répertoires
"""

import os
import jinja2
import pathlib
import datetime
import json
import scan_disk.scan_render as render

"""Application permettant de scanner un répertoire et ses sous-répertoires.

Exemple de lancement :
    - depuis le repertoire racine :
    docker run -it --rm -v $PWD:/code registry.tools.edw.lan/edwtf/
    pyrt3.6:'tag' python -m liste -d <rep>
    - depuis le repertoire grap_data :
    docker run -it --rm -v $PWD:/code registry.tools.edw.lan/edwtf/
    pyrt3.6:'tag' python app.py -d <rep>

Si le nom du répertoire est omis, le répertoire racine est pris par défault.
"""


class Repertoire():

    def __init__(self, name, repe, file):
        self.name = name
        self.repe = repe
        self.file = file


class ScanDisk:

    @classmethod
    def make(cls, directory, output):
        """
            Creates a class instance.

            :param cls: The Scan **disk class.
            :type cls: type.
            :returns: An instance of the class.
            :rtype: ScanDisk
        """
        return cls(directory=directory,
                   output=output)

    def __init__(self, directory, output):
        """
            Constructor
        """
        self.directory = directory
        self.output = output

    def read_directory(self, name):
        result = {}
        try:
            if name.is_dir():
                file_list = os.walk(name)
                for dirpath, dirname, filename in file_list:
                    sous_rep = self.search_data(dirname, dirpath)
                    fichier = self.search_data(filename, dirpath)
                    repe = Repertoire(dirpath, sous_rep, fichier)
                    result[dirpath] = repe.__dict__
            else:
                raise NotADirectoryError
        except NotADirectoryError:
            result['error'] = 'The name you enter is not a directory'
        except Exception as error:
            result['error'] = error
        finally:
            return result

    def search_data(self, walk_name, rep):
        fichier = {}
        try:
            if walk_name[0]:
                for name in walk_name:
                    chemin = pathlib.Path(f'{rep}/{name}')
                    fichier[name] = self.affiche_stats(chemin)
        except IndexError as error:
            fichier['null'] = None
        return fichier

    def affiche_stats(self, filename):
        result = {}
        try:
            stats = os.stat(filename)
            mode = self.calcul_droit(str(oct(stats.st_mode)))
            result['type'] = mode[0]
            result['droits'] = mode[1]
            result['inode'] = str(stats.st_ino)
            result['dev'] = str(stats.st_dev)
            result['uid'] = str(stats.st_uid)
            result['gid'] = str(stats.st_gid)
            result['size'] = str(stats.st_size)
            result['acces'] = self.format_time(int(stats.st_atime))
            result['modif'] = self.format_time(int(stats.st_mtime))
            result['create'] = self.format_time(int(stats.st_ctime))
        except FileExistsError as error:
            result['error'] = error
        except FileNotFoundError as error:
            result['error'] = error
        return result

    def format_time(self, time):
        formatted_date = None
        try:
            date = datetime.datetime.fromtimestamp(time)
            formatted_date = date.isoformat(sep=' ')
        except TypeError as error:
            formatted_date = error
        except ValueError as error:
            formatted_date = error
        except Exception as error:
            formatted_date = error
        finally:
            return formatted_date

    def calcul_droit(self, mode):
        ftype = ''
        droit = ''
        if mode[:len(mode)-3] == '0o40':
            ftype = 'Rep '
        elif mode[:len(mode)-3] == '0o100':
            ftype += 'File '
        else:
            ftype += 'Inconnu '
        for i in mode[len(mode)-3: len(mode)]:
            if i == '7':
                droit += 'rwx '
            elif i == '6':
                droit += 'rw- '
            elif i == '5':
                droit += 'r-x '
            elif i == '4':
                droit += 'r-- '
            elif i == '3':
                droit += '-wx '
            elif i == '2':
                droit += '-w- '
            elif i == '1':
                droit += '--x '
            elif i == '0':
                droit += '--- '
            else:
                droit += 'calcul invalide'
        return ftype, droit

    def run(self):
        scan_result = render.ScanRender(self.read_directory(self.directory),
                                        self.directory, self.output)
        error_code = scan_result.render_html()
        if error_code == 200:
            print('Opération terminée')
