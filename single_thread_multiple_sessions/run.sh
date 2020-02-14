for i in `seq 1 10`
do
 python partialPlane.py  
 sleep 10m
 python randomChunks.py  
 sleep 10m
 python sameChunk.py
 sleep 3h
done
exit
