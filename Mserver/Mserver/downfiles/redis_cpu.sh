while [ 1 ]
do
top  -bn2 -d2 -p  $(ps -aux|grep 'redis-server 0.0.0.0:6379'|grep -v grep|awk '{print $2}')|grep redis|awk '{print $9}'|tail -1 >/tmp/redis_cpu.log
sleep 5
done
