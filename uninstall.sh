#!/bin/env bash

found=$(which -a tochd)

echo "Found installations:"
echo "${found}"
echo
echo 'WARNING: If you installed tochd with a package manager, then use your' \
	'package manager instead to uninstall it again.'
echo

SAVEIFS=$IFS
IFS=$'\n'
list_of_installed=(${found})
IFS=$SAVEIFS

for path in "${list_of_installed[@]}"; do
	echo 'Do you want remove?'
	echo "        ${path}"
	echo ''
	echo '(Y)es or (N)o:'

	read -t 10 answer

	first_letter="${answer:0:1}"
	if [[ "${first_letter}" == "y" || "${first_letter}" == "Y" ]]; then
		if rm -f "${path}"; then
			echo "${path} uninstalled."
		else
			echo "Error! Could not uninstall ${path} !!"
			exit 1
		fi
	else
		continue
	fi
done
