from log_analyzer.analyze import analyze_log

config = {"REPORT_SIZE": 1000,
         "REPORT_DIR": "./report",
        "LOG_DIR": "./log", 
        "FILE_PATTERN":r"nginx-access-ui\.log-(\d{8})\.*",
        "REPORT_TEMPLATE_PATH":"./report/report.html"}

if __name__ == '__main__':
    analyze_log(config)