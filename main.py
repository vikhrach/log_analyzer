import argparse
import pathlib

import structlog

import log_analyzer.analyzer as analyzer

logger = structlog.get_logger()

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./report",
    "LOG_DIR": "./log",
    "FILE_PATTERN": r"nginx-access-ui\.log-(\d{8})\[gz|txt]",
    "REPORT_TEMPLATE_PATH": "./report/report.html",
}

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Script to use a configuration file in JSON format")
        parser.add_argument("--config", required=False, help="Path to the config JSON file")
        args = parser.parse_args()
        priority_config = analyzer.read_config(args.config)
        config = analyzer.merge_configs(priority_config, config)

        structlog.configure(
            processors=[
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.WriteLoggerFactory(
                pathlib.Path(str(config["LOG_DIR"]), "log_analyzer.json").open("wt")
            ),
        )
        analyzer.analyze_log(config)
        logger.info("Analyzing completed")
    except Exception:
        logger.exception("Cannot analyze")
