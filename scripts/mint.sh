#!/bin/bash
DIR="$(dirname "$0")"

python3 "${DIR}/mkroot.py" && "${DIR}/csr.sh"
