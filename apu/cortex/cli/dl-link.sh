#!/bin/bash
# https://docs-cortex.paloaltonetworks.com/r/Cortex-XSIAM/Cortex-XSIAM-Premium-Documentation/Connect-Cortex-CLI

# amd64 seems to be all that is supported as of 7/10 and I asked in chat if this is right. This script is successful but, my system is x86.

set -e

# shellcheck disable=SC1090
source ~/.cortexcloud/lab.py
echo "$CORTEX_DOMAIN"

# echo test commands
command -v curl || echo curl not installed
command -v python || echo python not installed

# os=macos
# Mac only works with arm as of 8/11
# cortex_dw=$(curl --fail -s "$CORTEX_DOMAIN/public_api/v1/unified-cli/releases/version/v0.18.0/download-link?os=linux&architecture=amd64" -H "x-xdr-auth-id: ${CORTEX_API_KEY_ID}" -H "Authorization: ${CORTEX_API_KEY}")
echo calling for download link...
cortex_dw=$(curl --fail -s "$CORTEX_DOMAIN/public_api/v1/unified-cli/releases/version/v0.18.0/download-link" -H "x-xdr-auth-id: ${CORTEX_API_KEY_ID}" -H "Authorization: ${CORTEX_API_KEY}")
# cortex_dw=$(curl -s "$CORTEX_DOMAIN/public_api/v1/cli/releases/" -H "x-xdr-auth-id: ${CORTEX_API_KEY_ID}" -H "Authorization: ${CORTEX_API_KEY}")

echo "$cortex_dw"
# read -r wait
parsed=$(echo "$cortex_dw" | python -c 'import json,sys;print(json.load(sys.stdin)["signed_url"])')
echo "$parsed"
curl --fail -o cortexcli "$parsed"
echo after curl

echo cortexcli downloaded..

command -v cortexcli || echo cortexcli not on path

command -v ./cortexcli || echo "cortexcli is likely not executable.. chmod +x cortexcli? $(file ./cortexcli)"

./cortexcli --version
./cortexcli --help
