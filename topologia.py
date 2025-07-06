#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Host
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
import os
import time

class SimpleTopo(Topo):
    def build(self):
        pc1 = self.addHost('pc1', ip='10.0.0.1/24', mac='00:00:00:00:00:01', hostname="PC-1")
        pc2 = self.addHost('pc2', ip='10.0.0.2/24', mac='00:00:00:00:00:02', hostname="PC-2")
        s1 = self.addSwitch('s1')

        self.addLink(pc1, s1)
        self.addLink(pc2, s1)

def run():

    c1 = RemoteController('c1', ip='127.0.0.1', port=9090)
    os.system("mn -c")
    os.system("pkill -9 simple_switch")
    

    topo = SimpleTopo()
    net = Mininet(topo=topo, controller=None)
    net.start()
    

    switch = net.get('s1')
    json_path = os.path.abspath('basic.json/basic.json')

    switch.cmd(f'simple_switch --log-console --thrift-port 9090 -i 0@{switch.name}-eth1 -i 1@{switch.name}-eth2 {json_path} &')
    
    time.sleep(0.5)

    print("Configuração da tabela P4:")
    pc1 = net.get('pc1')
    pc2 = net.get('pc2')
    os.system(f"echo 'table_add ipv4_lpm ipv4_forward 10.0.0.1/32 => 00:00:00:00:00:01 0' | simple_switch_CLI --thrift-port 9090")
    os.system(f"echo 'table_add ipv4_lpm ipv4_forward 10.0.0.2/32 => 00:00:00:00:00:02 1' | simple_switch_CLI --thrift-port 9090")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

