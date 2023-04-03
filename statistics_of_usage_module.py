import logging
from logger import log_action
import os
import paramiko
from dotenv import load_dotenv

def open_ssh_to_collect_data(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    load_dotenv()
    ssh.connect(os.getenv("CLIENT_IP"), username=os.getenv("CLIENT_USER"), password=os.getenv("CLIENT_USER_PASS"))

    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()

    ssh.close()
    return result

def get_data_as_lines(command):
    try:
        output = open_ssh_to_collect_data(command)
        logging.info(f"Data collected from command '{command}' successfully.")
        return output.strip().split("\n")
    except Exception as e:
        logging.exception("Error in getting data from the subprocess:", e)
        return []

def get_data_as_dict(headers, lines, start_line, typ):
    try:
        data = []
        for line in lines[start_line:]:
            values = line.split()
            if typ == 'c':
                values = values[2:]
            data.append(dict(zip(headers, values)))
        logging.info("Data converted to dictionary format successfully")
        return data
    except Exception as e:
        logging.error(f"{__name__} Error in parsing data:", e)
        return []


@log_action
def get_disks_usage():
    try:
        lines = get_data_as_lines("df -h")
        logging.info("Disks statistics convertd to lines format successfully.")
        headers = lines[0].split()
        return get_data_as_dict(headers, lines, 1, 'd')
    except Exception as e:
        print("Error in getting disk usage:", e)
        return []

@log_action
def get_memory_usage():
    try:
        lines = get_data_as_lines("free -m")
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
        lines = get_data_as_lines("mpstat -P ALL")
        logging.info("CPU statistics convertd to lines format successfully.")
        headers = lines[2].split()
        headers = headers[2:]
        headers = [name[1:] for name in headers] # to remove % sign from keys names
        headers[0]="CPU"
        return get_data_as_dict(headers, lines, 3, 'c')
    except Exception as e:
        print("Error in getting CPU usage:", e)
        return []