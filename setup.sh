#!/bin/bash

# ShellcodingDream Setup Script
# Usage: bash setup.sh

set -e

echo "╔════════════════════════════════════════════╗"
echo "║    ShellcodingDream - Setup Script         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "[!] Docker is not installed"
    echo "    Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "[!] Docker Compose is not installed"
    echo "    Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "[+] Docker is installed"
echo "[+] Docker Compose is installed"
echo ""

# Build image
echo "[*] Building Docker image..."
docker-compose build

echo ""
echo "[+] Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Test the installation:"
echo "     docker-compose run --rm shellcoding list"
echo ""
echo "  2. Read the quick start:"
echo "     cat docs/QUICK_START.md"
echo ""
echo "  3. For OSCP tips:"
echo "     cat docs/OSCP_GUIDE.md"
echo ""
echo "  4. Show available commands:"
echo "     docker-compose run --rm shellcoding oscp"
echo ""
echo "Good luck! 🚀"
