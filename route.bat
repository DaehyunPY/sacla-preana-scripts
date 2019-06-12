REM run with sudo
REM set daquser=172.30.121.254
set daquser=172.30.103.254
REM set daquser=172.30.39.254  REM SACLA BL3

route add %daquser% mask 255.255.254.0 %daquser% metrix 100
route add 10.12.100.0 mask 255.255.254.0 %daquser% metric 100
route add 172.30.120.0 mask 255.255.254.0 %daquser% metric 100
route add 172.28.8.0 mask 255.255.254.0 %daquser% metric 100
pause
