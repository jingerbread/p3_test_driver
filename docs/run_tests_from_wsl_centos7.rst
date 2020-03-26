***********************************************
Run p3_test_driver from WSL CentOS7 for Pulsar
***********************************************
Pre-requirements:
* Install python >= 3.7
Check https://www.python.org/ftp/python/

.. parsed-literal::
    yes | yum install gcc openssl-devel bzip2-devel libffi libffi-devel

    cd /home/aws/tools
    wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
    tar xzf Python-3.7.7.tgz
    cd Python-3.7.7

    # takes more than 10 min
    ./configure --enable-optimizations
    # 13:08 - 13:21 (13 min)
    make altinstall
    # Check
    python3.7 -V

*  Install virtualenv
https://blog.teststation.org/centos/python/2016/05/11/installing-python-virtualenv-centos-7/
.. parsed-literal::
    yum install epel-release
    yes | yum install python34 python-pip
    pip install -U pip
    pip install -U virtualenv

Deploy Pulsar on AWS according instruction in open-messaging benchmark driver-pulsar/README.md
Clone inside benchmark project
.. parsed-literal::
    cd /home/aws/fork-benchmark
    # todo refer to original project if is PR merged:
    # git clone https://github.com/pravega/p3_test_driver
    git clone -b UDSPERF-464_run_pulsar_aws_test https://github.com/jingerbread/p3_test_driver.git

Because project code refer to benchmark project driver-pulsar files:
.. parsed-literal::
    # tesgen_pulsar_ssh.py path to benchmark artifact:
    tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'

Check config/pulsar_ssh.config.yaml
.. parsed-literal::
    status_html: data/status/pulsar.html
    test_driver_log_filename: data/logs/p3_test_driver.log
    ssh_user: ec2-user
    ssh_identity_file: ~/.ssh/pulsar_aws
    terraform: true
    ansible: true # Requires ../driver-pulsar/deploy/vars.yaml

Create ../driver-pulsar/deploy/vars.yaml
.. parsed-literal::
    ---
    pulsarVersion: "2.4.1"
    zookeeperVersion: "3.5.5"
    bookkeeperVersion: "4.9.2"

Create virtualenv
.. parsed-literal::
    cd p3_test_driver/
    rm -rf venv
    virtualenv -p python3.7 venv
    # created virtual environment CPython3.7.7.final.0-64 in 11044ms

    source venv/bin/activate
    pip install p3_test_driver

Run test
.. parsed-literal::
     tests/perf-pulsar-tests/pulsar-gentest_multiple_partiotions_100b.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml

Exit the virtualenv
.. parsed-literal::
     deactive