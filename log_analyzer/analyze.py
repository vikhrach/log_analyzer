import gzip
import datetime
import re
import os
from collections import namedtuple

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

def extract_date_from_filename(filename):
    # Define the regular expression pattern
    pattern = r'nginx-access-ui\.log-(\d{8})\.*'
    
    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    
    if match:
        # Extract the date part (YYYYMMDD)
        return datetime.datetime.strptime(match.group(1),'%Y%m%d')
    else:
        return None  # If no match is found

def search_latest_logfile(log_dir):
    maxdate = datetime.datetime.fromtimestamp(0)
    maxpath = ""
    for i in os.listdir(log_dir):
        curpath = os.path.join(log_dir,i)
        curdate = extract_date_from_filename(curpath)
        if  curdate > maxdate:
            maxdate = curdate
            maxpath = curpath
    return curpath

def get_request_time_generator(file_path):
    # Check if the file is a GZIP file
    with gzip.open(file_path, 'rt') if file_path.endswith('.gz') else open(file_path, 'r') as file:
        for line in file: 
            pattern = r'(?P<url>(?<= )(/\S*)).*(?P<request_time>\d+\.\d+)$'
            match = re.search(pattern, line)
            if not match:
               continue
            yield (match.group('url'), match.group('request_time'))
            
   
def collect_data(generator):
    raw_data = {}
    general_count = 0
    general_time = 0.
    for url,request_time in generator:
        request_time = float(request_time)
        general_count+=1
        general_time+=request_time
        raw_data.setdefault(url,[]).append(request_time)
    return (raw_data,general_count,general_time)

def get_statistics(data):
    
    statistics = {}
    for k,v in data[0].items():
        count = len(v)
        time_sum = sum(v)
        statistics[k] = {"count":count,
                         "count_perc":count/data[1],
                         "time_sum":time_sum,
                         "time_perc":time_sum/data[2],
                         "time_avg":time_sum/count,
                         "time_max":max(v),
                         "time_min":min(v)}
    return statistics
    

log_file = search_latest_logfile(config["LOG_DIR"])
request_time_generator = get_request_time_generator(log_file)
raw_data = collect_data(request_time_generator)
analyzed_data = get_statistics(raw_data)
print(log_file)
print(extract_date_from_filename(log_file))
print(analyzed_data)
