import datetime
import gzip
import os
import re

config = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./log"}


def extract_date_from_filename(
    filename: str, pattern=r"nginx-access-ui\.log-(\d{8})\.*"
) -> datetime.datetime | None:
    match = re.search(pattern, filename)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y%m%d")
    else:
        return None  # If no match is found


def search_latest_logfile(log_dir: str) -> str:
    maxdate = datetime.datetime.fromtimestamp(0)
    for i in os.listdir(log_dir):
        curpath = os.path.join(log_dir, i)
        curdate = extract_date_from_filename(curpath)
        if not curdate:
            break
        if curdate > maxdate:
            maxdate = curdate
            maxpath = curpath
    return maxpath


def get_request_time_generator(file_path: str):
    # Check if the file is a GZIP file
    with (
        gzip.open(file_path, "rt")
        if file_path.endswith(".gz")
        else open(file_path, "r")
    ) as file:
        for line in file:
            pattern = r"(?P<url>(?<= )(/\S*)).*(?P<request_time>\d+\.\d+)$"
            match = re.search(pattern, line)
            if not match:
                continue
            yield (match.group("url"), match.group("request_time"))


def collect_data(generator) -> tuple[dict[str, list[float]], int, float]:
    raw_data: dict[str, list[float]] = {}
    general_count = 0
    general_time = 0.0
    for url, request_time in generator:
        request_time = float(request_time)
        general_count += 1
        general_time += request_time
        raw_data.setdefault(url, []).append(request_time)
    return (raw_data, general_count, general_time)


def get_statistics(data, all_count, all_time):
    statistics = {}
    for k, v in data.items():
        count = len(v)
        time_sum_per_url = sum(v)
        statistics[k] = {
            "count": count,
            "count_perc": count / all_count,
            "time_sum": time_sum_per_url,
            "time_perc": time_sum_per_url / all_time,
            "time_avg": time_sum_per_url / count,
            "time_max": max(v),
            "time_min": min(v),
        }
    return statistics


log_file = search_latest_logfile(str(config["LOG_DIR"]))
request_time_generator = get_request_time_generator(log_file)
raw_data = collect_data(request_time_generator)
analyzed_data = get_statistics(*raw_data)
print(log_file)
# print(extract_date_from_filename(log_file))
print(analyzed_data)
