#!/usr/bin/env python
import os
import sys
import threading
import multiprocessing
import geoip2.database
import Tkinter

import Queue
import json
import requests

global IP_List

# Set Output file
# Set Threads / processes
# open nessary files and ensure we can create file in working directory
def file_handle():
    try:
        IP_output = open('iplist_output.txt', 'w+')
        IP_output.close()
        print "[*] Output File created"
    except:
        print "[!] Couldnt create file check permissions"
        sys.exit(0)
    try:
        with open("iplist2.txt") as f:
            IP_List = f.readlines()
        f.close()
        # Calculate the account of IP's loaded
        with open("iplist.txt") as myfile:
            count = sum(1 for line in myfile)
        print '[*] IP List loaded with:', count, " IP's"
    except:
        print "[!] Couldnt open file check file path!"
        sys.exit(0)
    return IP_List

def whois_geo_lookup(ip_queue, results_queue):
    while True:
        try:
            reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
        except Exception as e:
            print e
        ip = ip_queue.get()
        if ip is None:
            # Break out of the while loop to terminate Sub-Procs
            break
        try:
            ip = str(ip.rstrip())
            response = reader.country(ip)
            country = response.country.name
            output = ip + ' ' + country + '\n'
            print output
            results_queue.put(output)
        except Exception as e:
            print e

def printer(results_queue):
    while True:
        # Get item an print to output file
        try:
            # Must set time out due to blocking,
            item = results_queue.get(timeout=1)
            with open('iplist_output2.txt', "a") as myfile:
                myfile.write(item)
        except Exception as e:
            print e
            break
        # results_queue.task_done()
    return

def main():
    # Build Queue
    script_queue = multiprocessing.Queue()
    results_queue = multiprocessing.Queue()

    # lock = multiprocessing.Lock()
    # with lock:

    # Set time out for join method
    timeout = float(0.1)
    # Define max Threads and IP list
    total_proc = 50
    IP_List = file_handle()
    # Places all the IP's in the list into the Queue
    for IP in IP_List:
        script_queue.put(IP)

    for i in xrange(total_proc):
        script_queue.put(None)
    # Generate threads for worker
    procs = []
    for thread in range(total_proc):
        procs.append(multiprocessing.Process(target=whois_geo_lookup, args=(script_queue,results_queue,)))

    for p in procs:
        p.daemon = True
        p.start()
    # Removed for loop due to time and uneeded function, Set Float to reduce time of clossing, TESTING NEEDED!
    for p in procs:
        p.join(timeout)
    # Launches a single thread to output results
    t2 = threading.Thread(target=printer, args=(results_queue,))
    t2.daemon = True
    t2.start()
    t2.join()
    # Wait for queue to empty
    print "[*] Scan Complete!"


if __name__ == "__main__":
        try:
             main()
        except KeyboardInterrupt:
            print 'Interrupted'
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

