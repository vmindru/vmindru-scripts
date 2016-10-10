#!/usr/bin/python

import os
import time 


from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
import novaclient as novdoc
import neutronclient.v2_0 as neudoc

VERSION = 1.0

AUTH_URL = os.environ['OS_AUTH_URL']
USERNAME = os.environ['OS_USERNAME']
PASSWORD = os.environ['OS_PASSWORD']
PROJECT_NAME = os.environ['OS_PROJECT_NAME']


loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=AUTH_URL,
                                username=USERNAME,
                                password=PASSWORD,
                                project_name=PROJECT_NAME)


sess = session.Session(auth=auth)
nova = novaclient.Client(VERSION, session=sess)
neutron = neutronclient.Client(session=sess)

def delete_servers(nova):
    servers = nova.servers.list()
    print "starting instance delete, will delete {} servers".format(len(servers))
    for server in servers:
        nova.servers.delete(server._info['id'])
    while servers != []:
        servers = nova.servers.list()
        print "waiting, pending delete {} servers".format(len(servers))
        time.sleep(2)

def delete_floating_ips(neutron):
    floating_ips = neutron.list_floatingips()['floatingips']
    print "starting floating IP delete, will delete {} ips".format(len(floating_ips))
    for flip in floating_ips:
        flipid = flip['id']
        neutron.delete_floatingip(flipid)
    while floating_ips != []:
        floating_ips = neutron.list_floatingips()['floatingips']
        print "waiting, pending delete {} floatings".format(len(floating_ips))
        time.sleep(2)

def delete_router(neutron):
    routers = neutron.list_routers()['routers']
    print "starting router delete, will delete {} routers".format(len(routers))
    for router in routers:
        rt = router['id']
        print rt
        try:
            neutron.remove_gateway_router(rt)
            ports = neutron.list_ports()['ports']
            for port in ports:
                if port['device_owner'] == "network:router_interface":
                    portid={"port_id": port['id']}
                    neutron.remove_interface_router(rt,body=portid)
            neutron.delete_router(rt)
        except ValueError:
            print "coudl not remote router {}".format(rt)
    while routers != []:
        routers = neutron.list_routers()['routers']
        print "removing routers, {} router left".format(len(routers))
        time.sleep(2) 

def delete_networks(neutron):
    # REQUIRS REMOVE, FIPS , INSTANCE, ROUTERS
    networks = neutron.list_networks()['networks']
    nets = []
    # PREPARE NEW ARRAY OF NETWORKS, need to dif all networks from our personal
    for network in  networks:
        if network['router:external'] == False:
            nets.append(network) 
    print "starting net delete, will delete {} networks".format(len(nets))
    while nets != []:
        print "waiting, pending delete {} nets".format(len(nets))
        for net in nets:
            neutron.delete_network(net['id'])
            nets.remove(net)
        time.sleep(2) 

def delete_security_groups(neutron):
    security_groups = neutron.list_security_groups()['security_groups']
    print "starting security group delete, will delete {} security groups".format(len(security_groups))
    for sc in security_groups:
    # there is always a default security group, we don't want to delet that one
        if sc['name'] != "default":
            neutron.delete_security_group(sc['id'])
    # there is always a default security group, we don't want to delet that one
    while len(security_groups) != 1:
        security_groups = neutron.list_security_groups()['security_groups']
        print "waiting, pending delete {} security_groups".format(len(security_groups))
        time.sleep(2)

def delete_keypair(nova):
    keypairs = nova.keypairs.list() 
    print "starting keypairs delete, will delete {} keypairs".format(len(keypairs))
    for keypair in keypairs:
        keypair_name = keypair._info['keypair']['name']
        nova.keypairs.delete(keypair_name) 
    keypairs = nova.keypairs.list() 
    while len(keypairs) != 0:
        time.sleep(2)
        print "waiting, pending delete {} keypairs".format(len(security_groups))
        keypairs = nova.keypairs.list() 


delete_servers(nova)
delete_floating_ips(neutron)
delete_router(neutron)
delete_networks(neutron)
delete_security_groups(neutron)
delete_keypair(nova)




