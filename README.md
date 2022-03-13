# tochd
Convert ISOs and archives into CD CHD for emulation.

# Requirements
The script was created with Python 3.10 on Linux in mind and may not work on other environments, as it was not tested otherwise. It makes use of pre existing programs that needs to be installed on the system to extract archives and convert the formats: `7z`, `chdman`

# Usage
This is a commandline application and has no graphical user interface. The usage overall is very simple: give it a filename or multiple files or even a directory and that's it. It will process all given files and all files in a given directory automatically, depending if the file formats are supported. Put the executable `tochd` into a directory that is in your environmental $PATH and just run it from any folder. The CHD files are created in the same folder where the input files are. If the CHD exists already, then it won't create it again.

## Examples
    tochd --help
    tochd .
    tochd ~/Downloads/new_isos
    tochd *.7z
    tochd file1.zip file2.iso
 
# What is this program for and what are CHD files?
If you use RetroArch or possibly any emulator that supports CHD files, then you might want to convert your ISO and CUE+BIN files to it. It is a compressed single file format. The helper tool `chdman` from the MAME tools can do that. And often the files are in archives, so they need to be extracted first in a temporary folder. I wanted automate all of this and it started as a simple Bash script, but later on decided to utilize Python.
