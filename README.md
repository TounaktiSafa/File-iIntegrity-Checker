# Log File Integrity Checker Tool

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A security tool that monitors log files for unauthorized modifications using cryptographic hashing (SHA-256).

## Features

- Detects tampering in log files by comparing current hashes with stored baselines
- Supports both single files and entire directories
- Simple command-line interface
- Secure hash storage in JSON format
- Cross-platform (works on Linux, macOS, Windows)

## Installation

1. **Prerequisites**: Python 3.6 or higher

2. **Install directly**:
   ```bash
   pip install git+https://github.com/TounaktiSafa/File-iIntegrity-Checker.git
