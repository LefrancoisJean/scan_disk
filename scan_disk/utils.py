#! /usr/bin/env python3

"""
    Utility functions.
"""

import contextlib
import jinja2
import logging
import logging.config
import mysql.connector as mariadb
import platform
import re
import sys
import yaml


def yaml_to_dict(file_path):
    """
        Loads YAML data from file.

        :param file_path: The path of the YAML file.
        :type file_path: str or pathlib.PurePath
        :returns: The loaded YAML data.
        :rtype: dict.
    """
    loaded_file = {}
    try:
        with open(file_path, encoding="utf-8") as file:
            loaded_file = yaml.safe_load(file.read())
    except Exception as error:
        loaded_file = {'erreur': error}

    return loaded_file


def render_templates(tmpl, template_path="templates/", **kwargs):
    """
        Renders a Jinja template.

        :param tmpl: The Jinja template or the path of the file holding it.
        :type tmpl: str.
        :param kwargs: The variables of the Jinja template.
        :type tmpl: dict.
        :returns: The rendered Jinja template.
        :rtype: str.
    """
    result = None
    try:
        if tmpl and tmpl.startswith("@"):
            template_name = tmpl[1:]
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(template_path)))
            template = environment.get_template(template_name)
        else:
            template = jinja2.Template(tmpl)
        result = template.render(**kwargs)
    except jinja2.exceptions.TemplateNotFound as error:
        result = {'erreur': f'"{error.name}" not found'} 

    return result


def setup_logging(config_path, logging_path): # pragma: no cover
    """
        Sets the logging up.

        :param config_path: The path of the logging.yml file.
        :type config_path: str or pathlib.PurePath.
        :param logging_path: The path of the logging file.
        :type logging_path: str or pathlib.PurePath.
    """
    kwargs = {"hostname": platform.node(), "file_path": str(logging_path)}

    try:
        config = yaml_to_dict(config_path)

        for key in config["formatters"]:
            try:
                config["formatters"][key]["format"] = render_templates(
                    config["formatters"][key]["format"], **kwargs)
            except KeyError:
                pass

        for key in config["handlers"]:
            try:
                config["handlers"][key]["filename"] = render_templates(
                    config["handlers"][key]["filename"], **kwargs)
            except KeyError:
                pass

        logging.config.dictConfig(config)
    except Exception as error:
        print(
            "Échec de configuration de la journalisation :\n{}".format(error))
        sys.exit(1)
