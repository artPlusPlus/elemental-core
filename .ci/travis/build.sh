#!/usr/bin/env bash

conda build --channel artplusplus ./.conda.recipe
conda install --use-local elemental-core
py.test

source deactivate
python ./.ci/move_conda_package.py ./.conda.recipe
