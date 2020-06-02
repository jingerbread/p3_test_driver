#!/usr/bin/env python

from __future__ import print_function
import json
import sys

test_list = []
# Generates 12 test and takes 25 min (duration: 1min)
# batchingEnabled: True

def add_test():
    driver = {
        'name': 'Pravega',
        'driverClass': 'io.openmessaging.benchmark.driver.pravega.PravegaBenchmarkDriver',
        'client': {
            'controllerURI': 'tcp://10.233.66.5:9090',
            'scopeName': 'examples2',
        },
        'writer': {
            'enableConnectionPooling': False,
        },
        'enableTransaction': False,
        'includeTimestampInEvent': includeTimestampInEvent,
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
        test='openmessaging-benchmark',
        max_test_attempts=1,
        driver=driver,
        workload=workload,
        numWorkers=numWorkers,
        localWorker=localWorker,
        tarball=tarball,
        build=build,
        undeploy=True,
    )
    test_list.append(t)

test_list = []

localWorker = True
tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
build = False


# Message size 100 B 1 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [2e4, 3e4, 4e4, 5e4, 6e4, 1e6, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()

# Message size 100 B 16 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [2e4, 3e4, 4e4, 5e4, 6e4, 1e6, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()


# Message size 10k 1 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [2e4, 3e4, 4e4, 5e4, 55e3, 6e4, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()

# Message size 10k 16 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [2e4, 3e4, 4e4, 5e4, 55e3, 6e4, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()

print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of Pulsar 2.5.2 tests generated: %d' % len(test_list), file=sys.stderr)
