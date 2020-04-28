***********************************************
Setup p3_test_driver on jump-host (rhel7.4)
***********************************************
 Deploy Pulsar on AWS according instruction in open-messaging benchmark driver-pulsar/README.md
 Clone p3_test_driver project inside benchmark project
 tesgen_pulsar_ssh.py path to benchmark artifact:
 tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'

.. parsed-literal::
    cd /home/aws/fork-benchmark
    # Todo: refer to original project if is PR merged:
    # git clone https://github.com/pravega/p3_test_driver
    git clone -b latest_master https://github.com/jingerbread/p3_test_driver.git fork_p3_test_driver
    # git clone -b low_cpu https://github.com/jingerbread/p3_test_driver.git fork_p3_test_driver
    # git clone -b UDSPERF-464_run_pulsar_aws_test https://github.com/jingerbread/p3_test_driver.git fork_p3_test_driver
    cd fork_p3_test_driver/
    time ./scripts/setup_p3_test_driver_on_jumphost.sh && pip3.7 install wheel

********************************************
Developer Installation
********************************************
Before running tests, run following command,
it will automate Developer installation of p3_test_driver.

.. parsed-literal::
   time ./scripts/update_local_package_from_src.sh

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

Install virtualenv
https://blog.teststation.org/centos/python/2016/05/11/installing-python-virtualenv-centos-7/

.. parsed-literal::
    yum install epel-release
    yes | yum install python34 python-pip
    pip3.7 install -U pip
    pip3.7 install -U virtualenv

Deploy Pulsar on AWS according instruction in open-messaging benchmark driver-pulsar/README.md
Clone inside benchmark project

.. parsed-literal::
    cd /home/aws/fork-benchmark
    # todo refer to original project if is PR merged:
    # git clone https://github.com/pravega/p3_test_driver
    git clone -b UDSPERF-464_run_pulsar_aws_test https://github.com/jingerbread/p3_test_driver.git

Because project code refer to benchmark project driver-pulsar files

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
    # pip3.7 --no-cache-dir -v install p3_test_driver
    # Install latest package from https://pypi.org/simple/p3-test-driver/
    pip3.7 -v --upgrade p3_test_driver

Run test

.. parsed-literal::
     tests/perf-pulsar-tests/pulsar-gentest_multiple_partiotions_100b.py -vv | p3_test_driver -t - -c config/pulsar_ssh.config.yaml

Uninstall p3_test_driver

.. parsed-literal::
    pip3.7 uninstall p3_test_driver

Exit the virtualenv

.. parsed-literal::
     deactive

**********************
Developer Installation
**********************

Use `script to build/install local p3_driver_package from src <https://github.com/jingerbread/p3_test_driver/blob/UDSPERF-464_run_pulsar_aws_test/scripts/update_local_package_from_src.sh>`__ before running tests

Those that wish to modify P3 Test Driver should use the following steps to install
an editable version and then upload to PyPI.

.. parsed-literal::
    # from project root:
    cd p3_test_driver
    yes | pip3.7 -v uninstall p3_test_driver
    #  -e, --editable <path/url>
    # Install a project in editable mode
    pip3.7 install -e p3_test_driver

    # Twine is a utility for publishing Python packages on PyPI
    pip3.7 install twine

    # Make sure you have the latest versions of setuptools and wheel installed:
    python3.7 -m pip3.7 install --user --upgrade setuptools wheel

    # Generating distribution archives
    cd p3_test_driver && python setup.py sdist bdist_wheel
    # The tar.gz file is a source archive
    # whereas the .whl file is a built distribution.
    ls dist/
    p3_test_driver-2.0.3-py3-none-any.whl  p3_test_driver-2.0.3.tar.gz

    #  Uninstall previous and install new package from dist
    cd .. && yes | pip3.7 -v uninstall p3_test_driver
    pip3.7 -v install p3_test_driver/dist/p3_test_driver-2.0.3-py3-none-any.whl

Upload your package to the Python Package Index
.. parsed-literal::
    twine upload dist/*

.. parsed-literal::
    pip3.7 install -e p3_data
    pip3.7 install twine
    cd p3_data
    python setup.py sdist bdist_wheel
    twine upload dist/*

.. parsed-literal::
    grep -A14 "Benchmark - Workloads" data/logs/p3_test_driver.log  > data/workloads.json
    --
    2020-03-27 18:02:09,968 [MainThread  ] [INFO ] 18:02:11.930 [main] INFO io.openmessaging.benchmark.Benchmark - Workloads: {
    2020-03-27 18:02:09,969 [MainThread  ] [INFO ]   "workload-4fb9b75b-384c-4849-b2f1-1107041e8449" : {
    2020-03-27 18:02:09,970 [MainThread  ] [INFO ]     "name" : "4fb9b75b-384c-4849-b2f1-1107041e8449",
    2020-03-27 18:02:09,971 [MainThread  ] [INFO ]     "topics" : 1,
    2020-03-27 18:02:09,972 [MainThread  ] [INFO ]     "partitionsPerTopic" : 16,
    2020-03-27 18:02:09,973 [MainThread  ] [INFO ]     "keyDistributor" : "NO_KEY",
    2020-03-27 18:02:09,974 [MainThread  ] [INFO ]     "messageSize" : 10000,
    2020-03-27 18:02:09,974 [MainThread  ] [INFO ]     "payloadFile" : "/tmp/payload-4fb9b75b-384c-4849-b2f1-1107041e8449.data",
    2020-03-27 18:02:09,974 [MainThread  ] [INFO ]     "subscriptionsPerTopic" : 1,
    2020-03-27 18:02:09,975 [MainThread  ] [INFO ]     "producersPerTopic" : 4,
    2020-03-27 18:02:09,975 [MainThread  ] [INFO ]     "consumerPerSubscription" : 16,
    2020-03-27 18:02:09,976 [MainThread  ] [INFO ]     "producerRate" : -1,
    2020-03-27 18:02:09,976 [MainThread  ] [INFO ]     "consumerBacklogSizeGB" : 0,
    2020-03-27 18:02:09,976 [MainThread  ] [INFO ]     "testDurationMinutes" : 5
    2020-03-27 18:02:09,977 [MainThread  ] [INFO ]   }


Run Jupyter for Analysis of Results
-----------------------------------

.. parsed-literal::
    docker run -d -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work \
        --name jupyter jupyter/scipy-notebook:1386e2046833
    docker logs jupyter

.. parsed-literal::
 # If you need to run on Windows:
 # C:\someFolder:
    - data (folder with experiment results)
    - fork-p3_test_driver (p3_test_driver project)
 # Docker Desktop > Settings > Ensure you have shared the drive in settings
 # Run from administrator console:
 docker run --user root -d -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v  C:\someFolder:/home/jovyan/work --name jupyter jupyter/scipy-notebook:1386e2046833
 # containerId
 docker logs jupyter
 # To access the notebook, open this file in a browser:
 #       file:///home/jovyan/.local/share/jupyter/runtime/nbserver-17-open.html
 #   Or copy and paste one of these URLs:
 #       http://2dfb7f3d53a5:8888/?token=3d0297ad7e8dac33438a8ef0e2195170826b28bdbaf38fa5
 #   or http://127.0.0.1:8888/?token=3d0297ad7e8dac33438a8ef0e2195170826b28bdbaf38fa5

Open Notebook results-analyzer/results-analyzer-pravega.ipynb and run all cells.

 Before running new jupyter container stop and remove previous:
.. parsed-literal::
 docker ps
 docker stop containerId
 docker rm containerId