#!/bin/bash
# https://docs-cortex.paloaltonetworks.com/r/Cortex-CLOUD/Cortex-Cloud-Runtime-Security-Documentation/Cortex-CLI-for-Cloud-Workload-Protection

set -e

cortexcli  --log-level <ERROR LEVEL> –-api-base-url <API URL> --api-key <API key from the "Authenticate" step in the CLI connector screen> \
    --auth-id 1 api scan  --api-spec-file <OPENAPI SPEC LOCATION>  \
    --scanned-app-url <BASE URL OF THE SCANNED APP> --java-location <JAVA BIN LOCATION>
