import statistics_of_usage_module as statistics
import sqlite3
import datetime
import logging
from logger import log_action

class MonitoringAppDatabase:
    @log_action
    def __init__(self):
        try:
            logging.debug("Connecting to the database.")
            self.conn = sqlite3.connect('monitoring_app.db')
            self.cur = self.conn.cursor()
            logging.info("Database connected successfully.")
        except sqlite3.Error as err:
            logging.error("An error occurred while connecting to the database:",err)

    # create tables to collect statistics
    @log_action
    def setup_database_tables(self):

        try:
            logging.debug("Creating tables in database...")
            self.cur.execute("CREATE TABLE IF NOT EXISTS disks (time TIMESTAMP, disk_name TEXT, size TEXT, used TEXT, Avail TEXT, Use TEXT, Mount_on TEXT);")
            self.cur.execute("CREATE TABLE IF NOT EXISTS memory (time TIMESTAMP, name TEXT, total INTEGER, used INTEGER, free INTEGER, shared INTEGER, buff INTEGER, available INTEGER);")
            self.cur.execute("CREATE TABLE IF NOT EXISTS cpu (time TIMESTAMP, cpu TEXT, usr FLOAT, nice FLOAT, sys FLOAT, iowait FLOAT, irq FLOAT, soft FLOAT, steal FLOAT, guest FLOAT, gnice FLOAT, idle FLOAT);")
            logging.info("Tables creation done successfully.")

            self.conn.commit()
        except Exception as e:
            print("Error setting up database tables: ", e)

    # collect data then store it inside database tabels
    @log_action
    def set_and_collect_data_in_database(self):
        self.set_disks_usage_in_db()
        self.set_memory_usage_in_db()
        self.set_cpu_usage_in_db()

        self.conn.commit()

    @log_action
    def set_disks_usage_in_db(self):
        try:
            disks = statistics.get_disks_usage()
            logging.debug("Inserting disks usage into disk table...")
            for item in disks:
                self.cur.execute("INSERT INTO disks (time, disk_name, size, used, Avail, Use, Mount_on) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (datetime.datetime.now(), item["Filesystem"], item["Size"], item["Used"], item["Avail"], item["Use%"], item["Mounted"]))
            logging.info("Inserting done successfully.")
        except sqlite3.InternalError as e:
            logging.exception("Error setting disks usage in database: ", e)

    @log_action
    def set_memory_usage_in_db(self):
        try:
            memory = statistics.get_memory_usage()
            logging.debug("Inserting memory usage into memory table...")
            for item in memory:
                if item["name"] == "Swap:": # swap memory cause it has specific attributes
                    self.cur.execute("INSERT INTO memory (time, name, total, used, free, shared, buff, available) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (datetime.datetime.now(), item["name"], item["total"], item["used"], item["free"], 0, 0, 0))
                else:
                    self.cur.execute("INSERT INTO memory (time, name, total, used, free, shared, buff, available) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (datetime.datetime.now(), item["name"], item["total"], item["used"], item["free"], item["shared"], item["buff/cache"], item["available"]))
            logging.info("Inserting done successfully.")
        except sqlite3.InternalError as e:
            logging.exception("Error setting memory usage in database: ", e)

    @log_action
    def set_cpu_usage_in_db(self):
        try:
            cpu = statistics.get_cpu_usage()
            logging.debug("Inserting CPU usage into cpu table...")
            for item in cpu:
                now = datetime.datetime.now()
                self.cur.execute("INSERT INTO cpu (time, cpu, usr, nice, sys, iowait, irq, soft, steal, guest, gnice, idle) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (datetime.datetime.now(), item["CPU"], item["%usr"], item["%nice"], item["%sys"], item["%iowait"], item["%irq"], item["%soft"],
                        item["%steal"], item["%guest"], item["%gnice"], item["%idle"]))
            logging.info("Inserting done successfully.")
        except sqlite3.InternalError as e:
            logging.exception("Error setting CPU usage in database: ", e)

    # this function will execute each hour to remove any recored has more than 24 hours created
    @log_action
    def refresh_database(self):
        try:
            # Get all tables from the database
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [table[0] for table in self.cur.fetchall()]
            logging.info("All database tables names are collected successfully.")

            # Delete rows older than 86400 sec (24 hours)
            logging.debug("Fetching old data(created since morethan one day)....")
            current_time = datetime.datetime.now()
            for table in table_names:
                self.cur.execute("DELETE FROM {} WHERE (strftime('%s','now') - strftime('%s',time)) > 86400".format(table))

            self.conn.commit()
            logging.info("data fetch done successfully.")
        except sqlite3.InternalError as e:
            logging.exception("Error occurn while refresh the database: ", e)

    @log_action
    def close_conncetion(self):
        logging.debug("Closing conncetion.....")
        self.conn.close()
        logging.info("Concetion closed.")

if __name__ == "__main__":
   app = MonitoringAppDatabase()
   app.refresh_database()
   app.setup_database_tables()
   app.set_and_collect_data_in_database()
   app.close_conncetion()