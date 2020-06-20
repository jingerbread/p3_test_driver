#!/usr/bin/env python

from __future__ import print_function
import json
import sys


# Generates 44 tests and takes ~185m (duration: 2min)
def add_test():
    driver = {
        'name': 'Pulsar',
        'driverClass': 'io.openmessaging.benchmark.driver.pulsar.PulsarBenchmarkDriver',
        'client': {
            'serviceUrl': 'pulsar://pulsar-broker.default.svc.cluster.local:6650',
            'httpUrl': 'http://pulsar-broker.default.svc.cluster.local:8080',
            'ioThreads': 8,
            'connectionsPerBroker': 8,
            'clusterName': 'pulsar',
            'namespacePrefix': 'benchmark/ns',
            'topicType': 'persistent',
            'persistence': {
                'ensembleSize': 3,
                'writeQuorum': 3,
                'ackQuorum': 3,
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
        test='openmessaging-benchmark-k8s',
        max_test_attempts=2,
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
image = 'devops-repo.isus.emc.com:8116/maria/omb:dev2.5.2-3a0164c-1'
tarball = '../package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz'
build = False

# Message size 10k 16 partitionsPerTopic 13 tests
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [1e6, 1e3, 5e5, 6e4, 3e3, 5e4, 55e3, 9e3, 4e4, 15e3, 3e4, 25e3, 35e3, 2e4]:
                    for topics in [4]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                            add_test()
'''
# Message size 100 B 16 partitionsPerTopic 9 tests
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [1e6, 1e2, 5e5, 1e3, 6e5, 1e4, 6e4, 5e3, 5e4]:
                    for topics in [4]:
                        for partitionsPerTopic in [16]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                            add_test()

# Message size 10k 1 partitionsPerTopic 13 tests
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [10000]:
                for producerRateEventsPerSec in [1e6, 1e3, 5e5, 6e4, 3e3, 5e4, 55e3, 9e3, 4e4, 15e3, 3e4, 25e3, 35e3, 2e4]:
                    for topics in [4]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                            add_test()

# Message size 100 B 1 partitionsPerTopic 9 tests
for repeat in range(1):
    for producerWorkers in [2]:
        numWorkers = 0 if localWorker else producerWorkers*2
        for testDurationMinutes in [2]:
            for messageSize in [100]:
                for producerRateEventsPerSec in [1e6, 1e2, 5e5, 1e3, 6e5, 1e4, 6e4, 5e3, 5e4]:
                    for topics in [4]:
                        for partitionsPerTopic in [1]:
                            for producersPerWorker in [2]:
                                producersPerTopic = int(producersPerWorker * producerWorkers)
                                for consumerBacklogSizeGB in [0]:
                                    for subscriptionsPerTopic in [1]:
                                        for consumerPerSubscription in [producersPerTopic]:
                                            add_test()

'''

print(json.dumps(test_list, sort_keys=True, indent=4, ensure_ascii=False))
print('Number of tests generated: %d' % len(test_list), file=sys.stderr)
