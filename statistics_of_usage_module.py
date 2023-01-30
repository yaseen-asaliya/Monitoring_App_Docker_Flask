import subprocess
import logging
from logger import log_action

def get_data_as_lines(arr):
    try:
        output = subprocess.check_output(arr).decode("utf-8")
        logging.info(f"Data collected from command '{' '.join(map(str, arr))}' successfully.")
        return output.strip().split("\n")
    except subprocess.CalledProcessError as e:
        logging.exception("Error in getting data from the subprocess:", e)
        return []

def get_data_as_dict(headers, lines, start_line, typ):
    try:
        data = []
        for line in lines[start_line:]:
            values = line.split()
            if typ == 'c':
                values = values[1:]
            data.append(dict(zip(headers, values)))
        logging.info("Data converted to dictionary format successfully")
        return data
    except Exception as e:
        logging.error(f"{__name__} Error in parsing data:", e)
        return []

@log_action
def get_disks_usage():
    try:
        lines = get_data_as_lines(["df", "-h"])
        logging.info("Disks statistics convertd to lines format successfully.")
        headers = lines[0].split()
        return get_data_as_dict(headers, lines, 1, 'd')
    except Exception as e:
        print("Error in getting disk usage:", e)
        return []

@log_action
def get_memory_usage():
    try:
        lines = get_data_as_lines(["free", "-m"])
        logging.info("Memory statistics convertd to lines format successfully.")
        headers = lines[0].split()
        headers.insert(0, "name")
        return get_data_as_dict(headers, lines, 1, 'm')
    except Exception as e:
        print("Error in getting memory usage:", e)
        return []

@log_action
def get_cpu_usage():
    try:
        lines = get_data_as_lines(["mpstat", "-P","ALL"])
        logging.info("CPU statistics convertd to lines format successfully.")
        headers = lines[2].split()
        headers = headers[1:]
        headers = [name[1:] for name in headers[1:]] # to remove % sign from keys names
        headers.insert(0,"CPU")
        return get_data_as_dict(headers, lines, 3, 'c')
    except Exception as e:
        print("Error in getting CPU usage:", e)
        return []
