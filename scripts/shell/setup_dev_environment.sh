#!/usr/bin/env bash

pip install --user --upgrade pipx
pipx install poetry
pipx upgrade poetry
poetry shell
poetry install
mkdir -vp data/{average,f8949,f1099,gl,in,ir,log,out}
