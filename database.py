# -*- coding: utf-8 -*-
""" This file contains all functions and information pertaining to the database of the bot.

Common Uses
-----------
Any connections to the database will be through the connect method.
Example:
    with connect(path, commit=True) as cursor:
        # Use the cursor here

    The connection will automatically close when you leave the with block.

Todo
----
*

"""
from contextlib import contextmanager  # Used to simplify connecting to the database
import sqlite3  # Used to connect to the database


@contextmanager
def connect(path, commit=False):
    """ Connects to the database, yielding a cursor to use during the connection, and closing the connection when
    finished.

    Parameters
    ----------
    path : str
        The path to the database.
    commit : bool
        Whether or not changes should be committed.

    """
    # Tries to open the connection
    try:
        # Opens the connection
        db = sqlite3.connect(path)
        # Creates the cursor
        cursor = db.cursor()
        # Yields the cursor for use outside of the function
        yield cursor
    # Excepts any errors generated by sqlite3
    except sqlite3.Error as e:
        # Prints the error
        print(e)
    # If there were no errors, checks if a commit or rollback should occur
    else:
        # If commits should occur
        if commit:
            # Commits the database
            db.commit()
        # if commits should not occur
        else:
            # Rolls the database back
            db.rollback()
    # Finishes the try block by closing the connection
    finally:
        # Closes the connection
        db.close()


def sql_execute(path, sql, commit=False):
    """ Executes the given sql, returning the cursor.

    Parameters
    ----------
    path : str
        The path to the database.
    sql : str
        The sql to be executed.
    commit: bool
        Determines if commits can occur in the used connection.

    """
    # Opens the database connection to retrieve the cursor
    with connect(path, commit=commit) as c:
        # Executes the given sql
        c.execute(sql)
        # Returns the cursor results
        return c.fetchall()


def list_tables(path, commit=False):
    """ Lists all of the tables in the database.

    Parameters
    ----------
    path : str
        The path to the database.
    commit : bool
        Whether or not changes should be committed.

    """
    # Opens the connection to the database and creates the cursor
    with connect(path, commit=commit) as c:
        # String that selects all of the tables from the master table
        sql = \
            '''
            SELECT name
            FROM sqlite_master
            WHERE type='table';
            '''
        # Execute the sql
        c.execute(sql)
        # Return all of the table names
        return c.fetchall()


def ins_def(path, server, command, definition, commit=False):
    """ Inserts a new definition into the defs table. Used to store urls, definitions, etc in a database based
    on a given command value.

    Parameters
    ----------
    path : str
        The path to the database.
    server : int
        The server id of the server the command is to be associated with.
    command : str
        The command to be associated with the definition.
    definition : str
        The definition to be stored in the database.
    commit : bool
        Whether or not changes should be committed.

    Returns
    -------
    bool
        Returns whether inputting the new definition was successful or not.

    """

    # Opens the database connection to retrieve the cursor
    with connect(path, commit=commit) as c:
        # The sql that will be used to insert the definition
        sql = \
            '''
            INSERT INTO defs
            (server, command, def)
            VALUES
            (?, ?, ?);
            '''
        # Executes the sql to insert the command into the database
        c.execute(sql, (server, command, definition))
        # Return True to signal the definition has been successfully inserted
        return True

    # Return False to signal the definition has not been successfully inserted
    return False


def get_def(path, server, command):
    """ Gets a definition from the defs table. Assumes the connection will not need to be committed.

    Parameters
    ----------
    path : str
        The path to the database.
    server : int
        The server id of the server the definition is to be retrieved for.
    command: str
        The command associated with the desired definition.

    Returns
    -------
    definition : str
        Returns the definition associated with the command.
    failure : None
        Returns None if the definition does not exist in the database.

    """
    # Connects to the database and uses the cursor to execute sql.
    with connect(path) as c:
        # The sql that will be used to retrieve the definition
        sql = \
            '''
            SELECT def
            FROM defs
            WHERE server=? AND command=?;
            '''
        # Executes the sql to retrieve the desired definition
        c.execute(sql, (server, command))
        # Returns the definition from the database
        definition = c.fetchone()
        if definition is not None:
            return definition[0]
        else:
            return None


def del_def(path, server, command, commit=False):
    """ Removes the definition from the defs table.

    Parameters
    ----------
    path : str
        The path to the database.
    server : int
        The server id of the server the definition is to be deleted from.
    command : str
        The command associated with the desired definition.
    commit : bool
        Determines if a commit can occur in the used connection.

    """
    # Connects to the database and uses the cursor to execute sql.
    with connect(path, commit=commit) as c:
        # The sql that will be used to delete the definition
        sql = \
            '''
            DELETE FROM defs
            WHERE server=? AND command=?;
            '''
        # Executes the sql to delete the desired definition
        c.execute(sql, (server, command))
