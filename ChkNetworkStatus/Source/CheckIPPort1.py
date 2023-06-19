__author__ = "Alex Mclachlan"
__email__ = "Alex.mclachlan.3@studytafensw.edu.au"
__copyright__ = "Copyright Gelos Enterprise"
__license__ = "Proprietary"
__last_update_date__ = "00/00/0000"
__version__ = "1.0.1"
__status__ = "Development"

"""Describe the program here in few sentences"""
# The user provides a subnet prefix and mask to check computers.
# Validating the input, the script imports defined ports from "ports.txt".
# IP addresses within the range are generated, excluding the
# top 10 reserved for printers/servers and those evenly numbered.
# For each IP, all ports are scanned, and their status (open/closed) is
# output to the console, log file (ip_port_log.txt), and Windows event log.
# The code, developed in Python, runs on a current MS Windows OS.

# Imports
import socket
import ipaddress
import win32evtlogutil
import os
# Functions


def log_to_file(message):
    """Logs to file"""
    file_out_a = open("ip_port_log.txt", "a")
    file_out_a.write(str(message) + "\n")
    file_out_a.close()

def validate_ip_address(my_ip_address):
    """Validate the ip address"""
    try:
        ipaddress.IPv4Address(my_ip_address)
        #print("Valid")
        return True
    except ipaddress.AddressValueError:
        #print("invalid")
        return False

def validate_subnet_mask(an_ip_address, a_subnet_mask):
    """Validate the subnet mask"""
    ip_range = an_ip_address + "/" + a_subnet_mask  # eg 192.168.0.1/255.255.255.0
    try:
        ipaddress.IPv4Network(ip_range)
        return True
    except ValueError:
        print("Invalid subnet mask")

def write_event_viewer_log(message, event_type):
    """Write to the system log (event viewer)"""
    win32evtlogutil.ReportEvent(
        appName="CheckIPPort - IP/Port Scanner",
        eventID=1337,
        eventCategory=9000,
        eventType=event_type,
        strings=message,
        data=b"CheckIPPort")



# Program
os.chdir(os.path.dirname(__file__))

print(" \x1B[4m" + "Welcome to Port Scanner" + "\n\x1B[0m", "\x1B[4m" "Let's scan some ports!" "\x1B[0m\n")

subnet_prefix = input("Input the subnet prefix:")
valid_ip = validate_ip_address(subnet_prefix + ".1")
while not valid_ip:
    subnet_prefix = input("Input the subnet prefix:")
    valid_ip = validate_ip_address(subnet_prefix + ".1")

valid_subnet_mask = False
while not valid_subnet_mask:
    subnet_mask = input("Enter the subnet mask: ")
    sample_ip = subnet_prefix + ".0"
    valid_subnet_mask = validate_subnet_mask(sample_ip, subnet_mask)

ips_list = [subnet_prefix + "." + str(num) for num in range(11, 50, 2)]


ports_file_in = open("..\Parameters\ports.txt", "r")
ports_list = []
for port in ports_file_in:
    ports_list.append(port)

for ip in ips_list:
    for line in ports_list:
        port = line.rstrip("\n")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
            print(ip + "/" + subnet_mask +f": Port {port.rstrip()} is open")
            status_message = ["IP:" + str(ip) + " Port:" + str(port) + " Open!"]
            write_event_viewer_log(status_message, 0)  # event types: 0=info 1=error 2=warning
            log_to_file(status_message)
        else:
            print(ip + "/" + subnet_mask + f": Port, {port.rstrip()} is Closed")
            status_message = [str(ip) + " " + str(port) + " Closed!"]
            write_event_viewer_log(status_message, 0)
        sock.close()