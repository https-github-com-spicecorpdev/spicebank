#!/bin/bash

pushd ~/dev/api
sh build.sh
popd
pushd ~/dev/api/backend 
gnome-terminal -e "flask --app app run --port 5000"
gnome-terminal -e "flask --app manager_app run --port 5001"
popd