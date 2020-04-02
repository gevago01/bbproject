for i in `seq 1 10`
do
 python3 partialPlane.py  
 sleep 30m
 python3 randomChunks.py  
 sleep 30m
 python3 sameChunk.py
 sleep 3h
done
exit
