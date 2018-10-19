#! /usr/bin/python3
# coding:utf-8

"""
    Génération du rapport de scannage de disque
    GRAP est en réalité une suite de programmes :

    Le dictionnaire en entrée ne contient que les données du disque

    Le modèle de présentation peut être très divers selon le type de format
    que l'on souhaite en sortie, à étudier pour excel ou pour pdf
"""
# import xlsxwriter
import pathlib
import jinja2
import yaml
# import copy
# import csv
import scan_disk.utils as utils

"""
    La génération du rapport se fera en fonction
    des paramètres passés à l'objet:
    x = Excel
    h = HTML
    j = Jinja (html evolué, à voir pour le packager)
    c = csv
    Le nom du fichier de sortie peut être choisi ou par défault
"""


class ScanRender:

    def __init__(self,
                 scan_result,
                 directory,
                 html=None,
                 csv=None,
                 jinja=None,
                 excel=None,
                 output=None):
        """
        Constructor
        """
        self.scan_result = scan_result
        self.directory = directory
        self.html = html
        self.csv = csv
        self.jinja = jinja
        self.excel = excel
        if output:
            self.output = output
        else:
            self.output = str(self.directory)[1:].split('/')[-1]
            # self.output = 'test'
        self.project_path = pathlib.Path(__file__).resolve().parents[1]

        # Set KO exit reply text
        self.ko_reply_text = "[O] Something went wrong!\n \
                                  Consult the log file \
                                     ._//(`O`)\_."

    def run(self):
        """
        Run the scan_render
        """
        if self.html:
            self.logger.info('[X] Début génération du fichier html')
            error_code = self.render_html(self.scan_result, self.output)
            if error_code != 200:
                self.logger.info(self.ko_reply_text)
                exit(1)
            self.logger.info('[X] Fichier html généré')

        if self.csv:
            self.logger.info('[X] Début génération du fichier csv')
            error_code = self.render_csv(self.scan_result, self.output)
            if error_code != 200:
                self.logger.info(self.ko_reply_text)
                exit(1)
            self.logger.info('[X] Fichier csv généré')

        if self.jinja:
            self.logger.info('[X] Début génération à partir du template jinja')
            error_code = self.render_jinja(self.scan_result, self.output)
            if error_code != 200:
                self.logger.info(self.ko_reply_text)
                exit(1)
            self.logger.info('[X] Fichier jinja généré')

        if self.excel:
            self.logger.info('[X] Début génération fichier Excel')
            error_code = self.render_excel(self.scan_result, self.output)
            if error_code != 200:
                self.logger.info(self.ko_reply_text)
                exit(1)
            self.logger.info('[X] Fichier excel généré')

        self.logger.info(self.ok_reply_text)
        exit(0)

    def render_jinja(self, data, output):
        """
           Génére une page html à partir de templates jinja.
           La page générée peut être afficher à l'écran ou
           sauvegarder dans un fichier
           :param data : dictionnaire des reports
           :type data : dict
           :param output : nom du fichier de sauvegarde
           :type output : string
           :return : error_code
           :rtype: int

        result = ''
        error_code = 200
        try:
            jinja_file_name = "@render.j2"
            result = render_templates(jinja_file_name,
                                      self.file_paths["template"],
                                      **data)
            if output:
                with open(self.file_paths['jinja']/(output+'.html'), 'w',
                          encoding="utf-8") as f:
                    f.write(result)
            else:
                self.logger.info(result)
        except TypeError as err:
            error_code = 1003
            error_dict = {
                "file_name": self.file_paths['template']/'render.j2',
                "description": str(err)
            }
            error_message = render_templates(self.errors[error_code],
                                             error_message=error_dict)
            self.logger.error("[O] {}".format(error_message))
        except Exception as err:
            error_code = 1000
            error_message = render_templates(self.errors[error_code],
                                             error_message=str(err))
            self.logger.error("[O] {}".format(error_message))

        return(error_code)"""
        pass

    def render_excel(self):
        """
           Génére un classeur excel.
           Le classeur généré est sauvegardé dans un fichier
           avec un nom spécifique si il est précisé,
           sinon le nom du fichier de données sera utilisé
           :param data : dictionnaire des reports
           :type data : dict
           :param output : nom du fichier de sauvegarde
           :type output : string
           :return : error_code
           :rtype: int

        error_code = 200
        try:
            print(self.data_file)
            metadata = data['metadata']
            reports = copy.deepcopy(data['reports'])
            if output:
                fic_name = self.file_paths['excel']/(output+'.xlsx')
            else:
                fic_name = self.file_paths['excel']/(self.data_file+'.xlsx')
            with xlsxwriter.Workbook(fic_name) as workbook:
                row, col = 0, 0

                workbook.set_properties({'title': metadata['title'],
                                         'subject': 'Génération d\'un rapport',
                                         'author': 'Olivier Corbier',
                                         'company': 'Docapost DPS',
                                         'comments': 'Created with Python
                                         and Xlsxwriter'})

                title1 = workbook.add_format({'bold': True,
                                              'font_size': 20,
                                              'align': 'center'})

                title2 = workbook.add_format({'bold': True,
                                              'font_size': 14,
                                              'align': 'center'})

                line = workbook.add_format({'italic': True,
                                            'font_size': 12,
                                            'align': 'left'})

                center = workbook.add_format({'align': 'center'})

                worksheet = workbook.add_worksheet('report')

                worksheet.set_column(0, 8, 20, center)
                worksheet.set_column(1, 1, 30, center)
                worksheet.set_column(2, 2, 60, center)
                worksheet.set_column(3, 4, 25, center)

                worksheet.merge_range(row,
                                      col,
                                      row,
                                      col + 8,
                                      metadata['title'],
                                      title1)

                row += 2

                worksheet.write_row(row,
                                    col + 1,
                                    metadata['description'],
                                    line)

                row += 2
                worksheet.write(row, col + 1,
                                f"Créé le {metadata['exec_infos']['created']}",
                                line)
                row += 2

                for key, value in reports.items():
                    if 'title' in reports[key]:
                        row = self.write_excel(reports[key],
                                               row,
                                               col,
                                               worksheet,
                                               title2)
                        row += 1
                    else:
                        for k, v in reports[key].items():
                            row = self.write_excel(reports[key][k],
                                                   row,
                                                   col,
                                                   worksheet,
                                                   title2)
                            row += 1

        except TypeError as err:
            error_code = 1000
            error_message = render_templates(self.errors[error_code],
                                             error_message=str(err))
            self.logger.error("[O] {}".format(error_message))

        return error_code"""
        pass

    def write_excel(self, args, row, col, worksheet, mep):
        """column = []
        for value in args['labels']:
            column.append({'header': value})
        worksheet.merge_range(row, col, row, col + len(args['labels']) - 1,
                              args['title'], mep)
        row += 2
        worksheet.add_table(row, col, row + len(args['data']),
                            col + len(args['labels']) - 1,
                            {'data': args['data'],
                             'columns': column})
        row += len(args['data']) + 2
        return row"""
        pass

    def render_csv(self, data, output):
        """
           Génére un fichier csv.
           Le fichier généré est sauvegardé dans un fichier
           avec un nom spécifique si il est précisé,
           sinon le nom du fichier de données sera utilisé
           :param data : dictionnaire des reports
           :type data : dict
           :param output : nom du fichier de sauvegarde
           :type output : string
           :return : error_code
           :rtype: int

        error_code = 200
        try:
            if output:
                    fic_name = self.file_paths['html']/(output+'.csv')
            else:
                fic_name = self.file_paths['html']/(self.data_file+'.csv')
            with open(fic_name, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=';',
                quoting=csv.QUOTE_ALL)
                writer.writerow([data['metadata']['title']])
                writer.writerow([data['metadata']['description']])
                writer.writerow([data['metadata']['exec_infos']['created']])
                writer.writerow('')
                for key in data['reports'].keys():
                    if 'title' in data['reports'][key]:
                        writer.writerow(data['reports'][key]['labels'])
                        writer.writerows(data['reports'][key]['data'])
                    else:
                        for k in data['reports'][key].keys():
                            writer.writerow(data['reports'][key][k]['labels'])
                            writer.writerows(data['reports'][key][k]['data'])
                            writer.writerow('')
                    writer.writerow('')
        except TypeError as err:
            error_code = 1002
            error_dict = {
                "file_name": fic_name,
                "description": str(err)
            }
            error_message = render_templates(self.errors[error_code],
                                             error_message=error_dict)
            self.logger.error("[O] {}".format(error_message))
        except Exception as err:
            error_code = 1000
            error_message = render_templates(self.errors[error_code],
                                             error_message=str(err))
            self.logger.error("[O] {}".format(error_message))

        return error_code"""
        pass

    def render_html(self):
        """
           Génére une page html à partir de templates jinja.
           La page générée peut être afficher à l'écran ou
           sauvegarder dans un fichier.
           Il s'agit une page basique, sans javascript et un CSS leger
           :param data : dictionnaire des reports
           :type data : dict
           :param output : nom du fichier de sauvegarde
           :type output : string
           :return : error_code
           :rtype: int

        error_code = 200
        result = ''
        try:
            result = render_templates(self.html_template['html'],
                                      **data)

            if output:
                with open(self.file_paths['html']/(output+'.html'),
                          'w', encoding="utf-8") as f:
                    f.write(result)
            else:
                self.logger.info(result)
        except TypeError as err:
            error_code = 1003
            error_dict = {
                "file_name": self.file_paths['html']/'html.yml',
                "description": str(err)
            }
            error_message = render_templates(self.errors[error_code],
                                             error_message=error_dict)
            self.logger.error("[O] {}".format(error_message))
        except Exception as err:
            error_code = 1000
            error_message = render_templates(self.errors[error_code],
                                             error_message=str(err))
            self.logger.error("[O] {}".format(error_message))

        return error_code"""
        error_code, error_message = 200, None
        result = ''
        tableau = self.project_path / 'templates' / 'tableau.yml'
        tableau_template = utils.yaml_to_dict(tableau)

        try:
            result += utils.render_templates(tableau_template['head'],
                                             name=self.output,
                                             descript=str(self.directory))

            for value in self.scan_result.values():
                value['key'] = [
                    'nom', 'type', 'droits', 'inode', 'dev', ' uid', 'gid',
                    'size', 'acces', 'modif', 'create']
                result += utils.render_templates(tableau_template['body'],
                                                 **value)
                result += tableau_template['footer']

                with open(self.project_path / 'html' / (self.output+'.html'),
                          'w', encoding="utf-8") as f:
                    f.write(result)
        except TypeError as error:
            error_code = 1003
            error_message = error
        except IOError as error:
            error_code = 1003
            error_message = error
        except Exception as error:
            error_code = 1000
            error_message = error
        finally:
            return error_code, error_message
