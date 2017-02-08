#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pyVmomi import vim


def create_vswitch(name, host, num_ports=1024):
    """
    Creates a vSwitch
    :param name: Name of the vSwitch to create
    :param host: vim.HostSystem to create the vSwitch on
    :param num_ports: Number of ports the vSwitch should have [default: 1024]
    """
    logging.info("Creating vSwitch {} with {} ports on host {}".format(name, str(num_ports), host.name))
    vswitch_spec = vim.host.VirtualSwitch.Specification()
    vswitch_spec.numPorts = num_ports
    host.configManager.networkSystem.AddVirtualSwitch(name, vswitch_spec)

# TODO: edit vswitch


def delete_vswitch(name, host):
    """
    Deletes the named vSwitch from the host
    :param name: Name of the vSwitch to delete
    :param host: vim.HostSystem to delete vSwitch from
    """
    logging.info("Deleting vSwitch {} from host {}".format(name, host.name))
    host.configManager.networkSystem.RemoveVirtualSwitch(name)


def create_portgroup(name, host, vswitch_name, vlan=0, promiscuous=False):
    """
    Creates a portgroup
    :param name: Name of portgroup to create
    :param host: vim.HostSystem on which to create the port group
    :param vswitch_name: Name of vSwitch on which to create the port group
    :param vlan: (Optional) VLAN ID of the port group [default: 0]
    :param promiscuous: (Optional) Sets the promiscuous mode of the switch, allowing for monitoring [default: False]
    """
    logging.info("Creating PortGroup {} on vSwitch {} on host {}".format(name, vswitch_name, host.name))
    logging.info("VLAN ID: {} \t Promiscuous: {}".format(str(vlan), str(promiscuous)))
    spec = vim.host.PortGroup.Specification()
    spec.name = name
    spec.vlanId = int(vlan)
    spec.vswitchName = vswitch_name
    policy = vim.host.NetworkPolicy()
    policy.security = vim.host.NetworkPolicy.SecurityPolicy()
    policy.security.allowPromiscuous = promiscuous
    policy.security.macChanges = False
    policy.security.forgedTransmits = False
    spec.policy = policy

    host.configManager.networkSystem.AddPortGroup(spec)


def delete_portgroup(name, host):
    """
    Deletes a portgroup
    :param name: Name of the portgroup
    :param host: vim.HostSystem with the portgroup
    """
    logging.info("Deleting PortGroup {} from host {}".format(name, host.name))
    host.configManager.networkSystem.RemovePortGroup(name)
