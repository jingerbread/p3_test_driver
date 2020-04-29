#!/usr/bin/perl

use lib '.';
use HTML::Template;
use File::Slurp;

use strict;
use warnings;

my $dir_jsons = "low-cpu-jsons/100b/";
my $dir_logs  = "low-cpu/100b/";
my $dir_p3    = "p3/low-cpu/100b/"; 

opendir(my $dh, $dir_jsons) || die "Can't open $dir_jsons: $!";
while (my $json_file = readdir $dh) {
    next if  $json_file =~ /^\./;	
    my ($omb_output_file) = $json_file =~ /^(.+?)-Pravega-/;
    $omb_output_file .= '.yaml.log';
    create_json($dir_jsons.$json_file, $dir_logs.$omb_output_file);
}
closedir $dh;

sub create_json {
    my ($json_file, $log_file) = @_;

    my $omb_results = read_file($json_file);
    my ($workload) = $omb_results =~ /"workload" : "(.+?)"/;
    $workload =~ s/\s//g;
    $workload =~ s/\//_/g; 
    my $omb_output = read_file($log_file); 
    my ($name) = $omb_output =~ /"name" : "(.+?)"/;
    my ($topics)  = $omb_output =~ /"topics" \: (\d+)/;
    my ($producerRate) = $omb_output =~ /"producerRate" \: (.+?)/;
    my ($partitionsPerTopic) = $omb_output =~ /"partitionsPerTopic" \: (\d+)/;
    my ($producersPerTopic) = $omb_output =~ /"producersPerTopic" \: (\d+)/;
    my ($consumerPerSubscription) = $omb_output =~ /"consumerPerSubscription" \: (\d+)/;
    my ($subscriptionsPerTopic) = $omb_output =~ /"subscriptionsPerTopic" \: (\d+)/;
    my ($messageSize) = $omb_output =~ /"messageSize" \: (\d+)/;
    my ($testDurationMinutes) = $omb_output =~ /"testDurationMinutes" \: (\d+)/;

    $omb_output =~ s/\n/\\n/sg;
    $omb_output =~ s/"/\\"/sg;

    my $template = HTML::Template->new(filename => 'testframe.json.tmpl');
    $template->param(OMB_RESULTS => $omb_results);
    $template->param(OMB_OUTPUT  => $omb_output);
    $template->param(TEST_UUID   => $workload);
    $template->param(name   => $name);
    $template->param(topics   => $topics);
    $template->param(producerRate   => $producerRate);
    $template->param(partitionsPerTopic   => $partitionsPerTopic);
    $template->param(producersPerTopic   => $producersPerTopic);
    $template->param(consumerPerSubscription   => $consumerPerSubscription);
    $template->param(subscriptionsPerTopic   => $subscriptionsPerTopic);
    $template->param(messageSize   => $messageSize);
    $template->param(messageSize   => $messageSize);
    $template->param(testDurationMinutes => $testDurationMinutes);

    write_file("${dir_p3}openmessaging-benchmark_test$workload.json", $template->output);
}
