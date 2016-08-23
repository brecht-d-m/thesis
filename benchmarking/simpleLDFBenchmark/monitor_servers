#!/bin/bash
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
output_dir="/srv/evaluation_bloom/monitor_$current_time"

mkdir -p $output_dir

sub_pids=()

for pid in "$@"
do
  ./monitor $pid > $output_dir/$pid.csv & sub_pids+=("$(echo $!)")
done

wait $(echo ${sub_pids[@]})

trap "killall ./monitor" EXIT
