import mysql.connector
import datetime
import os
import logging

class database:
    def __init__(self,db_ip,db_user,db_pass,db_name):

        self.db_ip = db_ip
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

        self.connect_database()
        if not self.test_database():
            print("[DB] DATABASE NOT FOUND")
            self.create_database()
            print("[DB] DATABASE CREATED")

    def test_database(self):
        self.cursor.execute("SHOW TABLES LIKE \"dnslogs\"")
        if len(self.cursor.fetchall()) != 0:
            return True
        else:
            return False

   
    def connect_database(self):
        self.conn = mysql.connector.connect(user=self.db_user, password=self.db_pass, host=self.db_ip, database=self.db_name)
        self.cursor = self.conn.cursor()

    def create_database(self):
        sql_dns_table = """ CREATE TABLE IF NOT EXISTS dnslogs (
                                        id integer primary key auto_increment,
                                        date_added varchar(255) not null,
                                        entry varchar(255) not null
                                    ); """


        if self.cursor is not None:
            self.create_table(sql_dns_table)
            self.commit()

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
            self.commit()
        except Error as e:
            logger.info(e)

    def parse_entry(self, entry):
        lookupQuery = 'SELECT entry FROM dnslogs WHERE entry=%s'
        queryResult = self.cursor.execute(lookupQuery, (entry, ))
        lookupResult = self.cursor.fetchall()

        if len(lookupResult) == 0:
              print("[DB] New entry: "+entry)
              data = (str(datetime.datetime.now()), entry)
              insert_query = """insert into dnslogs(date_added,entry) values(%s, %s)"""

              self.cursor.execute(insert_query,data)
              self.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
