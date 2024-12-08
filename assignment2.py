#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Kamith Balasooriya
Semester: Summer

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script visualizes system memory usage, and can also show memory usage of a specific program. 
It displays memory usage in a bar chart format, with the option for human-readable memory sizes.

'''

import argparse
import os
import sys

def parse_command_args():
    """
    Parse command-line arguments for the script using argparse.

    This function sets up the command-line interface, allowing the user to specify:
    - A program name to check memory usage for.
    - Whether to display memory in human-readable format.
    - The length of the bar graph representing memory usage.
    """
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts")
    parser.add_argument('program', nargs='?', help='The program to check memory usage for (optional)')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Print memory sizes in human-readable format')
    parser.add_argument('-l', '--length', type=int, default=20, help='Length of the bar graph')
    
    args = parser.parse_args()
    return args


def percent_to_graph(pcnt, max_value):
    """ 
     Convert percentage to a bar graph of '#' characters.
    
     Args:
        pcnt (float): The percentage of memory usage, between 0.0 and 1.0.
        max_value (int): The maximum length of the bar graph.

    Returns:
        str: A string representation of the bar graph.
    
    """
    # Validate input
    if not (0.0 <= pcnt <= 1.0) or not isinstance(max_value, int) or max_value <= 0:
        return "Invalid input"

    # Calculate the number of '#' and ' ' to represent the percentage
    num_hashes = int(pcnt * max_value)  # Calculate based on proportion
    num_spaces = max_value - num_hashes

    # Return the graph representation
    return "#" * num_hashes + " " * num_spaces


    # Calculate the number of '#' and ' ' to represent the percentage
    num_hashes = int(percentage // 10)  # Calculate based on proportion
    num_spaces = 10 - num_hashes       

    # Return the graph representation
    return "#" * num_hashes + " " * num_spaces

    ...

def get_sys_mem():
    """
    Get total system memory in kilobytes from /proc/meminfo.

    Reads from the '/proc/meminfo' file to get the total system memory in KiB.
    
    Returns:
        int: Total system memory in kilobytes.
        
    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                total_mem = int(line.split()[1])
                return total_mem

def get_avail_mem():
    """
    Get available memory in kilobytes from /proc/meminfo.

    Reads from the '/proc/meminfo' file to get the available memory in KiB.
    
    Returns:
        int: Available memory in kilobytes.

    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemAvailable'):
                available_mem = int(line.split()[1])
                return available_mem


def pids_of_prog(app_name: str) -> list:
    """
    Given an app name, return all PIDs associated with the app.

    Args:
        app_name (str): The name of the program to get the PIDs for.

    Returns:
        list: A list of process IDs (PIDs) of the given program, or an empty list if not found.

    """
    try:
        # Use os.popen to call the "pidof" command and read the output
        result = os.popen(f"pidof {app_name}").read().strip()
        # If result is not empty, split into a list of PIDs, else return an empty list
        return result.split() if result else []
    except Exception:
        # Return an empty list in case of an exception
        return []


def rss_mem_of_pid(proc_id: str) -> int:
    """
   Given a process ID, return the total RSS memory used by the process in kilobytes.
    If the PID doesn't exist or the file can't be opened, return 0.

    Args:
        proc_id (str): The process ID to check.

    Returns:
        int: The total RSS memory in kilobytes used by the process.
    """
    try:
        # Define the path to the smaps file for the process
        smaps_path = f'/proc/{proc_id}/smaps'
        
        # Open the smaps file to read the memory usage
        with open(smaps_path, 'r') as smaps_file:
            total_rss = 0
            # Read through each line in the smaps file
            for line in smaps_file:
                # Look for lines that contain "Rss" (resident set size) information
                if line.startswith('Rss'):
                    # Each Rss line contains the memory size in kilobytes
                    rss_kb = int(line.split()[1])  # Extract the value and convert it to integer
                    total_rss += rss_kb  # Accumulate the RSS memory

            # Return the total RSS memory found in kilobytes
            return total_rss
    except FileNotFoundError:
        # If the process does not exist or smaps file cannot be opened, return 0
        return 0
    except Exception as e:
        # In case of any unexpected error, print and return 0
        print(f"Error reading smaps for PID {proc_id}: {e}")
        return 0


def bytes_to_human_r(kibibytes: int, decimal_places: int = 2) -> str:
    """
        Convert memory in kibibytes (KiB) to a human-readable format (e.g., MiB, GiB, TiB).

    Args:
        kibibytes (int): The memory amount in KiB to convert.
        decimal_places (int): Number of decimal places to include in the output.

    Returns:
        str: A string representation of the memory in the most appropriate unit.
        
    """
    # Define units in increasing order
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # Base-1024 units
    suf_count = 0  # Tracks which suffix to use
    result = kibibytes  # Start with the input in KiB

    # Divide by 1024 until the result is less than 1024 or we run out of suffixes
    while result > 1024 and suf_count < len(suffixes) - 1:
        result /= 1024  # Convert to the next higher unit
        suf_count += 1  # Move to the next suffix

    # Format the result to the specified number of decimal places and add the unit
    str_result = f'{result:.{decimal_places}f} {suffixes[suf_count]}'
    return str_result


if __name__ == "__main__":
    args = parse_command_args()

    if not args.program:  # No specific program provided
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem
        percentage_used = used_mem / total_mem

        # Check for human-readable flag
        if args.human_readable:
            total_mem_h = bytes_to_human_r(total_mem)
            used_mem_h = bytes_to_human_r(used_mem)
            print(f"System Memory (Human-Readable):\nUsed: {used_mem_h}\tTotal: {total_mem_h}")
        else:
            print(f"System Memory:\nUsed: {used_mem} KiB\tTotal: {total_mem} KiB")
        
        # Display the bar graph representation
        print(percent_to_graph(percentage_used, args.length))
    else:  # Program memory usage
        pids = pids_of_prog(args.program)
        if not pids:
            print(f"No running processes found for program '{args.program}'")
            sys.exit(1)

        total_rss = sum(rss_mem_of_pid(pid) for pid in pids)
        total_mem = get_sys_mem()
        percentage_used = total_rss / total_mem

        # Check for human-readable flag
        if args.human_readable:
            total_mem_h = bytes_to_human_r(total_mem)
            total_rss_h = bytes_to_human_r(total_rss)
            print(f"Memory Usage for '{args.program}' (Human-Readable):\nUsed: {total_rss_h}\tTotal: {total_mem_h}")
        else:
            print(f"Memory Usage for '{args.program}':\nUsed: {total_rss} KiB\tTotal: {total_mem} KiB")
        
        # Display the bar graph representation
        print(percent_to_graph(percentage_used, args.length))
