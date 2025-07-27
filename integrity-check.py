#!/usr/bin/env python3
import os
import hashlib
import json
import argparse
from pathlib import Path

# Configuration
HASH_STORE = os.path.expanduser("~/.log_integrity_store.json")

def compute_file_hash(file_path):
    """Compute SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # Read in 64k chunks
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def load_hash_store():
    """Load the stored hashes from file"""
    try:
        with open(HASH_STORE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_hash_store(store):
    """Save the hash store to file"""
    try:
        with open(HASH_STORE, 'w') as f:
            json.dump(store, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving hash store: {e}")
        return False

def initialize(directory):
    """Initialize hash store with files in directory"""
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return False

    hash_store = {}
    processed_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = compute_file_hash(file_path)
            if file_hash:
                hash_store[file_path] = file_hash
                processed_files += 1

    if save_hash_store(hash_store):
        print(f"Hashes stored successfully for {processed_files} files.")
        return True
    return False

def check_file(file_path):
    """Check if a file's hash matches the stored hash"""
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file")
        return False

    hash_store = load_hash_store()
    current_hash = compute_file_hash(file_path)

    if file_path not in hash_store:
        print(f"Status: New file (not in hash store)")
        return False

    if current_hash == hash_store[file_path]:
        print("Status: Unmodified")
        return True
    else:
        print("Status: Modified (Hash mismatch)")
        return False

def update_file(file_path):
    """Update the stored hash for a file"""
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file")
        return False

    current_hash = compute_file_hash(file_path)
    if not current_hash:
        return False

    hash_store = load_hash_store()
    hash_store[file_path] = current_hash

    if save_hash_store(hash_store):
        print("Hash updated successfully.")
        return True
    return False

def check_directory(directory):
    """Check all files in a directory against stored hashes"""
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return False

    hash_store = load_hash_store()
    modified_files = []
    new_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_hash = compute_file_hash(file_path)
            
            if file_path not in hash_store:
                new_files.append(file_path)
            elif current_hash != hash_store[file_path]:
                modified_files.append(file_path)

    if not modified_files and not new_files:
        print("All files unmodified.")
        return True

    if modified_files:
        print("\nModified files:")
        for file in modified_files:
            print(f"- {file}")

    if new_files:
        print("\nNew files (not in hash store):")
        for file in new_files:
            print(f"- {file}")

    return False

def main():
    parser = argparse.ArgumentParser(description="Log file integrity checker")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize hash store')
    init_parser.add_argument('directory', help='Directory to scan for log files')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check file/directory')
    check_parser.add_argument('path', help='File or directory to check')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update hash for file')
    update_parser.add_argument('file', help='File to update in hash store')

    args = parser.parse_args()

    if args.command == 'init':
        initialize(args.directory)
    elif args.command == 'check':
        if os.path.isfile(args.path):
            check_file(args.path)
        elif os.path.isdir(args.path):
            check_directory(args.path)
        else:
            print(f"Error: {args.path} is not a valid file or directory")
    elif args.command == 'update':
        update_file(args.file)

if __name__ == "__main__":
    main()
