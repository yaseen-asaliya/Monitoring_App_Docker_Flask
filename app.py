from flask import Flask
import statistics_of_usage_module as stat
import database_configrations as dbc
import logging
from logger import log_action
import json

app = Flask(__name__)
db = dbc.MonitoringAppDatabase()

@log_action
@app.route("/disk")
def get_disks_usage():
   try:
      current_disk_usage = stat.get_disks_usage()
      logging.info("Current disks usage collected successfully.")

      disk_usage_24h = db.get_usage_from_db('disk')
      logging.info("Disks usage for past 24h collected successfully.")

      disks = {"current": current_disk_usage,"usage_for_last_24h": disk_usage_24h}
      return json.dumps(disks, default=str)
   except Exception as e:
      logging.error("An error occurred while collecting disk usage statistics using /disks endpoint : ", e)
      return []

@log_action
@app.route("/memory")
def get_memory_usage():
   try:
      current_memory_usage = stat.get_memory_usage()
      logging.info("Current memory usage collected successfully.")

      memory_usage_24h = db.get_usage_from_db('memory')
      logging.info("Memory usage for past 24h collected successfully.")

      memorys = {"current": current_memory_usage,"usage_for_last_24h": memory_usage_24h}
      return json.dumps(memorys, default=str)
   except Exception as e:
      logging.error("An error occurred while collecting memory usage statistics using /memory endpoint : ", e)
      return []

@log_action
@app.route("/cpu")
def get_cpu_usage():
  try:
      current_cpu_usage = stat.get_cpu_usage()
      logging.info("Current CPU usage collected successfully.")

      cpu_usage_24h = db.get_usage_from_db('cpu')
      logging.info("CPU usage for past 24h collected successfully.")
      cpus = {"current": current_cpu_usage,"usage_for_last_24h": cpu_usage_24h}
      return json.dumps(cpus, default=str)
  except  Exception as e:
      logging.error("An error occurred while collecting CPU usage statistics using /cpu endpoint : ", e)
      return []


if __name__ == "__main__":
    logging.debug("Starting flask server....")
    app.run()