time.gmtime(0)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)
a=time.gmtime(0)
time.strftime('%Y-%m-%dT%H:%M:%SZ', a)
'1970-01-01T00:00:00Z'