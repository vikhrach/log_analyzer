import datetime

from log_analyzer.analyzer import extract_date_from_filename


def test_extract_date_from_filename():
    reference_date = datetime.datetime(year=2017, month=6, day=30)
    pattern = r"nginx-access-ui\.log-(\d{8})\.[gz|txt]"
    assert extract_date_from_filename("nginx-access-ui.log-20170630.gz", pattern) == reference_date
    assert extract_date_from_filename("nginx-access-ui.log-20170630.txt", pattern) == reference_date
