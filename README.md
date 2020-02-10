# bbproject

## First Benchmark - Requesting same chunk 64x64x64 repeatedly

100 Mesaurements were taken on each of the following dates/times:
+ 2020-01-30 11:20:34.381382
+ 2020-01-30 13:20:43.193917
+ 2020-01-30 16:44:13.580841
+ 2020-01-30 19:15:35.099461
+ 2020-01-31 10:52:13.023486
+ 2020-01-31 13:28:47.748974
+ 2020-01-31 14:25:52.449957
+ 2020-01-31 15:53:00.896320
+ 2020-02-01 14:28:29.440245
+ 2020-02-02 13:11:52.268082
+ 2020-02-02 17:38:58.963355

The plot was created using plots.py, which calculates the mean and the error over all mesaurements. The plot is saved in the plots directory

## Second Benchmark - Requesting random 64x64x64 chunks

100 Random objects requested on each of the following dates/times:

+ 2020-02-04 11:55:22.752434
+ 2020-02-04 14:02:38.206192
+ 2020-02-04 16:21:24.547007
+ 2020-02-05 14:01:44.874018
+ 2020-02-05 16:01:49.974413
+ 2020-02-05 18:01:55.232591
+ 2020-02-05 20:02:00.443417
+ 2020-02-05 22:02:05.804817
+ 2020-02-06 00:02:11.517283
+ 2020-02-06 02:02:16.854936

The mean and the error are calculated over all mesaurements (see [plots.py](https://github.com/gevago01/bbproject/blob/master/plots.py)) 

## Third Benchmark - Requesting partial plane

In this benchmark we fix the x coordinate and iterate Y and Z to 1/4th of the full volume's range
 
Partial Planes requested:

+ 20um/0-64_3392-3456_448-512
+ 20um/0-64_4736-4800_3328-3392
+ 20um/0-64_6592-6656_3264-3328
+ 20um/0-64_384-448_704-768
+ 20um/0-64_384-448_2496-2560
+ 20um/0-64_1152-1216_2240-2304
+ 20um/0-64_3072-3136_1472-1536
+ 20um/0-64_3648-3712_1408-1472
+ 20um/0-64_4544-4608_4096-4160
+ 20um/0-64_1024-1088_0-64
+ 20um/0-64_3520-3584_5568-5632

on the corresponding following dates/times:

+ 2020-02-06 18:54:12.362544
+ 2020-02-06 20:54:36.081339
+ 2020-02-06 22:54:59.203599
+ 2020-02-07 00:55:21.272413
+ 2020-02-07 02:55:46.131702
+ 2020-02-07 04:56:11.336795
+ 2020-02-07 06:56:34.762248
+ 2020-02-07 11:14:25.359943
+ 2020-02-07 15:14:54.829031
+ 2020-02-07 17:15:18.590824


