#!/bin/bash
# [DRAFT] version
# See full instruction in docs/run_tests_from_wsl_centos7.rst
# Script to build/install local p3_driver_package from src
# (checked only for WSL CentOS7)

# Run script from p3_test_driver root dir: (~ 1min)
# time ./scripts/update_local_package_from_src.sh
scriptName=${0##*/}

echo -e "\e[32mSet debug mode and exit upon error\e[0m"
set -ex

git pull

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

set +x
echo -e "\e[36mUpdate finished successfully\e[0m"
echo "\e[36mRun test with f.e:\e[0m"
echo -e "\e[36tests/testgen_pulsar_ssh.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
echo -e "\e[36tests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
echo- e "\e[36tests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"

