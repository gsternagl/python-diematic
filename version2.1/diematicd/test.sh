#!/bin/sh

while true
do
	curl http://192.168.178.190:5000/registers
	sleep 1
	echo
	echo "next one"
done
