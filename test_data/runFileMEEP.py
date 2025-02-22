"""
    Team: MEEP
    Members: Mike Giles, Peter Nolan, Emma Bolduc, Eric Tech
    Date: 2/15/2025
    Course: COMSC 330
    Description: This program reads a GRP file and extracts the names of .txt files. It then reads each .txt file and prints its contents for testing.
"""

import re
import os

def extract_filenames(grp_filename):
    """Extracts .txt filenames from a GRP file."""
    try:
        with open(grp_filename, 'r', encoding= "utf-8") as file:
            content = file.read()
            print(content)
        return [fname.strip() for fname in re.findall(r'\S+\.SEC', content)]
    except FileNotFoundError:
        print(f"Error: GRP file '{grp_filename}' not found.")
        return []

def process_txt_file(sec_filename):
    """Reads and processes a .txt file."""
    try:
        with open(sec_filename, 'r', encoding= "utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Warning: File '{sec_filename}' not found.")
        return []

def main():
    grp_filename = 'test_data\COMSC330.GRP'
    sec_files = extract_filenames(grp_filename)
    print(sec_files)
    for i in range(0, len(sec_files)):
        sec_files[i] = 'test_data\\' + sec_files[i]
    print(sec_files)
    
    if not sec_files:
        print("Error: No .txt files found in GRP file.")
        return
    
    for sec_file in sec_files:
        file_data = process_txt_file(sec_file)
        print(f"\nContents of {sec_file}:")
        print(''.join(file_data) if file_data else "(Empty or not found)")

if __name__ == "__main__":
    main()
