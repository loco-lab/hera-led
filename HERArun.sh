#! /usr/bin/env bash
set -e
source /home/hera-led/mambaforge/bin/activate hera-led
echo $(which python)
python /home/hera-led/hera-led/HERAtest.py
