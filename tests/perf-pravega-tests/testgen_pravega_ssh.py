#!/usr/bin/env python

from __future__ import print_function
import json
import sys

# Generates 33 tests with duration - 1min = 72m total run time
def add_test():
    driver = {
        'name': 'Pravega',
        'driverClass': 'io.openmessaging.benchmark.driver.pravega.PravegaBenchmarkDriver',
        'client': {
            'controllerURI': 'tcp://localhost:9090',
            'scopeName': 'examples',
        },
        'writer': {
            'enableConnectionPooling': False,
            'enableTransaction': False,
            'eventPerTransaction': 1,
        },
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

localWorker = False
tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
build = False

# Message size 100 B
# for repeat in range(1):
#     for producerWorkers in [1]:
#         numWorkers = 0 if localWorker else producerWorkers*2
#         for testDurationMinutes in [1]:
#             for messageSize in [100]:
#                 for producerRateEventsPerSec in [1e5, 2e5, 4e5, -1]:
#                     for topics in [1]:
#                         for partitionsPerTopic in [16]: #[1, 16]:
#                             for producersPerWorker in [1]:
#                                 producersPerTopic = 1   # int(producersPerWorker * producerWorkers)
#                                 for consumerBacklogSizeGB in [0]:
#                                     for subscriptionsPerTopic in [1]:
#                                         for consumerPerSubscription in [partitionsPerTopic]:
#                                             for includeTimestampInEvent in [True]:
#                                                 add_test()

# Message size 10 KB
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [1e5, 2e5, 3e5]: #[2e5, 3e5]: #-1]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]: #[1, 16]:
                            for producersPerWorker in [2]:
                                producersPerTopic = 1   # int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for includeTimestampInEvent in [True]:
                                                add_test()


print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)
