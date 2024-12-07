#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Student Name"
Semester: "Enter Winter/Summer/Fall Year"

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os
import sys


def parse_command_args():
    """
    Parse command-line arguments for the script using argparse.
    """
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts")
    parser.add_argument('program', nargs='?', help='The program to check memory usage for (optional)')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Print memory sizes in human-readable format')
    parser.add_argument('-l', '--length', type=int, default=20, help='Length of the bar graph')
    
    args = parser.parse_args()
    return args

# create argparse function
# -H human readable
# -r running only

def percent_to_graph(pcnt, max_value):
    # Validate input
    if not (0.0 <= pcnt <= 1.0) or not isinstance(max_value, int) or max_value <= 0:
        return "Invalid input"

    # Calculate the number of '#' and ' ' to represent the percentage
    num_hashes = int(pcnt * max_value)  # Calculate based on proportion
    num_spaces = max_value - num_hashes

    # Return the graph representation
    return "#" * num_hashes + " " * num_spaces


    # Calculate the number of '#' and ' ' to represent the percentage
    num_hashes = int(percentage // 10)  # Each '#' represents 10%
    num_spaces = 10 - num_hashes       # Remaining spaces to make up 10

    # Return the graph representation
    return "#" * num_hashes + " " * num_spaces

    ...
# percent to graph function

def get_sys_mem():
    """
    Get total system memory in kilobytes from /proc/meminfo.
    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                total_mem = int(line.split()[1])
                return total_mem

def get_avail_mem():
    """
    Get available memory in kilobytes from /proc/meminfo.
    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemAvailable'):
                available_mem = int(line.split()[1])
                return available_mem


def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
    else:
        ...
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
