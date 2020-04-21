#!/bin/bash
# [DRAFT] version
# Setup p3_test_driver on jumphost (RHEL7.4):
# See manual instruction
# https://github.com/jingerbread/p3_test_driver/blob/UDSPERF-464_run_pulsar_aws_test/docs/run_tests_from_wsl_centos7.rst

# Run script from p3_test_driver root dir: (~ 4min)
# cd /home/aws/fork-benchmark
# Todo: refer to original project if is PR merged:
# git clone https://github.com/pravega/p3_test_driver
# git clone -b UDSPERF-464_run_pulsar_aws_test https://github.com/jingerbread/p3_test_driver.git fork_p3_test_driver
# cd fork_p3_test_driver/
# time ./scripts/setup_p3_test_driver_on_jump_host.sh

echo -e "\e[36m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\e[0m"
echo -e "\e[36mRunning script ${0##*/} at $(date)\e[0m"
echo -e "\e[36m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\e[0m"

echo -e "\e[32mSet exit upon error mode\e[0m"
set -e

# Install Python 3.7
yes | yum -q install gcc openssl-devel bzip2-devel libffi libffi-devel
cd /home/aws/tools
wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
tar xzf Python-3.7.7.tgz
cd Python-3.7.7
./configure --enable-optimizations
# 3 min
make altinstall
# Check version
python3.7 -V
# Python 3.7.7


# Install virtualenv https://blog.teststation.org/centos/python/2016/05/11/installing-python-virtualenv-centos-7/
yum -y install epel-release
yum -y install python34 python-pip
pip3.7 install -U pip
pip3.7 install -U virtualenv
# Make sure you have the latest versions of setuptools and wheel installed:
python3.7 -m pip3.7 install --user --upgrade setuptools wheel
# Deploy Pulsar on AWS according instruction in open-messaging benchmark driver-pulsar/README.md
# Clone p3_test_driver project inside benchmark project
# tesgen_pulsar_ssh.py path to benchmark artifact:
# tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
# Todo: refer to original project if is PR merged:
# cd /home/aws/fork-benchmark
# git clone https://github.com/pravega/p3_test_driver
# git clone -b UDSPERF-464_run_pulsar_aws_test https://github.com/jingerbread/p3_test_driver.git fork_p3_test_driver
# cd /home/aws/fork-benchmark/fork_p3_test_driver/

## Check config/pulsar_ssh.config.yaml:
#
# status_html: data/status/pulsar.html
# test_driver_log_filename: data/logs/p3_test_driver.log
# ssh_user: ec2-user
# ssh_identity_file: ~/.ssh/pulsar_aws
# terraform: true
# ansible: true # Requires ../driver-pulsar/deploy/vars.yaml
#
# Create ../driver-pulsar/deploy/vars.yaml
#
# ---
# pulsarVersion: "2.4.1"
# zookeeperVersion: "3.5.5"
# bookkeeperVersion: "4.9.2"

## Check config/pravega_ssh_config.yaml
#
# status_html: ../data/p3_test_driver/status/pravega.html
# result_filename: ../data/p3_test_driver/results/%(test)s_%(test_uuid)s.json
# test_driver_log_filename: ../data/p3_test_driver/logs/p3_test_driver.log
# ssh_user: ec2-user
# ssh_identity_file: ~/.ssh/pravega_aws
# kubernetes: false
# docker: false
# aws-ec2: true
# terraform: true
# ansible: true

# Create virtualenv
cd /home/aws/fork-benchmark/fork_p3_test_driver/p3_test_driver
# Remove previous virtualenv
deactivate
rm -rf venv
# Install
virtualenv -p python3.7 venv
# created virtual environment CPython3.7.7.final.0-64 in 904ms
source venv/bin/activate

# Developer installation
yes | pip3.7 -v  uninstall p3_test_driver
#  -e, --editable <path/url>
# Install a project in editable mode
cd ..
pwd
# /home/aws/fork-benchmark/fork_p3_test_driver
pip3.7 install -e p3_test_driver
# Twine is a utility for publishing Python packages on PyPI
yes | pip3.7 -q install twine

yes | pip3.7 -q install wheel

# Generating distribution archives
cd p3_test_driver && python3.7 setup.py sdist bdist_wheel
# The tar.gz file is a source archive
# whereas the .whl file is a built distribution.
ls dist/
# p3_test_driver-2.0.3-py3-none-any.whl  p3_test_driver-2.0.3.tar.gz

#  Uninstall previous and install new package from dist
cd .. && yes | pip3.7 -v uninstall p3_test_driver
pip3.7  install p3_test_driver/dist/p3_test_driver-2.0.3-py3-none-any.whl

echo -e "\e[36mSetup finished successfully at $(date)\e[0m"
echo "\e[36mRun test with f.e:\e[0m"
echo -e "\e[35m----Pravega tests:----\e[0m"
echo -e "\e[36mtests/testgen_pravega_ssh.py -vv | p3_test_driver -t - -c config/pravega_ssh.config.yaml\e[0m"
echo -e "\e[36mtests/perf-pravega-tests/pravega-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pravega_ssh.config.yaml\e[0m"

echo -e "\e[35m----Pulsar tests:----\e[0m"
echo -e "\e[36mtests/testgen_pulsar_ssh.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m" # Takes ~ >= 90 min
echo -e "\e[36mtests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
echo -e "\e[36mtests/perf-pulsar-tests/pulsar-gentest_100b_1p_5e4_rate_2min.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml\e[0m"
