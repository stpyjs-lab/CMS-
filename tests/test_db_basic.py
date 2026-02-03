# Feature: basic DB tests — check DB existence and tables. Connects: database/connection and queries.
# tests/test_db_basic.py

"""
BASIC DATABASE TESTING IDEA:

These tests answer simple questions:
- Does the database file exist?
- Can Python open the database?
- Does the database contain tables?

We are NOT testing business logic here.
We are only checking that the database is usable.
"""

import unittest
import sqlite3
import os


class TestDatabaseBasics(unittest.TestCase):

    def test_clinic_db_exists(self):
        """
        Check that the clinic database file is present in the project.

        If the file is missing:
        - the app cannot work
        - the test should fail immediately
        """

        # Check: does 'clinic.db' file exist?
        self.assertTrue(
            os.path.exists("clinic.db"),
            "clinic.db file is missing"
        )

    def test_can_connect_and_list_tables(self):
        """
        Check that:
        - we can connect to the database
        - the database contains at least one table
        """

        # Open a connection to the SQLite database
        conn = sqlite3.connect("clinic.db")

        # Create a cursor to run SQL queries
        cur = conn.cursor()

        # Ask SQLite for all table names
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Extract table names into a Python list
        tables = [row[0] for row in cur.fetchall()]

        # Close the database connection
        conn.close()

        # Check: database should have at least one table
        self.assertTrue(
            len(tables) > 0,
            "No tables found in the database"
        )

        # Check: expected table should exist (patients table)
        self.assertIn(
            "patients",
            tables
        )