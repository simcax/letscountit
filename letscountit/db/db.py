"""Class implements database connectivity"""
import logging
from os import environ

import psycopg2


class Database:
    """Class implementing the database connectivity"""

    # db_settings can be configured and passed to psycopg2 as connection parameters
    # application_name is only there for informational purposes
    # According to this link: https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME
    # It will make it easy to see which database stats are coming from, by giving it a name
    db_settings = {
        "database": "app",
        "user": "app",
        "host": "app",
        "port": "app",
        "password": "app",
        "application_name": "app",
        "sslmode": "app",
    }
    mode = ""
    conn = False

    def __init__(self) -> None:
        """Initialize the database settings"""
        # For now we inistialize sane default here. At  a later point, we will probably move this class
        # to be a full fledged module, and have the dictionary values passed thus enabling connection
        # to any database

        if environ.get("ENV") not in ("TEST", "PROD"):
            # We must be on a local development machine, otherwise environment would be one of prod or test
            self.mode = "DEV"
            self.db_settings["database"] = "letscountit_local"
            self.db_settings["user"] = "root"
            self.db_settings["host"] = "localhost"
            self.db_settings["port"] = 26257
            self.db_settings["password"] = ""
            self.db_settings["application_name"] = "letscountit"
            self.db_settings["sslmode"] = "disable"
        else:
            self.mode = environ.get("ENV")
            self.db_settings["database"] = environ.get("database")
            self.db_settings["user"] = environ.get("dbUser")
            self.db_settings["host"] = environ.get("dbHost")
            self.db_settings["port"] = environ.get("dbPost", 26257)
            self.db_settings["password"] = environ.get("dbPass")
            self.db_settings["application_name"] = "letscountit"
            self.db_settings["sslmode"] = "disable"

    def connect(self):
        """Get a new connection to the database"""
        try:
            self.conn = psycopg2.connect(**self.db_settings)
        except psycopg2.DatabaseError as error:
            self.conn = False
            logging.error(
                "Error connecting to datbaase %s - %s",
                self.db_settings["database"],
                error,
            )

    def disconnect(self):
        """
        Closes the database connection from the class itself
        """
        if self.conn:
            try:
                return self.conn.close()
            except psycopg2.DatabaseError as error:
                print(f"Failed to close database connection: {error}")
        else:
            return False
