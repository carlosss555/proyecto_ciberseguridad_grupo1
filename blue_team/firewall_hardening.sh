#!/bin/bash

echo "======================================"
echo " BLUE TEAM - FIREWALL HARDENING"
echo "======================================"

echo "[+] Configurando políticas por defecto..."

sudo ufw default deny incoming
sudo ufw default allow outgoing

echo "[+] Permitiendo SSH..."

sudo ufw allow 22/tcp

echo "[+] Activando firewall..."

sudo ufw --force enable

echo ""
echo "[+] Estado actual del firewall:"
sudo ufw status verbose

echo ""
echo "Firewall configurado correctamente."
