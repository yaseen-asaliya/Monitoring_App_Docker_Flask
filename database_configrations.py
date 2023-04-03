import statistics_of_usage_module as statistics
import datetime
import logging
from logger import log_action
import mysql.connector
from dotenv import load_dotenv
import os

class MonitoringAppDatabase:
    @log_action
    def __init__(self):
        try:
            logging.debug("Connecting to the database.")
            load_dotenv()
            self.mydb = mysql.connector.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), passwd=os.getenv("DB_PASS"), database=os.getenv("DB_NAME"), port=os.getenv("DB_PORT"))
            self.cur = self.mydb.cursor()
            logging.info("Database connected successfully.")
        except Exception as err:
            logging.error("An error occurred while connecting to the database:",err)

    # create tables to collect statistics
    @log_action
    def setup_database_tables(self):

        try:
            logging.debug("Creating tables in database...")
            self.cur.execute("CREATE TABLE IF NOT EXISTS disk (time TIMESTAMP, disk_name TEXT, size TEXT, used TEXT, Avail TEXT, duse TEXT, Mount_on TEXT);")
            self.cur.execute("CREATE TABLE IF NOT EXISTS memory (time TIMESTAMP, name TEXT, total INTEGER, used INTEGER, free INTEGER, shared INTEGER, buff INTEGER, available INTEGER);")
            self.cur.execute("CREATE TABLE IF NOT EXISTS cpu (time TIMESTAMP, cpu_name TEXT, usr FLOAT, nice FLOAT, sys FLOAT, iowait FLOAT, irq FLOAT, soft FLOAT, steal FLOAT, guest FLOAT, gnice FLOAT, idle FLOAT);")
            logging.info("Tables creation done successfully.")

        except Exception as e:
            print("Error setting up database tables: ", e)

    @log_action
    def set_disks_usage_in_db(self):
        try:
            disks = statistics.get_disks_usage()

            logging.debug("Inserting disks usage into disk table...")
            for item in disks:
                dt_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.cur.execute("INSERT INTO disk (time, disk_name, size, used, Avail, duse, Mount_on) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                 (datetime.datetime.now(), item["Filesystem"], item["Size"], item["Used"], item["Avail"], item["Use%"], item["Mounted"]))
            self.mydb.commit()
            logging.info("Insertion done successfully.")
        except Exception as e:
            logging.exception("Error setting disks usage in database: ", e)

    @log_action
    def set_memory_usage_in_db(self):
        try:
            memory = statistics.get_memory_usage()
            logging.debug("Inserting memory usage into memory table...")
            for item in memory:
                if item["name"] == "Swap:": # swap memory cause it has specific attributes
                    self.cur.execute("INSERT INTO memory (time, name, total, used, free, shared, buff, available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (datetime.datetime.now(), item["name"], item["total"], item["used"], item["free"], 0, 0, 0))

                else:
                    self.cur.execute("INSERT INTO memory (time, name, total, used, free, shared, buff, available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (datetime.datetime.now(), item["name"], item["total"], item["used"], item["free"], item["shared"], item["buff/cache"], item["available"]))
            self.mydb.commit()
            logging.info("Inserting done successfully.")
        except Exception as e:
            logging.exception("Error setting memory usage in database: ", e)

    @log_action
    def set_cpu_usage_in_db(self):
        try:
            cpu = statistics.get_cpu_usage()
            logging.debug("Inserting CPU usage into cpu table...")

            for item in cpu:
                self.cur.execute("INSERT INTO cpu (time, cpu_name, usr, nice, sys, iowait, irq, soft, steal, guest, gnice, idle) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (datetime.datetime.now(), item["CPU"], item["usr"], item["nice"], item["sys"], item["iowait"], item["irq"], item["soft"],
                        item["steal"], item["guest"], item["gnice"], item["idle"]))

            self.mydb.commit()
            logging.info("Inserting done successfully.")
        except Exception as e:
            logging.exception("Error setting CPU usage in database: ", e)

    # this function will execute each hour to remove any recored has more than 24 hours created
    @log_action
    def refresh_database(self):
        try:
            # Get all tables from the database
            load_dotenv()
            mydb = mysql.connector.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), passwd=os.getenv("DB_PASS"), database=os.getenv("DB_NAME"), port=os.getenv("DB_PORT"))
            cur = self.mydb.cursor()
            cur.execute("SHOW TABLES")
            table_names = [table[0] for table in self.cur]
            logging.info("All database tables names are collected successfully.")

            # Delete rows older than 259200 sec (3 days)
            logging.debug("Fetching old data(created since morethan one day)....")
            for table in table_names:
                cur.execute("DELETE FROM {} WHERE UNIX_TIMESTAMP() - UNIX_TIMESTAMP(time) > 259200".format(table))

            mydb.commit()
            logging.info("data fetch done successfully.")
        except Exception as e:
            logging.exception("Error occurn while refresh the database: ", e)

    @log_action
    def close_conncetion(self):
        logging.debug("Closing conncetion.....")
        self.mydb.close()
        logging.info("Concetion closed.")

    @log_action
    def get_usage_from_db(self,table_name):
        try:
            load_dotenv()
            mydb = mysql.connector.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), passwd=os.getenv("DB_PASS"), database=os.getenv("DB_NAME"), port=os.getenv("DB_PORT"))
            cur = mydb.cursor()
            logging.debug(f"Getting {table_name} usage from {table_name} table.")
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()

            result = [dict(zip([key[0] for key in cur.description], row)) for row in rows]
            logging.info(f"Convert {table_name} usage to dictonary format successfully.")
            return result
        except Exception as e:
            logging.error(f"Error while fetching data from the database: {e}")
            result = None
        finally:
            mydb.close()

if __name__ == "__main__":
   app = MonitoringAppDatabase()
   app.setup_database_tables()
   app.set_disks_usage_in_db()
   app.set_memory_usage_in_db()
   app.set_cpu_usage_in_db()
   app.refresh_database()
   app.close_conncetion()