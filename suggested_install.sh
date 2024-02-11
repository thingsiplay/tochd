#!/bin/env bash

print_usage() {
	self_filename="${0##*/}"
	echo "usage: ${self_filename} [-h] [DIR...]"
	echo \
		'
Search set of folders until one is found in the systems $PATH with write
access. Use it to install the files as commands into the folder. Without DIR
arguments a list of default folders are searched.

positional arguments:
  DIR                  folders to look for when searching for installation path

options:
  -h                   print this help and exit'
}

# Default path to search with priority, if no arguments are given.
default_install_dir=""
install_cmd="$(/usr/bin/which install)"

while getopts ':h' OPTION; do
	case "$OPTION" in
	h)
		print_usage
		exit 0
		;;
	?)
		continue
		;;
	esac
done

# This variable will be set by the following function if any usable path is
# found. Then later functions will use it as base folder to install into.
install_dir=""
# This one will also be set by the following function. Can be useful to print
# in case of a problem.
list_of_install_dirs=""

# Searches the list of system $PATH if any of the given directories are found
# in it. If so, then update the variable "install_dir" with it, when user has
# write permission. If no arguments to the function are given, then it defaults
# to some predefined set of directories to look for.
find_install_dir() {
	if [ ${#} -eq 0 ]; then
		list_of_install_dirs=(
			"${default_install_dir}"
			"$(systemd-path user-binaries)"
			"$HOME/.local/bin"
			"$HOME/bin"
			"/usr/local/bin"
		)
	else
		list_of_install_dirs=("${@}")
	fi

	# Convert the system $PATH variable into a Bash list.
	IFS=: read -r -d '' -a list_of_path < <(printf '%s:\0' "$PATH")

	for dir in "${list_of_install_dirs[@]}"; do
		for path in "${list_of_path[@]}"; do
			if [ "${path}" == "${dir}" ]; then
				if [ -w "${path}" ]; then
					install_dir="${path}"
				else
					echo "No write permission for install directory:"
					echo "        ${path}"
					exit 1
				fi
				return
			fi
		done
	done
}

# Install the given "filename" as a command into the previously set
# "install_dir". It will remove the file extension, so it works like any
# normal system command. Second argument can be an option with special
# actions, such as creating an additional symbolic link.
install_program() {
	filename="${1}"
	file_no_ext="${filename%.*}"
	option="${2}"

	"${install_cmd}" -m 755 -b -C -D -t "${install_dir}" "${filename}"

	if ! [ "${?}" == 0 ]; then
		exit 1
	else
		mv -f "${install_dir}/${filename}" "${install_dir}/${file_no_ext}"

		if [ "${option}" == "--symlink" ]; then
			ln --symbolic \
				"${install_dir}/${file_no_ext}" \
				"${install_dir}/${filename}"
		fi
	fi

	if [ -f "${install_dir}/${file_no_ext}" ]; then
		echo ""
		echo "${filename} installed as:"
		echo "        ${install_dir}/${file_no_ext}"
		if [ "${option}" == "--symlink" ]; then
			echo "        ${install_dir}/${filename}"
		fi
	else
		echo "Error! Could not install ${filename} to ${install_dir}"
		exit 1
	fi
}

# Simple question to answer with "y" for proceeding. Any other key than "y"
# will cause to end the script.
ask_proceed() {
	echo "Continue installallation programs to:"
	echo "        ${install_dir}"
	echo ""
	echo "(Y)es or (N)o:"

	read -t 10 answer

	first_letter="${answer:0:1}"
	if ! [[ "${first_letter}" == "y" || "${first_letter}" == "Y" ]]; then
		exit 1
	fi
}

if [ $# -eq 0 ]; then
	find_install_dir
else
	find_install_dir "${@}"
fi

if [ "${install_dir}" == "" ]; then
	echo "Error! No usable install directory could be recognized from:"
	echo "     \"${list_of_install_dirs[*]}\" "
	exit 1
else
	ask_proceed
fi

# Install following files by removing their extension.
install_program "tochd.py"
