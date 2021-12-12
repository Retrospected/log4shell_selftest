import sqlite3
import datetime
import os
import logging

class database:
    def __init__(self,db_file):

        self.db_file=db_file
        if not os.path.exists(db_file):
            print("[DB] DATABASE NOT FOUND")
            self.create_database()
            print("[DB] DATABASE CREATED")
        else:
            print("[DB] DATABASE FOUND")

        self.connect_database()

    def connect_database(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_database(self):
        self.connect_database()

        sql_webapps_table = """ CREATE TABLE IF NOT EXISTS dnslogs (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        date_added text NOT NULL,
                                        entry text NOT NULL
                                    ); """


        if self.cursor is not None:
            self.create_table(sql_webapps_table)

    def commit(self):
        self.conn.commit()

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            logger.info(e)

    def parse_entry(self, entry):
        cursor = self.cursor
        lookupQuery = 'SELECT entry FROM dnslogs WHERE entry=\'{entryValue}\''.format(entryValue=entry)
        lookupResult = cursor.execute(lookupQuery).fetchall()

        if len(lookupResult) == 0:
              print("[DB] New entry: "+entry)
              cursor.execute("INSERT INTO dnslogs (date_added, entry) VALUES (?,?)", (str(datetime.datetime.now()), entry))

        self.commit()

    def get_entry(self, entry):
        print("[DB] Looking up entry based on web request: "+entry)
        cursor = self.cursor
        lookupQuery = 'SELECT entry FROM dnslogs WHERE entry=\'{entryValue}\''.format(entryValue=entry)
        lookupResult = cursor.execute(lookupQuery).fetchall()

        if len(lookupResult) == 0:
            print("[DB] No entry found for web request :"+entry)
            return False
        else:
            print("[DB] ENTRY FOUND! for web request: "+entry)
            return True
