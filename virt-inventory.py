#!/bin/python

'''
Dynamic inventory via libvirt
'''

import sys
import argparse
import libvirt
import json


addr_source = libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE


def ignore(data, err):
    pass


def query_dom(dom):
    try:
        ifaces = dom.interfaceAddresses(addr_source)
    except Exception:
        return None

    netaddr = None
    # generally we get only one, if more, we pick the last
    for iface in ifaces:
        for addr in ifaces[iface]['addrs']:
            if addr['type'] == 0:
                netaddr = addr['addr']

    return netaddr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action = 'store_true')
    parser.add_argument('--host', action = 'store')
    args = parser.parse_args()

    libvirt.registerErrorHandler(f=ignore, ctx=None)

    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to connect to hypervisor')
        sys.exit(1)

    if args.list:
        hosts = []
        hostvars = {}
        doms = conn.listAllDomains()
        for dom in doms:
            try:
                print dom.metadata(1, None)
            except:
                pass
            if not dom.isActive():
                continue
            hosts.append(dom.name())
            addr = query_dom(dom)
            if addr:
                hostvars[dom.name()] = {'ansible_host': addr}
        if hosts:
            inventory = {'all':{'hosts':hosts}}
            inventory.update({'_meta': {'hostvars': hostvars}})
            print json.dumps(inventory);

    elif args.host:
        dom = conn.lookupByName(args.host)
        if dom.isActive():
            addr = query_dom(dom)
            if addr:
                print json.dumps({dom.name(): {'ansible_host': addr}})
