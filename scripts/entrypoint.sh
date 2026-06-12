#!/bin/bash

# ShellcodingDream Docker Entrypoint

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ $# -eq 0 ] || [ "$1" == "--help" ]; then
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════╗"
    echo "║    ShellcodingDream - Dockerized Edition  ║"
    echo "║    OSCP-Ready Shellcode Obfuscation Tool  ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    python3 -m app.main --help
else
    python3 -m app.main "$@"
fi
