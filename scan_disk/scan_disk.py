#! /usr/bin/python3
# coding:utf-8

"""
    Programme permettant de lire le contenu d'un ou plusieurs répertoires
"""

import os
import sys
import pathlib
import datetime
import scan_disk.utils as utils
import scan_disk.scan_render as render

project_path = pathlib.Path(__file__).resolve().parents[1]

if sys.path[0] != str(project_path):
    sys.path.insert(0, str(project_path))

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
        file_paths = {'logging': project_path / 'config' / 'logging.yml'}
        print(project_path)

        # initialisation des loggings
        utils.setup_logging(file_paths["logging"],
                            project_path / "logs" / "scan_disk.log")
        logger = utils.logging.getLogger("flogger")

        return cls(directory=directory,
                   output=output,
                   logger=logger)

    def __init__(self, directory, output, logger):
        """
            Constructor
        """
        self.directory = directory
        self.output = output
        self.logger = logger

        self.logger.info('********** Initialisation du programme **********')
        self.logger.info('******* Fin d\'initialisation du programme *******')

        # Set KO exit reply text
        self.ko_reply_text = 'Scan_disk a été brusquement interrompu !\n \
                                           ._//(`O`)\_.'

        # Set OK exit reply text
        self.ok_reply_text = 'Scan_disk a correctement écrit l\'ensemble \
        des fichiers demandés.\n\
        A bientôt ...\n!°\--(^_^)--/°!'

    def read_directory(self, name):
        result = {}
        try:
            if name.is_dir():
                file_list = os.walk(name)
                for dirpath, dirname, filename in file_list:
                    self.logger.info(f'Lecture du repertoire {dirpath}')
                    self.logger.info('Lecture des sous-répertoires')
                    sous_rep = self.search_data(dirname, dirpath)
                    self.logger.info('Lecture des fichiers')
                    fichier = self.search_data(filename, dirpath)
                    self.logger.info('Construction du dictionnaire')
                    repe = Repertoire(dirpath, sous_rep, fichier)
                    result[dirpath] = repe.__dict__
            else:
                raise NotADirectoryError
        except NotADirectoryError:
            self.logger.error(f'{name} n\'est pas un répertoire valide')
            result[str(name)] = 'The name you enter is not a directory'
        except Exception as error:
            self.logger.error(f'Une erreur {error} est survenue')
            result[str(name)] = error
        finally:
            self.logger.info('Fin de l\'analyse du répertoire')
            return result

    def search_data(self, walk_name, rep):
        fichier = {}
        try:
            if walk_name[0]:
                for name in walk_name:
                    chemin = pathlib.Path(f'{rep}/{name}')
                    fichier[name] = self.affiche_stats(chemin)
        except IndexError as error:
            self.logger.info('La liste est vide')
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
            size = str(stats.st_size//1024) + ' Ko' if stats.st_size > 1024 else str(stats.st_size) + ' o'
            result['size'] = size
            result['acces'] = self.format_time(int(stats.st_atime))
            result['modif'] = self.format_time(int(stats.st_mtime))
            result['create'] = self.format_time(int(stats.st_ctime))
        except FileExistsError as error:
            self.logger.error(f'Le fichier {filename} n\'existe pas' +
                              f'L\'erreur {error} a été générée')
            result['error'] = error
        except FileNotFoundError as error:
            self.logger.error(f'Le fichier {filename} n\'a pas été trouvé' +
                              f'L\'erreur {error} a été générée')
            result['error'] = error
        return result

    def format_time(self, time):
        formatted_date = None
        try:
            date = datetime.datetime.fromtimestamp(time)
            formatted_date = date.isoformat(sep=' ')
        except TypeError as error:
            self.logger.error(error)
            formatted_date = error
        except ValueError as error:
            self.logger.error(error)
            formatted_date = error
        except Exception as error:
            self.logger.error(error)
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
        self.logger.info(f'Analyse du répertoire {self.directory}')
        scan = self.read_directory(self.directory)
        if isinstance(scan[str(self.directory)], str):
            self.logger.info(self.ko_reply_text)
            exit(1)
        self.logger.info('Fin analyse du répertoire')
        self.logger.info('Début du rendu html')
        scan_result = render.ScanRender(scan,
                                        self.directory,
                                        self.output)
        error_code, error_message = scan_result.render_html()
        self.logger.info('Fin du rendu html')
        if error_code != 200:
            self.logger.error(error_message)
        else:
            self.logger.info(self.ok_reply_text)
