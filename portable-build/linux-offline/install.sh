#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "PDF2Word - Linux Offline Kurulum"
echo "================================"

if [ "$EUID" -ne 0 ]; then
    echo "Bu script root yetkisi gerektirir."
    echo "Kullanım: sudo ./install.sh"
    exit 1
fi

if [ -d "debs" ]; then
    dpkg -i debs/*.deb 2>/dev/null || true
    apt-get install -f -y 2>/dev/null || true
    echo "Kurulum tamamlandı!"
else
    echo "HATA: debs/ klasörü bulunamadı!"
    exit 1
fi
