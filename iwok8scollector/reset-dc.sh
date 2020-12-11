#!/bin/bash

echo $0 $1
if [ ! $1 ]; then
    echo "Usage: $0 <on-prem full DNS name>"
    echo "      For example $0 ccp-intersight-241.cisco.com"
    exit;
fi

DC=$1
mkdir -p tmp
echo | openssl s_client -connect  $DC:443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > tmp/cert.pem
sleep 1
curl -X POST --data-binary @./tmp/cert.pem localhost:9110/ManageCertificates
sleep 1
curl -X PUT -d '{"CloudDns":"'$DC'", "ForceResetIdentity": true }' 127.0.0.1:9110/DeviceConnections
sleep 1