print(">>> conftest.py LOADED")

import icontract

def pytest_configure():
    # Enable contracts explicitly (on by default, but explicit is good)
    icontract._globals.ENABLED = True
