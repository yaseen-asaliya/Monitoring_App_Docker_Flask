import socket
import requests
import shutil
import json

# Get current ip-address for container
def get_container_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    
def get_data_from_url(endpoint):
    base_url = f"http://{container_ip}:5000"
    response = requests.get(base_url + endpoint)
    result = []
    if response.status_code == 200:
        print("The request was successful. The response content:")
        result = response.content
    else:
        print("The request failed with status code:", response.status_code) 
    return result

def get_css():
        return """
        <style>
        a {
        font-weight: bold;
        margin-right: 10px;
        text-decoration: none;
        }

        h2 {
         margin-bottom: 10px;
        }
        table {
        border-collapse: collapse;
        width: 100%;
        }

        th, td {
        border: 1px solid #dddddd;
        padding: 8px;
        text-align: left;
        }

        th {
        background-color: #dddddd;
        font-weight: bold;
        }
        
         .buttons {
        display: flex;
        justify-content: left;
        align-items: center;
        height: 60px;
      }

      .button {
        background-color: #938f8f; 
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
      }
      
        </style>
    """

def get_table_header(arr):
    result = "<tr>\n"
    for item in arr:
        result += f"<th>{item}</th>\n"
    result += "</tr>\n"
    return result
    
def get_buttons():
    return """
    <div class="buttons">
      <a href="disk.html" class="button">Disks</a>
      <a href="memory.html" class="button">Memorys</a>
      <a href="cpu.html" class="button">CPU</a>
    </div>
    """

def get_tabel(data):
    result = ""
    for item in data: 
        result += "<tr>\n"
        for element in item:
            result += f"<th>{item[element]}</th>\n"
        result += "</tr>\n"
    return result

def create_html_file(file_name, table_name, header, data):
    with open(file_name,"w") as file:
        file.write("<!DOCTYPE html><html><head>")
        file.write(get_css())
        file.write("</head><body>\n")
        file.write(get_buttons())
        
        file.write(f"<div>\n<h2>Current {table_name} Usage</h2><br><table>") 
        file.write(get_table_header(header))
        file.write(get_tabel(data['current']))
        
        file.write(f"</table></div>\n</div>\n<h2>{table_name} Usage for last 24h</h2><br><table>")   
        header.insert(0,"Time")
        file.write(get_table_header(header))
        file.write(get_tabel(data['usage_for_last_24h']))
        file.write("</table>\n</div></html></body>")
        
def initilaize_html_files():
    disk_header = ["Filesystem","Size","Used","Avail","Use","Mounted on"]
    memory_header = ["Name","Total","Used","Free","Shared","Buff/cache","Available"]
    cpu_header = ["CPU","usr%","nice%","sys%","iowait%","irq%","soft%","steal%","guest%","gnice%","idle%"]
    
    create_html_file("disk.html","Disks",disk_header,disk)
    create_html_file("memory.html","Memorys",memory_header,memory)
    create_html_file("cpu.html","CPU",cpu_header,cpu)

def copy_file_to_apache_dir():
    files = ["disk","memory","cpu"]
    
    for file_name in files:
        src_dir = f"/app/{file_name}.html"
        dst_dir = f"/var/www/html/{file_name}.html"
        shutil.move(src_dir, dst_dir)
        
if __name__ == "__main__":
    container_ip = get_container_ip()
    disk = json.loads(get_data_from_url("/disk"))
    memory = json.loads(get_data_from_url("/memory"))
    cpu = json.loads(get_data_from_url("/cpu"))
    
    initilaize_html_files()
    copy_file_to_apache_dir()
