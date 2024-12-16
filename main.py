import argparse

import log_analyzer.analyzer as analyzer

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./report",
    "LOG_DIR": "./log",
    "FILE_PATTERN": r"nginx-access-ui\.log-(\d{8})\[gz|txt]",
    "REPORT_TEMPLATE_PATH": "./report/report.html",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to use a configuration file in JSON format")
    parser.add_argument("--config", required=False, help="Path to the config JSON file")

    # Parse arguments
    args = parser.parse_args()

    # Read and process the config file
    priority_config = analyzer.read_config(args.config)

    analyzer.analyze_log(config)
