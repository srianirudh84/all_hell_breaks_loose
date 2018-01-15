1) This is a network scanning tool , that scans IP addresses or network as a whole

2) This tool assumes you have the libnmap python module installed. If not get it from the following link:
   https://pypi.python.org/pypi/python-libnmap

   or

   pip install python-libnmap

2) Required 2 arguments:
	
	-- Network or subnet like 192.168.0.0/24 or Just IP addresses like 10.1.2.50
	-- Customized timeframe in seconds

3) Since NMAP required root access, it is inbuilt within this script. So you are required to type password if you are running this as non root user.

4) Command help:
	
	anirudh-MacBook-Pro:~ anirudh$ python netscan.py --help
    Usage: netscan.py [options]

    Options:
      -h, --help            show this help message and exit
      -n MY_NETWORK, --network=MY_NETWORK
                        Please type atleast one subnet of the type x.x.x.x/x
      -t CUSTOM_TIME, --time=CUSTOM_TIME
                        custom time in sec

5) Sample run:
	
	anirudh-MacBook-Pro:~ anirudh$ python netscan.py -n 192.168.0.0/24 -t 2
	Password:

	IP Address: 192.168.0.1
	OS Type: Motorola SURFboard 5101 cable modem
	Last seen timestamp: Sat Nov  4 12:59:25 2017

	IP Address: 192.168.0.10
	OS Type: Linux 2.6.9 - 2.6.33
	Last seen timestamp: Sat Nov  4 13:04:08 2017

	IP Address: 192.168.0.15
	OS Type: Linux 2.6.17 - 2.6.36
	Last seen timestamp: Tue Jan  9 17:44:17 2018

	IP Address: 192.168.0.16
	OS Type: Linux 2.6.32 - 3.10
	Last seen timestamp: Tue Jan  9 17:50:40 2018

	IP Address: 192.168.0.17
	OS Type: Apple Mac OS X 10.7.0 (Lion) - 10.12 (Sierra) or iOS 4.1 - 9.3.3 (Darwin 10.0.0 - 16.1.0)
	Last seen timestamp: Mon Jan  1 21:53:45 2018


