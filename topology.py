#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    net = Containernet(controller=Controller, link=TCLink, xterms=False)
    mgr = VNFManager(net)

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Creating hosts\n")
    h1 = net.addDockerHost(
        "h1", dimage="complete_client", ip="10.0.0.1", docker_args={"hostname": "h1"}
    )

    h2 = net.addDockerHost(
        "h2", dimage="complete_client", ip="10.0.0.2", docker_args={"hostname": "h2"}
    )

    h3 = net.addDockerHost(
        "h3", dimage="server_streaming", ip="10.0.0.3", docker_args={"hostname": "h3"}
    )

    h4 = net.addDockerHost(
        "h4", dimage="operations_server", ip="10.0.0.4", docker_args={"hostname": "h4"}
    )

    h5 = net.addDockerHost(
        "h5", dimage="echo_server", ip="10.0.0.5", docker_args={"hostname": "h5"}
    )
    

    info("*** Adding switch and links\n")
    switch1 = net.addSwitch("s1")
    switch2 = net.addSwitch("s2")
    net.addLink(switch1, h1, bw=10, delay="10ms")
    net.addLink(switch1, h2, bw=10, delay="10ms")
    net.addLink(switch1, switch2, bw=10, delay="10ms")
    net.addLink(switch2, h3, bw=10, delay="10ms")
    net.addLink(switch2, h4, bw=10, delay="10ms")
    net.addLink(switch2, h5, bw=10, delay="10ms")


    info("\n*** Starting network\n")
    net.start()

    info("*** Adding tcpdump to containers\n")
    # Avvia tcpdump in background su entrambe i container

    srv1 = mgr.addContainer("srv1", "h1", "dev_test", "", docker_args={})
    srv2 = mgr.addContainer("srv2", "h2", "dev_test", "", docker_args={})
    srv3 = mgr.addContainer("srv3", "h3", "server_streaming", "", docker_args={})
    srv4 = mgr.addContainer("srv4", "h4", "dev_test", "", docker_args={})
    srv5 = mgr.addContainer("srv5", "h5", "dev_test", "", docker_args={})
     
    if not AUTOTEST_MODE:
        spawnXtermDocker("srv2")        
        CLI(net)

    # Attendi un po' di tempo per garantire che il traffico avvenga
    mgr.removeContainer("srv1")
    mgr.removeContainer("srv2")
    mgr.removeContainer("srv3")
    mgr.removeContainer("srv4")
    mgr.removeContainer("srv5")
    net.stop()
    mgr.stop()
