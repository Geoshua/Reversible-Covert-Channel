from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.nodelib import LinuxBridge

"""
         10.1.0.0/24   ||      10.3.0.0/24   ||    10.2.0.0/24

   h1.eth0--s1--r1.eth0  r1.eth1--s3--r2.eth0  r2.eth1--s2--h2.eth0

   10.1.0.2    10.1.0.1  10.3.0.1    10.3.0.2   10.2.0.1    10.2.0.2

"""

def run():
     net = Mininet(switch=LinuxBridge, controller=None)

     h1 = net.addHost('h1', ip=None)
     s1 = net.addSwitch('s1')
     r1 = net.addHost('r1', ip=None)
     s3 = net.addSwitch('s3')
     r2 = net.addHost('r2', ip=None)
     s2 = net.addSwitch('s2')
     h2 = net.addHost('h2', ip=None)

     net.addLink(h1, s1)
     net.addLink(r1, s1)
     net.addLink(h2, s2)
     net.addLink(r2, s2)
     net.addLink(r1, s3)
     net.addLink(r2, s3)

     h1.cmd("ip addr add 10.1.0.2/24 dev h1-eth0")
     h1.cmd("ip route add default via 10.1.0.1")

     h2.cmd("ip addr add 10.2.0.2/24 dev h2-eth0")
     h2.cmd("ip route add default via 10.2.0.1")

     r1.cmd("ip addr add 10.1.0.1/24 dev r1-eth0")
     r1.cmd("ip addr add 10.3.0.1/24 dev r1-eth1")
     r1.cmd("ip route add 10.2.0.0/24 via 10.3.0.2")
     r1.cmd("sysctl net.ipv4.ip_forward=1")
     r1.cmd("iptables -I FORWARD -s 10.1.0.0/24 -j NFQUEUE —queue-num 2")

     r2.cmd("ip addr add 10.2.0.1/24 dev r2-eth0")
     r2.cmd("ip addr add 10.3.0.2/24 dev r2-eth1")
     r2.cmd("ip route add 10.1.0.0/24 via 10.3.0.1")
     r2.cmd("sysctl net.ipv4.ip_forward=1")
     r2.cmd("iptables -I FORWARD -s 10.1.0.0/24 -j NFQUEUE —queue-num 2")


     net.start()
     CLI(net)
     net.stop()

if __name__ == '__main__':
     setLogLevel('info')
     run()
