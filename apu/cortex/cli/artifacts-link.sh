#!/bin/bash

set -e

# shellcheck disable=SC1090
source ~/.cortexcloud/lab.py

curl -v --fail -k -u "$CORTEX_API_ID::$CORTEX_API_KEY" --output ./cortexcli2 "$CORTEX_DOMAIN/api/v2/remote-li/0.18.0/windows/artifacts"
