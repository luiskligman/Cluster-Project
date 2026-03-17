wakeonlan -i 10.0.1.255 -p 9 08:92:04:eb:31:fe  # head
sleep 10
wakeonlan -i 10.0.1.255 -p 9 90:b1:1c:71:9a:9a  # worker 1
sleep 10
wakeonlan -i 10.0.1.255 -p 9 90:b1:1c:71:95:b8  # worker 2
sleep 10
wakeonlan -i 10.0.1.255 -p 9 90:b1:1c:71:a4:b9  # worker 3
sleep 10
wakeonlan -i 10.0.1.255 -p 9 90:b1:1c:71:93:64  # worker 4
