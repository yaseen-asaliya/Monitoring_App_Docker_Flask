from flask import Flask
import statistics_of_usage as stat
import logging
from logger import log_action

app = Flask(__name__)


@log_action
@app.route("/disk")
def get_disks_usage():
   try:
      current_disk_usage = stat.get_current_disks_usage()
      logging.info("Current disks usage collected successfully.")
      disk_usage_24h = stat.get_disks_usage_24h()
      logging.info("Disks usage for past 24h collected successfully.")

      disks = {"current": current_disk_usage,"usage_for_last_24h": disk_usage_24h}
      return disks
   except  Exception as e:
      logging.error("An error occurred while collecting disk usage statistics using /disks endpoint : ", e)
      return []

@log_action
@app.route("/memory")
def get_memory_usage():
   try:
      current_memory_usage = stat.get_current_memory_usage()
      logging.info("Current memory usage collected successfully.")
      memory_usage_24h = stat.get_memory_usage_24h()
      logging.info("Memory usage for past 24h collected successfully.")

      memorys = {"current": current_memory_usage,"usage_for_last_24h": memory_usage_24h}
      return memorys
   except  Exception as e:
      logging.error("An error occurred while collecting memory usage statistics using /memory endpoint : ", e)
      return []

@log_action
@app.route("/cpu")
def get_cpu_usage():
   try:
      current_cpu_usage = stat.get_current_cpu_usage()
      logging.info("Current CPU usage collected successfully.")
      cpu_usage_24h = stat.get_cpu_usage_24h()
      logging.info("CPU usage for past 24h collected successfully.")

      cpus = {"current": current_cpu_usage,"usage_for_last_24h": cpu_usage_24h}
      return cpus
   except  Exception as e:
      logging.error("An error occurred while collecting CPU usage statistics using /cpu endpoint : ", e)
      return []


if __name__ == "__main__":
   logging.debug("Starting flask server....")
   app.run()