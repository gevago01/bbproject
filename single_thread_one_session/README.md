# bbproject

## First Benchmark - Requesting same chunk 64x64x64 repeatedly

100 Mesaurements were taken on each of the following dates/times:
+ 2020-02-11 10:46:12.455772
+ 2020-02-11 13:56:29.498024
+ 2020-02-11 17:13:18.372585
+ 2020-02-11 20:23:35.604235
+ 2020-02-11 20:57:48.314422
+ 2020-02-12 00:08:05.546106
+ 2020-02-12 03:18:22.451586
+ 2020-02-12 06:28:39.448217
+ 2020-02-12 09:38:56.486058
+ 2020-02-12 12:49:13.273884

The plot was created using plots.py, which calculates the mean and the error over all mesaurements. The plot is saved in the plots directory

## Second Benchmark - Requesting random 64x64x64 chunks

100 Random objects requested on each of the following dates/times:

+ 2020-02-11 10:51:15.272021
+ 2020-02-11 14:01:32.190817
+ 2020-02-11 17:18:21.251947
+ 2020-02-11 20:28:38.522815
+ 2020-02-11 21:02:51.223404
+ 2020-02-12 00:13:08.336647
+ 2020-02-12 03:23:25.095115
+ 2020-02-12 06:33:42.239486
+ 2020-02-12 09:43:59.324827
+ 2020-02-12 12:54:16.304179


The mean and the error are calculated over all mesaurements (see [plots.py](https://github.com/gevago01/bbproject/blob/master/plots.py)) 

## Third Benchmark - Requesting partial plane

In this benchmark we fix the x coordinate and iterate Y and Z to 1/4th of the full volume's range
 
Partial Planes requested:

+ 20um/0-64_6208-6272_1664-1728
+ 20um/0-64_5696-5760_5632-5696
+ 20um/0-64_2496-2560_5376-5440
+ 20um/0-64_2816-2880_5440-5504
+ 20um/0-64_6400-6464_832-896
+ 20um/0-64_4992-5056_832-896
+ 20um/0-64_320-384_1472-1536
+ 20um/0-64_3456-3520_1856-1920
+ 20um/0-64_5184-5248_4736-4800
+ 20um/0-64_5440-5504_4032-4096
+ 20um/0-64_5440-5504_3200-3264
+ 20um/0-64_3008-3072_1472-1536

on the corresponding following dates/times:

+ 2020-02-11 10:56:26.873728
+ 2020-02-11 14:06:43.718411
+ 2020-02-11 17:23:32.893062
+ 2020-02-11 20:33:50.275848
+ 2020-02-11 21:08:02.893070
+ 2020-02-12 00:18:19.846912
+ 2020-02-12 03:28:36.821028
+ 2020-02-12 06:38:53.954710
+ 2020-02-12 09:49:10.656442
+ 2020-02-12 12:59:29.003161

