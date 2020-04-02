#!/usr/bin/env sh

ssh-keygen -t rsa -b 2048 -f ./ssh/aws.pem -q -P ''
ssh-keygen -y -f ./ssh/aws.pem > ./ssh/aws.pub
chmod 400 ./ssh/aws.pem
chmod 400 ./ssh/aws.pub