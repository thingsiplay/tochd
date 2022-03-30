#!/bin/env bash

name=tochd.py
name_no_ext="${name%.py}"
# install_dir=/usr/local/bin
install_dir=$(systemd-path user-binaries)
install_cmd=$(/usr/bin/which install)

if [ -f "$name_no_ext" ]
then
    "$install_cmd" -m 755 -b -C -D -t "$install_dir" "$name_no_ext" 
else
    "$install_cmd" -m 755 -b -C -D -t "$install_dir" "$name" 
    mv -f "$install_dir/$name" "$install_dir/$name_no_ext"
fi

if [ ! -f "$install_dir/$name_no_ext" ]
then
    echo "Error! Could not install $name_no_ext to $install_dir !!"
    exit 1
else
    echo "$name_no_ext installed to $install_dir/$name_no_ext"
fi
