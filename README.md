# bbproject

## Short Description

This repository contains different benchmarks that evaluate the request time of different image chunks from [this Swift store](https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/bigbrain).

Benchmarks implemented:

+ Requesting same chunk 64x64x64 repeatedly. This benchmark requests the same random chunk 100 times. At every benchmark run, the chunk is different. Across different requests of the same benchmark run, the chunk remains the same.
+ Requesting random 64x64x64 chunks. This benchmark requests 100 random chunks and calculate the average request time per chunk.
+ Requesting partial plane. This benchmark defines a plane by fixing the x-coordinate and the the other two dimensions to be 1/4 of the full volume. The bencharm then requests chunks from within the plane.

## Benchmark Execution

The benchmarks are ran using the [run.sh](https://github.com/gevago01/bbproject/blob/master/multiple_threads_one_session/run.sh). All three benchmarks are ran every 3 hours. 

## Execution Environment

We run the benchmarks on the following machine img-svc-bench-01 (148.187.97.94), which is configured with the following specifications:

+ CPU(s):              8
+ Thread(s) per core:  1
+ Core(s) per socket:  1
+ Socket(s):           8
+ Memory:              32 **GB**
+ Disk:                40 **GB**



