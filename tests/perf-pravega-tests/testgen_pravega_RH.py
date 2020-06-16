#!/usr/bin/env python

from __future__ import print_function
import json
import sys


# Generates 44 tests and takes ~185m (duration: 2min)
def add_test():
    driver = {
        'name': 'Pravega',
        'driverClass': 'io.openmessaging.benchmark.driver.pravega.PravegaBenchmarkDriver',
        'client': {
            'controllerURI': 'tcp://pravega-pravega-controller:9090',
            'scopeName': 'examples2',
        },
        'writer': {
            'enableConnectionPooling': False,
        },
        'enableTransaction': False,
        'includeTimestampInEvent': True
    }
    workload = {
        'messageSize': messageSize,
        'topics':  topics,
        'partitionsPerTopic': partitionsPerTopic,
        'subscriptionsPerTopic': subscriptionsPerTopic,
        'consumerPerSubscription': consumerPerSubscription,
        'producersPerTopic': producersPerTopic,
        'producerRate': producerRateEventsPerSec,
        'consumerBacklogSizeGB': consumerBacklogSizeGB,
        'testDurationMinutes': testDurationMinutes,
        'keyDistributor': 'NO_KEY',
    }
    t = dict(
        test='openmessaging-benchmark-k8s',
        max_test_attempts=1,
        driver=driver,
        workload=workload,
        numWorkers=numWorkers,
        localWorker=localWorker,
        tarball=tarball,
        image=image,
        ombHelmPath=ombHelmPath,
        namespace=namespace,
        build=build,
        undeploy=True,
    )
    test_list.append(t)

test_list = []
localWorker = False
namespace = 'default'
ombHelmPath = '../deployment/kubernetes/helm/pulsar-benchmark'
image = 'jingerbread/pulsar-omb:dev2.5.2-d84a68c'
tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
build = False


# Message size 100 B 1 partitionsPerTopic 9 tests
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [5e4]:   # [1e2, 1e3, 5e3, 1e4, 5e4, 6e4, 6e5, 1e6, -1]:
                    for topics in [4]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                                add_test()
'''
# Message size 100 B 16 partitionsPerTopic 9 tests
for repeat in range(1):
    for producerWorkers in [4]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [1e2, 1e3, 5e3, 1e4, 5e4, 6e4, 6e5, 1e6, -1]:
                    for topics in [16]:
                        for partitionsPerTopic in [4]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                                add_test()


# Message size 10k 1 partitionsPerTopic 13 tests
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [1e3, 3e3, 9e3, 15e3, 25e3, 35e3, 2e4, 3e4, 4e4, 5e4, 55e3, 6e4, -1]:
                    for topics in [4]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                                add_test()

# Message size 10k 16 partitionsPerTopic 13 tests
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [1e3, 3e3, 9e3, 15e3, 25e3, 35e3,  2e4, 3e4, 4e4, 5e4, 55e3, 6e4, -1]:
                    for topics in [16]:
                        for partitionsPerTopic in [4]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                            add_test()
'''

print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)
