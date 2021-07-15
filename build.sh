#!/bin/sh

podman build -t danielkucera/sip-docker .
podman push danielkucera/sip-docker

