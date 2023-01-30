import statistics_of_usage_module as statistics
import sqlite3
import logging
from logger import log_action

@log_action
def get_current_disks_usage():
    try:
        logging.debug("Collecting current disks usage.")
        return statistics.get_disks_usage()
    except Exception as e:
        print("Error while collecting current disk usage:", e)
        return []

@log_action
def get_current_memory_usage():
    try:
        logging.debug("Collecting current memory usage.")
        return statistics.get_memory_usage()
    except Exception as e:
        print("Error while collecting current memory usage:", e)
        return []

@log_action
def get_current_cpu_usage():
    try:
        logging.debug("Collecting current CPU usage.")
        return statistics.get_cpu_usage()
    except Exception as e:
        print("Error while collecting current CPU usage:", e)
        return []

def get_usage_from_db(table_name):
    try:
        logging.debug("Connecting to the database.")
        conn = sqlite3.connect('/root/monitoring_app.db')
        cursor = conn.cursor()
        logging.info("Database connected successfully.")

        logging.debug(f"Getting {table_name} usage from {table_name} table.")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        logging.info(f"Getting data from {table_name} successfully.")

        result = [dict(zip([key[0] for key in cursor.description], row)) for row in rows]
        logging.info(f"Convert {table_name} usage to dictonary format successfully.")
        return result
    except Exception as e:
        logging.error(f"Error while fetching data from the database: {e}")
        result = None
    finally:
        logging.debug("Closing connection.")
        conn.close()
        logging.info("Conncetion closed.")

@log_action
def get_disks_usage_24h():
    try:
        logging.debug("Collecting disks usage for the past 24h.")
        return get_usage_from_db('disks')
    except Exception as e:
        print("Error while collecting CPU usage from database:", e)
        return []

@log_action
def get_memory_usage_24h():
    try:
        logging.debug("Collecting memory usage for the past 24h.")
        return get_usage_from_db('memory')
    except Exception as e:
        print("Error while collecting memory usage from database:", e)
        return []

@log_action
def get_cpu_usage_24h():
    try:
        logging.debug("Collecting CPU usage for the past 24h.")
        return get_usage_from_db('cpu')
    except Exception as e:
        print("Error while collecting CPU usage from database:", e)
        return []
