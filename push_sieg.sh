#!/bin/bash

cd ~/SIEG-Hub

# Timestamp para el commit
NOW=$(date +"%Y-%m-%d %H:%M")

# Añadir todos los cambios
git add .

# Crear commit con fecha y hora
git commit -m "Actualización automática SIEG Dashboard — $NOW"

# Subir a GitHub
git push
