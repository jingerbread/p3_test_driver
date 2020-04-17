#!/bin/bash
# [DRAFT] version
# See full instruction in docs/run_tests_from_wsl_centos7.rst
# Script to build/install local p3_driver_package from src
# (checked only for WSL CentOS7)

# Run script from p3_test_driver root dir: (~ 1min)
# time ./scripts/update_local_package_from_src.sh

echo -e "\e[36m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\e[0m"
echo -e "\e[36mRunning script ${0##*/} at $(date)\e[0m"
echo -e "\e[36m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\e[0m"

echo -e "\e[32mSet exit upon error\e[0m"
set -e

git pull

#  -e, --editable <path/url>
# Install a project in editable mode
pip install -e p3_test_driver

# Generating distribution archives
cd p3_test_driver && python3.7 setup.py sdist bdist_wheel
# The tar.gz file is a source archive
# whereas the .whl file is a built distribution.
ls -l dist/

#  Uninstall previous and install new package from dist
cd .. && yes | pip -v uninstall p3_test_driver
# Add -v for verbose
pip  install p3_test_driver/dist/p3_test_driver-2.0.3-py3-none-any.whl

set +x
echo -e "\e[36mSetup finished successfully at $(date)\e[0m"
echo -e "\e[36mRun test with f.e:\e[0m"
echo -e "\e[35m----Pravega tests:----\e[0m"
echo -e "\e[36mtests/testgen_pravega_ssh.py -vv | p3_test_driver -t - -c config/pravega_ssh.config.yaml\e[0m"
echo -e "\e[36mtests/perf-pravega-tests/pravega-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pravega_ssh.config.yaml\e[0m"

echo -e "\e[35m----Pulsar tests:----\e[0m"
echo -e "\e[36mtests/testgen_pulsar_ssh.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m" # Takes ~ >= 90 min
echo -e "\e[36mtests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
echo -e "\e[36mtests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
