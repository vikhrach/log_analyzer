from log_analyzer.analyze import analyze_log
import argparse
import os
import json

config = {"REPORT_SIZE": 1000,
         "REPORT_DIR": "./report",
        "LOG_DIR": "./log", 
        "FILE_PATTERN":r"nginx-access-ui\.log-(\d{8})\.*",
        "REPORT_TEMPLATE_PATH":"./report/report.html"}

def read_config(config_path):
    # Check if the config file exists
    if not os.path.exists(config_path):
        print(f"Config file does not exist: {config_path}")
        return None
    
    # Try to load and parse the JSON configuration
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except json.JSONDecodeError:
        print(f"Error decoding JSON in the config file: {config_path}")
        return None



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to use a configuration file in JSON format")
    parser.add_argument('--config', required=False, help="Path to the config JSON file")

    # Parse arguments
    args = parser.parse_args()

    # Read and process the config file
    priority_config = read_config(args.config)

    analyze_log(config)