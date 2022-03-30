#!/bin/env bash

name=tochd.py
name_no_ext="${name%.py}"
# install_dir=/usr/local/bin
install_dir=$(systemd-path user-binaries)
install_cmd=$(/usr/bin/which install)

rm -f "$install_dir/$name_no_ext"

if [[ $? -ne 0 ]]
then
    echo "Error! Could not uninstall $name_no_ext from $install_dir !!"
    exit 1
else
    echo "$name_no_ext uninstalled from $install_dir"
fi
