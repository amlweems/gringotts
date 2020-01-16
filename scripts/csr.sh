#!/bin/bash

# create tmp CA structure
mkdir -p demoCA/newcerts
touch demoCA/index.txt

# create CSR and sign it
openssl req -new -nodes -config /app/templates/server.cnf \
  -newkey rsa:2048 -keyout ssl/server-key.pem -out /tmp/server-req.pem
openssl ca -cert ca/root.pem -keyfile ca/root-key.pem \
  -notext -batch -policy policy_anything -rand_serial \
  -startdate 20180430000000Z -enddate 20200801000000Z \
  -extfile /app/templates/server.cnf -extensions req_ext \
  -in /tmp/server-req.pem -out ssl/server.pem
cat ssl/server.pem ca/root.pem > ssl/server-bundle.pem

# clean up
rm /tmp/server-req.pem
rm -rf demoCA
