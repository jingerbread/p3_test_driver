#!/bin/bash
# [DRAFT] version
# See full instruction in docs/run_tests_from_wsl_centos7.rst
# Script to build/install local p3_driver_package from src
# (checked only for WSL CentOS7)

# Run script from p3_test_driver root dir:
# ./scripts/update_local_package_from_src.sh
scriptName=${0##*/}

echo -e "\025[25mSet debug mode and exit upon error\025[0m"
set -ex
#  -e, --editable <path/url>
# Install a project in editable mode
pip install -e p3_test_driver

# Generating distribution archives
cd p3_test_driver && python setup.py sdist bdist_wheel
# The tar.gz file is a source archive
# whereas the .whl file is a built distribution.
ls -l dist/

#  Uninstall previous and install new package from dist
cd .. && yes | pip -v uninstall p3_test_driver
pip -v install p3_test_driver/dist/p3_test_driver-2.0.3-py3-none-any.whl

echo -e "\066[66m Update finished successfully\066[0m"
echo "Run test with f.e:"
echo "tests/perf-pulsar-tests/pulsar-gentest_multiple_partiotions_100b.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml"

