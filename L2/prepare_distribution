#!/bin/sh
mkdir -p /tmp/db/SSDD-GameroMillanRodriguez
cp icegauntlet.ice /tmp/db/SSDD-GameroMillanRodriguez
cp auth_server /tmp/db/SSDD-GameroMillanRodriguez
cp Server.py /tmp/db/SSDD-GameroMillanRodriguez
mkdir -p /tmp/db/registry
mkdir -p /tmp/db/node1
mkdir -p /tmp/db/node2
echo "execute icepatch..."
icepatch2calc /tmp/db/SSDD-GameroMillanRodriguez
echo "execute icegrid nodes..."
icegridnode --Ice.Config=node1.config & icegridnode --Ice.Config=node2.config

