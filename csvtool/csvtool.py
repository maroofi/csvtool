#!/usr/bin/python3
import csv
import argparse
import os

def open_file(filename):
    try:
        return open(filename, 'r', newline='', encoding='utf-8')
    except IOError as e:
        print(f"Error opening file {filename}: {e}")
        raise

def open_file_binary(filename):
    try:
        return open(filename, 'rb')
    except IOError as e:
        print(f"Error opening binary file {filename}: {e}")
        raise

def read_csv(file_path):
    with open_file(file_path) as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def display_csv(file_path):
    data = read_csv(file_path)
    for row in data:
        print(', '.join(row))

def count_rows(file_path):
    data = read_csv(file_path)
    print(f"Row count: {len(data)}")

def add_row(file_path, row_data):
    data = read_csv(file_path)
    data.append(row_data)
    write_csv(file_path, data)
    print("Row added successfully.")

def delete_row(file_path, row_index):
    data = read_csv(file_path)
    if 0 <= row_index < len(data):
        data.pop(row_index)
        write_csv(file_path, data)
        print("Row deleted successfully.")
    else:
        print("Invalid row index.")

def search_in_csv(file_path, search_term):
    data = read_csv(file_path)
    results = [row for row in data if search_term in row]
    print("Search results:")
    for row in results:
        print(', '.join(row))

def replace_value(file_path, old_value, new_value):
    """Replace all occurrences of old_value with new_value in the specified CSV file."""
    data = read_csv(file_path)
    for row in data:
        for i, value in enumerate(row):
            if value == old_value:
                row[i] = new_value
    write_csv(file_path, data)
    print(f"Replaced all instances of '{old_value}' with '{new_value}' in {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add replace command
    replace_parser = subparsers.add_parser('replace', help='Replace a specific value in the CSV file')
    replace_parser.add_argument('file', help='Path to the CSV file')
    replace_parser.add_argument('old_value', help='Value to replace')
    replace_parser.add_argument('new_value', help='New value to replace with')

    args = parser.parse_args()

    if args.command == 'replace':
        replace_value(args.file, args.old_value, args.new_value)
