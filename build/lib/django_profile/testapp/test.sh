#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export PYTHONPATH="${SCRIPT_DIR}/../../"; pytest ${SCRIPT_DIR}/../tests