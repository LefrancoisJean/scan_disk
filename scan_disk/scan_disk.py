#! /usr/bin/python3
# coding:utf-8

"""
    This application scan a folder, this sub folders and files.
    The output file is a html file.
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


class Repertoire():
    """
       Create a class to construct the result
    """

    def __init__(self, name, repe, file):
        self.name = name
        self.repe = repe
        self.file = file


class ScanDisk:

    @classmethod
    def make(cls, directory, output):
        """
            Creates a class instance.

            :param cls: The Scan_disk class
            :type cls: type
            :param directory: The folder to scan
            :type directory: Path
            :param output: The name of the output file
            :type output: String
            :returns: An instance of the class
            :rtype: ScanDisk
        """
        file_paths = {'logging': project_path / 'config' / 'logging.yml'}

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
            :param self: The class instance
            :type self: Scan_disk
            :param directory: The folder to scan
            :type directory: Path
            :param output: The name of the output file
            :type output: String
            :param logger: The logger file
            :type logger: Logging
        """
        self.directory = directory
        self.output = output
        self.logger = logger

        self.logger.info('********** Initialisation du programme **********')
        self.logger.info('******* Fin d\'initialisation du programme *******')

        # Set KO exit reply text
        self.ko_reply_text = 'Scan_disk a été brusquement interrompu !\n ._//(`O`)\_.'

        # Set OK exit reply text
        self.ok_reply_text = 'Scan_disk a correctement écrit l\'ensemble \
des fichiers demandés.\n\
        A bientôt ...\n\
        !°\--(^_^)--/°!'

    def read_directory(self, name):
        """
            The main function to read the folder
            :param self: The class instance
            :type self: Scan_disk
            :param name: the name of the folder to scan
            :type name: Path
            :return: The result of the scan
            :rtype: Dict
        """
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
        """
            Construct the result for sub-folder and files
            :param self: The class instance
            :type self: Scan_disk
            :param walk_name: the list of folders/ files to be analyzed
            :type walk_name: List
            :param rep: the full path of the folder
            :type rep: Path
            :return: the properties of the folders/files
            :rtype: Dict
        """
        result = {}
        try:
            if walk_name[0]:
                for name in walk_name:
                    chemin = pathlib.Path(f'{rep}/{name}')
                    result[name] = self.search_stats(chemin)
        except IndexError as error:
            self.logger.info('La liste est vide')
            result['null'] = None
        return result

    def search_stats(self, name):
        """
            Search information for each folder and file
            :param self: The class instance
            :type self: Scan_disk
            :param name: the name of folder/ file
            :type name: String
            :return: the information of the folder/file
            :rtype: Dict
        """
        result = {}
        try:
            stats = os.stat(name)
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
        except OSError as error:
            self.logger.error(f'Le fichier {name} n\'existe pas. ' +
                              f'L\'erreur {error} a été générée')
            result['error'] = error
        except FileNotFoundError as error:
            self.logger.error(f'Le fichier {name} n\'a pas été trouvé. ' +
                              f'L\'erreur {error} a été générée')
            result['error'] = error
        return result

    def format_time(self, date_time):
        """
            formatted the datetime for human readable
            :param self: The class instance
            :type self: Scan_disk
            :param date_time: the datetime to analyse
            :type date_time: Datetime
            :return: the date_time human readable
            :rtype: String
        """
        formatted_date = None
        try:
            date = datetime.datetime.fromtimestamp(date_time)
            formatted_date = date.isoformat(sep=' ')
        except TypeError as error:
            self.logger.error(error)
            formatted_date = error
        except OverflowError as error:
            self.logger.error(error)
            formatted_date = error
        except Exception as error:
            self.logger.error(error)
            formatted_date = error
        finally:
            return formatted_date

    def calcul_droit(self, mode):
        """
            calculate permissions for each folder or file
            :param self: The class instance
            :type self: Scan_disk
            :param mode: the permissions in linux format
            :type mode: String
            :return: the permissions human readable
            :rtype: String
        """
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

    def run(self):  # pragma: no cover
        """
            The main function
        """
        self.logger.info(f'Analyse du répertoire {self.directory}')
        scan = self.read_directory(self.directory)
        self.logger.info('Fin analyse du répertoire')
        if isinstance(scan[str(self.directory)], str):
            self.logger.info(self.ko_reply_text)
            exit(1)
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
