#!/usr/bin/env bash

pip install --user --upgrade pipx
pipx install poetry
pipx upgrade poetry
poetry shell
poetry install
mkdir -vp data/{in,ir,gl,f8949,f1099}
