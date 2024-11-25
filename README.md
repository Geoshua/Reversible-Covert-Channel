# About
This is a Bachelor Thesis project completed under the supervision of Professor ![Jurgen Sch&ouml;nw&auml;lder](https://www.beadg.de/js/) during Spring 2024 at ![Jacobs/Constructor University](https://constructor.university/).


The code used for the experiments are included in this Repository. The thesis itself is not included but the Presentation and Abstract is available for reading at the bottom.

# Included code
All programs were written in Python.

### compressor.py
A .pcap compressor that was used to compress incoming packets for earlier experiments, uses various compression libraries.

### scapy-interceptor-recv.py and scapy-interceptor-send.py 
The implementation of the TLS record editor that was used for the covert sender and covert receiver nodes. Uses the Python Scapy library.

### finaltopo.py and https.py
The implementation of the mininet topology used to imitate client and server packet transfers, https.py is the implementation of the https server that allows for testing with TLS protocol. Uses the Python mininet library. 

See below for more clarity on the topology structure.

![mininettopo](https://github.com/user-attachments/assets/1bc7600d-c2a5-4155-a8d4-aa3279393c0d)

# Abstract
This thesis presents the design and implementation of a reversible covert channel over
Transport Layer Security (TLS), exploring a novel and effective method for covert com-
munication within encrypted network traffic. Utilizing a controlled Mininet simulation,
the experiment involves a client node and a server node, with two intermediary router
nodes intercepting and modifying packet bytes to facilitate covert data exchange. The
router nodes effectively conceal communication within legitimate TLS traffic, ensuring
undetected information transmission. The paper takes two approaches to the problem,
compressing encrypted packets and directly modifying a TLS packet. The successful
implementation demonstrates the feasibility of the reversible covert channel, highlight-
ing its potential implications for network security and the challenges it poses to conven-
tional detection mechanisms. This research fills a gap in the understanding of covert
channels within secure communication protocols, offering valuable insights into defen-
sive strategies against advanced persistent threats and sophisticated cyber attacks. The
findings underscore the need for enhanced detection and mitigation techniques to safe-
guard against emerging covert communication methods.
