#!/usr/bin/env python

import setuptools

if __name__ == "__main__":
    setuptools.setup(
    name="aecg100",
    version="1.1.0.18",
    author="WHALETEQ Co., LTD",
    description="WHALETEQ Co., LTD AECG100 Linux SDK",
    url="https://www.whaleteq.com/en/Support/Download/7/Linux%20SDK",
    include_package_data=True,
    package_data={
        '': ['sdk/*.so', 'sdk/*.h', 'sample/python/*.txt']       
    },
)

