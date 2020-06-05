#!/usr/bin/env python

from __future__ import print_function
import json
import sys


# Generates 28 tests and takes 56 min (duration: 1min)
def add_test():
    driver = {
        'name': 'Pulsar',
        'driverClass': 'io.openmessaging.benchmark.driver.pulsar.PulsarBenchmarkDriver',
        'client': {
            'ioThreads': 8,
            'connectionsPerBroker': 8,
            'clusterName': 'local',
            'namespacePrefix': 'benchmark/ns',
            'topicType': 'persistent',
            'persistence': {
                'ensembleSize': 3,
                'writeQuorum': 3,
                'ackQuorum': 2,
                'deduplicationEnabled': True
            },
            'tlsAllowInsecureConnection': False,
            'tlsEnableHostnameVerification': False,
            'tlsTrustCertsFilePath': None,
            'authentication': {'plugin': None, 'data': None}},
        'producer': {
            'batchingEnabled': True,
            'batchingMaxPublishDelayMs': 1,
            'blockIfQueueFull': True,
            'pendingQueueSize': 10000
        }

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
                for producerRateEventsPerSec in [5e4]:  # [5e4, 6e4, 6e5, 1e6, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                                add_test()
'''
# Message size 100 B 16 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [5e4, 6e4, 6e5, 1e6, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
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
                                                add_test()

# Message size 10k 16 partitionsPerTopic
for repeat in range(1):
    for producerWorkers in [1]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [1]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [5e4, 55e3, 6e4, -1]:
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [1]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            add_test()
'''

print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)
