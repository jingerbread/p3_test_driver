#!/usr/bin/env python

from __future__ import print_function
import json
import sys


def add_test():
    driver = {
        'name': 'Pravega',
        'driverClass': 'io.openmessaging.benchmark.driver.pravega.PravegaBenchmarkDriver',
        'client': {
            'controllerURI': 'tcp://10.0.0.140:9090',
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


# Message size 100 B 1 segment
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [1e4, 5e4, 3e5, 1e6, -1]: #[1e2, 1e3, 5e3, 1e4, 5e4, 2e5, 3e5, 1e6, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()
# Message size 100 B 16 segments
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [5e3, 5e4, 3e5, 1e6, -1]: # [1e2, 1e3, 5e3, 1e4, 5e4, 2e5, 3e5, 1e6, -1]
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()

# Message size 10 KB 1 segment
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [9e3, 15e3, 25e3, 35e3]: #[1e3, 3e3, 6e3, 9e3, 12e3, 15e3, 20e3, 25e3, 30e3, 35e3]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()

# Message size 10 KB 16 segments
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [5e3, 9e3, 15e3, 25e3]: #[1e3, 3e3, 5e3, 6e3, 9e3, 12e3, 15e3, 20e3, 25e3]:
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
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)