import socket
import threading
from queue import Queue
import os
import argparse

parser = argparse.ArgumentParser(description='Enter Target IP Address')
parser.add_argument('target', help='IP Address of Target')
args = parser.parse_args()
input_target = args.target
target = input_target

queue = Queue()
open_ports = []

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f" Port {port} on {target} is open")
            open_ports.append(port)

port_list = range(1, 20000)
fill_queue(port_list)

thread_list = []


for t in range(900):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()
