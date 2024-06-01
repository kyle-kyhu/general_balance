#!/usr/bin/env bash
# exit on error
set -o errexit

export DJANGO_SETTINGS_MODULE=general_balance.settings_production

echo "Installing python dependencies"
pip install -U pip
pip install -r requirements.txt
