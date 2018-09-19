set xlabel "time [s]"
set ylabel "Throughput [Mbps]"
set key bel
plot  "tcp1.tr" u ($1):($2) t "TCP1" w lp linecolor 3, "tcp2.tr" u ($1):($2) t "TCP2" w lp linecolor 1
pause -1