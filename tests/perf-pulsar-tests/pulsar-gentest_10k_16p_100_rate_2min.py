#!/usr/bin/env python

from __future__ import print_function
import json
import sys

test_list = []

localWorker = False
tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
build = False

# Run 10kb 100 rate 16 partitions 2min
# "workload": {
#     "consumerBacklogSizeGB": 0,
#     "consumerPerSubscription": 16,
#     "keyDistributor": "NO_KEY",
#     "messageSize": 10000,
#     "partitionsPerTopic": 16,
#     "producerRate": 100.0,
#     "producersPerTopic": 4,
#     "subscriptionsPerTopic": 1,
#     "testDurationMinutes": 5,
#     "topics": 1
# }
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:    #   , 10000]:
                messageSize = int(messageSize)
                eps = []
                MBps = []
                ppw = []
                if messageSize <= 100:
                    eps = [5e4]     # producerRateEventsPerSec
                    ppw = [1]   # producersPerWorker
                elif messageSize <= 10000:
                    eps += [100]    # [3e1, 1e2, 3e2, 1e3, 3e3, 1e4, 3e4, -1]
                    ppw = [1]   # [2] # producersPerWorker
                else:
                    eps += [1]  # , 3, 10, 30, 50, 70, 90, -1]
                    ppw = [4]
                eps += [x * 1e6 / messageSize for x in MBps]
                for producerRateEventsPerSec in eps:
                    for topics in [1]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in ppw:
                                producersPerTopic = 4   # int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [partitionsPerTopic]:
                                            for ackQuorum in [2]:   # 2 causes OOM in Bookie at max rate
                                                driver = {
                                                    'name': 'Pulsar',
                                                    'driverClass': 'io.openmessaging.benchmark.driver.pulsar.PulsarBenchmarkDriver',
                                                    'client': {
                                                        'ioThreads': 8,
                                                        'connectionsPerBroker': 8,
                                                        'clusterName': 'local',
                                                        'namespacePrefix': 'benchmark/ns',
                                                        'topicType': 'persistent',
                                                        'persistence': {'ensembleSize': 3,
                                                                        'writeQuorum': 3,
                                                                        'ackQuorum': ackQuorum,
                                                                        'deduplicationEnabled': True},
                                                        'tlsAllowInsecureConnection': False,
                                                        'tlsEnableHostnameVerification': False,
                                                        'tlsTrustCertsFilePath': None,
                                                        'authentication': {'plugin': None, 'data': None}},
                                                    'producer': {'batchingEnabled': True,
                                                                 'batchingMaxPublishDelayMs': 1,
                                                                 'blockIfQueueFull': True,
                                                                 'pendingQueueSize': 10000},
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
                                                    # result_filename_long='data/results/json/%(test)s__%(messageSize)d__%(partitionsPerTopic)d__%(producerRateEventsPerSec)__%(testDurationMinutes)d__%(test_uuid)s.json',
                                                    # result_filename_long='data/results/json/%(test)s__%(workload)s__%(test_uuid)s.json',
                                                    # result_filename_long_s='data/results/json/%(test)s__%(workload["messageSize"])s__%(test_uuid)s.json',
                                                    # result_filename_long_d='data/results/json/%(test)s__%(workload["messageSize"])d__%(test_uuid)s.json',
                                                    result_filename='data/results/json/%(test)s_%(test_uuid)s.json',
                                                    driver=driver,
                                                    workload=workload,
                                                    numWorkers=numWorkers,
                                                    localWorker=localWorker,
                                                    tarball=tarball,
                                                    build=build,
                                                    undeploy=True,
                                                )
                                                test_list += [t]
                                                build = False


print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)
