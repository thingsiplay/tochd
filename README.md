# tochd

Convert ISOs and archives into CD CHD for emulation.

# Requirements

The script was created with Python 3.10 on Linux in mind and may not work on other environments, as it was not tested otherwise. It makes use of pre existing programs that needs to be installed on the system to extract archives and convert the formats. 

* The executable filenames are: `7z` `chdman`
* I have installed following packages in Manjaro which install the above executables. It is possible that the packages are named differently for your distribution: `p7zip` `mame-tools`

# Usage

This is a commandline application and has no graphical user interface. The usage overall is very simple: give it a filename or multiple files or even a directory and that's it. It will process all given files and all files in a given directory automatically, depending if the file formats are supported. Put the executable `tochd.py` into a directory that is in your environmental $PATH and just run it from any folder. Alternatively rename it to just `tochd` without file extension. The CHD files are created in the same folder where the input files are. If the CHD exists already, then it won't create it again.

## Examples

    tochd --help
    tochd .
    tochd ~/Downloads/new_isos
    tochd *.7z
    tochd file1.zip file2.iso
 
# What is this program for and what are CHD files?

If you use RetroArch or possibly any emulator that supports CHD files, then you might want to convert your ISO and CUE+BIN files to it. It is a compressed single file format. The helper tool `chdman` from the MAME tools can do that. And often the files are in archives, so they need to be extracted first in a temporary folder, which `7z` does. No need for manual extraction, this script takes care. I wanted automate all of this and it started as a simple Bash script, but later on decided to utilize Python.

# Multithreading support

Normally all files are created one after another, as each process waits before
it's completion.  If you use the new option `-p` (short for
`--parallel`), then multiple process are created and execute at the same time.
This can save a lot of time, depending on your hardware.  However, this
approach comes with a few drawbacks.

- cancelling the script execution with Ctrl+c in the terminal in example will
  not clean up any hidden temporary files and folders
- output of the individual programs are no longer available 

# Changes

## v0.3
- new: initial support for experimental multithreading, use `-p` option to
  activate

## v0.2
- new: check each archive, only extract files if supported files are found inside
- new: if an archive or directory contains .gdi files, then ignore all other files and only process .gdi files
