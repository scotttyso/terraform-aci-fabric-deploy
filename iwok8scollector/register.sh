#!/bin/bash

TOKEN=$(curl -s http://localhost:9110/SecurityTokens | jq '.[].Token')
ID=$(curl -s http://localhost:9110/DeviceIdentifiers | jq '.[].Id')

echo ""
echo ""
echo "Go to on-prem apidocs(https://<on-prem>/apidocs/asset/DeviceClaims/post/)"
echo "and claim the device using the following payload at /api/v1/asset/DeviceClaims:"
echo "{"
echo '"SerialNumber"':"${ID},"
echo '"SecurityToken"':"${TOKEN}"
echo "}"