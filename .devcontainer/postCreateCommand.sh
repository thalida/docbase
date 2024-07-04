#!/usr/bin/env bash

cd $WORKSPACE_FOLDER/api
poetry install
pre-commit install

cd $WORKSPACE_FOLDER/app
npm install

npm i -g @quasar/cli

chmod -R +x $WORKSPACE_FOLDER/scripts
sudo ln -s $WORKSPACE_FOLDER/scripts/* /usr/local/bin
