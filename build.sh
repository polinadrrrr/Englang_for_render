#!/usr/bin/env bash
pip install -r requirements.txt
# python (?) Englang_for_render/main/manage.py collectstatic --no-input
python Englang_for_render/main/manage.py migrate
