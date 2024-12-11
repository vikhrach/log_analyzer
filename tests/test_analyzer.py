import datetime

import log_analyzer.analyzer


def test_extract_date_from_filename():
    reference_date = datetime.datetime(year=2017, month=6, day=30)
    assert log_analyzer.analyzer.extract_date_from_filename("nginx-access-ui.log-20170630.gz") == reference_date
    assert log_analyzer.analyzer.extract_date_from_filename("nginx-access-ui.log-20170630.txt") == reference_date
    assert log_analyzer.analyzer.extract_date_from_filename("nginx-access-ui.log-20170630.bz2") == None
