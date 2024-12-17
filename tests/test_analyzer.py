import datetime

import log_analyzer.analyzer


def test_extract_date_from_filename():
    reference_date = datetime.datetime(year=2017, month=6, day=30)
    pattern = r"nginx-access-ui\.log-(\d{8})\.[gz|txt]"
    assert (
        log_analyzer.analyzer.extract_date_from_filename("nginx-access-ui.log-20170630.gz", pattern) == reference_date
    )
    assert (
        log_analyzer.analyzer.extract_date_from_filename("nginx-access-ui.log-20170630.txt", pattern) == reference_date
    )
