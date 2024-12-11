import datetime
import gzip
import json
import os
import re
from string import Template

import structlog

log = structlog.get_logger()


def merge_configs(config_priority, config):
    """Merge two configuration dictionaries"""
    merged_config = config.copy()
    merged_config.update(config_priority)
    return merged_config


def extract_date_from_filename(filename: str, pattern: str) -> datetime.datetime | None:
    """Extract date from filename using pattern"""
    match = re.search(pattern, filename)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y%m%d")
    else:
        return None


def search_latest_logfile(log_dir: str, pattern: str) -> str:
    """Get latest logfile for analyzing"""
    log.info(f"searching latest logfile in {log_dir}")
    max_date = datetime.datetime.fromtimestamp(0)
    path_with_maxdate = ""
    for i in os.listdir(log_dir):
        current_log_path = os.path.join(log_dir, i)
        current_parsed_date = extract_date_from_filename(current_log_path, pattern)
        if not current_parsed_date:
            break
        if current_parsed_date > max_date:
            max_date = current_parsed_date
            path_with_maxdate = current_log_path
    if not path_with_maxdate:
        raise RuntimeError("Log files not parsed")
    return path_with_maxdate, max_date


def get_request_time_generator(file_path: str):
    """Read and parse line in logfile"""
    log.info("logfile parsing")
    with gzip.open(file_path, "rt") if file_path.endswith(".gz") else open(file_path, "r") as file:
        for line in file:
            pattern = r"(?P<url>(?<= )(/\S*)).*(?P<request_time>\d+\.\d+)$"
            match = re.search(pattern, line)
            if not match:
                continue
            yield (match.group("url"), match.group("request_time"))


def collect_data(generator) -> tuple[dict[str, list[float]], int, float]:
    """Aggregate all data from logfile"""
    raw_data: dict[str, list[float]] = {}
    general_count = 0
    general_time = 0.0
    for url, request_time in generator:
        request_time = float(request_time)
        general_count += 1
        general_time += request_time
        raw_data.setdefault(url, []).append(request_time)
    return (raw_data, general_count, general_time)


def get_statistics(config, data, all_count, all_time):
    """Calculate statistics"""
    log.info("generating statistics")
    statistics = []
    for k, v in data.items():
        count = len(v)
        time_sum_per_url = sum(v)
        statistics.append(
            {
                "url": k,
                "count": count,
                "count_perc": count / all_count,
                "time_sum": time_sum_per_url,
                "time_perc": time_sum_per_url / all_time,
                "time_avg": time_sum_per_url / count,
                "time_max": max(v),
                "time_min": min(v),
            }
        )
    statistics = sorted(statistics, key=lambda x: x["time_sum"], reverse=True)[: int(config["REPORT_SIZE"])]
    return statistics


def create_report_with_template(config, report_data, latest_date: datetime.datetime):
    report_file = config["REPORT_TEMPLATE_PATH"]
    report_dir = config["REPORT_DIR"]
    log.info(f"generating report in {report_dir}")
    with open(report_file, "r") as f:
        report_template = Template(f.read())
    print(json.dumps(report_data, ensure_ascii=False))
    with open(f"{report_dir}/report-{latest_date.strftime('%Y-%m-%d')}.html", "w") as f:
        f.write(report_template.safe_substitute(table_json=json.dumps(report_data, ensure_ascii=False)))


def analyze_log(config):
    """Analyze logs with given configuration"""
    log_file, latest_date = search_latest_logfile(str(config["LOG_DIR"]), str(config["FILE_PATTERN"]))
    request_time_generator = get_request_time_generator(log_file)
    raw_data = collect_data(request_time_generator)
    report_data = get_statistics(config, *raw_data)
    create_report_with_template(config, report_data, latest_date)
    return
