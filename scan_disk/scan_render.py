#! /usr/bin/python3
# coding:utf-8

# import xlsxwriter
import pathlib
import jinja2
import yaml
# import copy
# import csv
import scan_disk.utils as utils

"""
    Generating Disk Scan Report

    The presentation model is a html file.

    In future, the presentation model can be very different depending on the type of format
    that we wish to leave, to study for excel or for pdf
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

    def render_html(self):
        """
           Generate a html page from jinja templates and the data dict
           :param self : The class instance
           :type self : ScanRender
           :return : error_code, error_message
           :rtype: int, String
        """

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
