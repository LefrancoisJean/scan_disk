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
    with open(file_path, encoding="utf-8") as file:
        loaded_yaml = yaml.load(file.read())

    return loaded_yaml


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
    if tmpl and tmpl.startswith("@"):
        template_name = tmpl[1:]
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_path)))
        template = environment.get_template(template_name)
    else:
        template = jinja2.Template(tmpl)

    return template.render(**kwargs)


def setup_logging(config_path, logging_path):
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


def validate_schema(file_paths,
                    template=None,
                    template_schema=None):
    """
        Checks the yaml files.

        :param file_paths: The paths of the yaml files.
        :type file_paths: dict.
        :param template: The template of the grap.
        :type template: dict.
        :param template_schema: The schema of the *.yml file.
        :type template_schema: dict.
    """
    error_code = 200
    error_message = None

    if template is not None and template_schema is not None:
        try:
            jsonschema.validate(template, template_schema)
        except jsonschema.ValidationError as error:
            error_code = 1002
            error_message = {
                "description": str(error),
                "file_name": file_paths["template"]
            }
        except jsonschema.SchemaError as error:
            error_code = 1001
            error_message = {
                "description": str(error),
                "file_name": file_paths["template_schema"]
            }
        except Exception as error:
            error_code = 1000
            error_message = str(error)

    return (error_code, error_message)


class DBSession(mariadb.MySQLConnection):
    """
        Extension of the MySQL connector that provides automatic cursor
        management and a context manager for nested transaction control.
    """

    def __init__(self, *args, **kwargs):
        """
            Initializes the parent class and instance variables.

            :param self: The class instance.
            :type self: DBSession.
            :param args: Positional arguments.
            :type args: list.
            :param kwargs: Keyword arguments.
            :type args: dict.
        """
        super().__init__(*args, **kwargs)

        if "autocommit" not in kwargs:
            self.autocommit = True

    def __enter__(self):
        """
            Creates the target of the context manager.

            :param self: The class instance.
            :type self: DBSession.
            :returns: The class instance.
            :rtype: DBSession
        """
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """
            Closes the context manager.

            :param self: The class instance.
            :type self: DBSession.
            :param exception_type: The type of the exception raised in the
             body of the with statement if any or None.
            :type exception_type: BaseException or NoneType.
            :param exception_value: The value of the exception raised in the
             body of the with statement if any or None.
            :type exception_value: str or NoneType.
            :param exception_traceback: The value of the exception raised in
             the body of the with statement if any or None.
            :type exception_traceback: Traceback or NoneType.
        """
        self.close()

    def execute(self, statement, parameters=None, fetch="all", size=None,
                script=False):
        """
            Executes a statement and counts the number of affected rows.

            :param self: The class instance.
            :type self: DBSession.
            :param statement: The SQL statement to be executed.
            :type statement: str.
            :param parameters: The parameters of the SQL statement.
            :type parameters: tuple.
            :param fetch: The fetch method to call.
            :type fetch: str.
            :param size: The number of rows to fetch.
            :type size: int.
            :param script: If multiple statements are given.
            :type script: bool.
            :returns: The result set or the number of affected rows.
            :rtype: list(dict) or int.
        """
        cursor = self.cursor(dictionary=True)
        return_value = None

        try:
            if script:
                statement = re.sub(r"--.*", r"", statement)
                statement = re.sub(
                    r"/\*.*?\*/", r"", statement, flags=re.DOTALL)
                statement = re.sub(
                    r"DELIMITER\s+(.*?)\s+(.*?)\1\s+DELIMITER",
                    r"\2",
                    statement,
                    flags=re.DOTALL | re.IGNORECASE)
                statements = statement.split(";")

                for statement in statements:
                    statement = statement.strip()

                    if statement:
                        cursor.execute(statement)
            elif parameters:
                cursor.execute(statement, parameters)
            else:
                cursor.execute(statement)

            try:
                if fetch == "all":
                    return_value = cursor.fetchall()
                elif fetch == "one":
                    return_value = cursor.fetchone()
                elif fetch == "many":
                    if size:
                        return_value = cursor.fetchmany(size)
                    else:
                        return_value = cursor.fetchmany()
            except mariadb.InterfaceError as error:
                return_value = cursor.rowcount
        finally:
            cursor.close()

        return return_value

    @contextlib.contextmanager
    def transaction(self):
        """
            Creates a context manager for nested transaction control.

            :param self: The class instance.
            :type self: DBSession.
        """
        savepoint = False

        if self.autocommit:
            cursor = self.cursor()

            try:
                if not self.in_transaction:
                    cursor.execute("BEGIN")
                else:
                    savepoint = True
                    cursor.execute("SAVEPOINT s")
            finally:
                cursor.close()

        try:
            yield
        except mariadb.DatabaseError:
            cursor = self.cursor()

            try:
                if savepoint:
                    cursor.execute("ROLLBACK TO s")
                    cursor.execute("RELEASE SAVEPOINT s")
                else:
                    cursor.execute("ROLLBACK")
                    raise
            finally:
                cursor.close()
        else:
            cursor = self.cursor()

            try:
                if savepoint:
                    cursor.execute("RELEASE SAVEPOINT s")
                else:
                    cursor.execute("COMMIT")
            finally:
                cursor.close()
