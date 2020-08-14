#!/usr/bin/python3

import os
import sys
import re
import struct
import datetime
from socket import inet_aton
import argparse
from ipaddress import IPv4Address, summarize_address_range, IPv4Network, ip_network

#Validation for correct IP evaluation
def validateIP(ip):
    ValidIpAddressRegex = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])|(.{2}[0-9])?$")
    if ValidIpAddressRegex.match(ip):
        return True
    else:
        return False

def getmodel(elem):

    if "/" in elem:
        return "cidr"
    elif "-" in elem:
        return "netmask"
    elif validateIP(elem):
        return "ip"
    else:
        return "unknown"

#If , or space or - in line remove and set IP on newline
def evaluateBadStrings(line):
    if "-" or "," in line:
        stripper=[x for x in re.split(r",| ",line) if x != '']
        for elem in stripper:
            return stripper
    else:
        return line

#if cidr return list of unpacked ip
def iscidr(net):
    try:
        ranger = ip_network(net)
        for ip in ranger:
            yield ip
    except ValueError:
        for ip in list(ip_network(net, False).hosts()):
            yield ip

def getcidrfromblock(net):
    block=net.split("-")
    print(block)
    cidr=summarize_address_range(IPv4Address(block[0]),IPv4Address(block[1]))
    return cidr

#Sort ip address from 1.1.1.1 to 255.255.255.255
def sort_ip_list(ip_list):
    return sorted(ip_list, key=lambda ip: struct.unpack("!L", inet_aton(str(ip)))[0])

def ip_in_prefix(ip_address, prefix):
    #CIDR based separation of address and network size

    [prefix_address, net_size] = prefix.split("/")
    #Convert string to int
    net_size = int(net_size)
    #Get the network ID of both prefix and ip based net size
    prefix_network = get_addr_network(prefix_address, net_size)
    ip_network = get_addr_network(ip_address, net_size)

    return ip_network == prefix_network

def sortcidr(input,separator,char):

    netmasks = []
    badblocks = []
    newcidr = set()
    singleIp = []
    ranges = []
    ipoverlapping = []

    try:
        for cidr in input :
            eval = cidr.strip()
            if "-" in eval :
                ipblock = eval.split("-")
                if len(ipblock) > 2:
                    logger.warning("The following blocks {} are badly formatted and requires manual intervetions".format(eval))
                    badblocks.append(ipblock)
                else:
                    ranges.append(eval)
                    for range in summarize_address_range(IPv4Address(ipblock[0]),IPv4Address(ipblock[1])):
                        newcidr.add(IPv4Network(range))
            elif '/' in eval:
                newcidr.add(IPv4Network(eval))

            else:
                if validateIP(eval):
                    singleIp.append(eval)
    except ipaddress.AddressValueError:
        logger.warning("The following blocks {} are badly formatted and requires manual intervetions".format(eval))


    logging.info("Single IPs identified in file: {}".format(len(singleIp)))
    logging.info("Single IPs duplicates identified {}".format(len(singleIp)-len(set(singleIp))))
    logging.info("IPs removed from list of CIDRs {}".format(len(set(singleIp))))
    logging.info("CIDR identified in file: {}".format(len(newcidr)))
    logging.info("Ranges identified in file: {}".format(len(ranges)))
    logging.info("Bad formatted blocks identified in file: {}".format(len(badblocks)))
    logging.info("Cleaning, sorting, removing duplicates ip and ip overlapping network from cidrs in progress...")

    for ip in set(singleIp):
        for cidr in newcidr:
            if ip_in_prefix(str(ip),str(cidr)):
                ipoverlapping.append(ip)
                singleIp.remove(ip)

    return sorted(newcidr)

    #with open(output,"a") as writefile:
    #    for cidrs in sorted(newcidr):
    #        writefile.write("{}\n".format(cidrs))
    #    for ips in sort_ip_list(set(singleIp)):
    #        writefile.write(("{}\n".format(ips)))

    #return len(ipoverlapping),len(newcidr),len(set(singleIp))





