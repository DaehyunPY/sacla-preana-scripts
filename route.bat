:: run with sudo
set eduroam=192.168.0.1
:: change gateway ip!
:: set daquser=172.30.121.254
:: set daquser=172.30.39.254
set daquser=172.30.103.254

route delete 0.0.0.0
route add 0.0.0.0 mask 0.0.0.0 %eduroam% metric 20
route add %daquser% mask 255.255.254.0 %daquser% metrix 10
route add 10.12.100.0 mask 255.255.254.0 %daquser% metric 10
route add 172.30.120.0 mask 255.255.254.0 %daquser% metric 10
route add 172.28.8.0 mask 255.255.254.0 %daquser% metric 10
pause
