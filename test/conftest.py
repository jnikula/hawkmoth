import sys
from hawkmoth.doccursor import DocCursor

def pytest_sessionfinish(session, exitstatus):
    print('\n>>> DocCursor cache stats:', file=sys.stderr)
    print(DocCursor.cache_info(), file=sys.stderr)
