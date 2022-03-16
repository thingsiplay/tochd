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

# Multiprocessing support

Normally all files are processed sequential, only one after another.  Use the `-p` option (short for `--parallel`) to activate multiprocessing.  This enables the creation of threads to extract and convert multiple files at the same time. This can save a lot of time, depending on the input data and your hardware.  At default only 2 threads are created at the same time, because chdman uses up all cores at default.  Use `-t` option (short for `--threads`) with a number to specify how many threads should be created.

## However, multiprocessing has some drawbacks here:

- output of individual processes from 7z and chdman are not available anymore, as they would overlap on the stdout
- consequently no user input can be done and the process would stuck forever, so at least for 7z the option `-y` (assume Yes on all queries) is used, this can lead to unwanted overwriting of same filenames from the extracted archive
- cancelling the script execution with Ctrl+c in the terminal in example will no longer clean up any hidden temporary files and folders, but it is cleaned up if thread terminates successfully

# Changes

**Important**: Since v0.2 was a bug present that created the temporary folder in
current directory, instead of the archives original directory. This means you
could have a lot of hidden temporary folders on your drive. So please check for
hidden folders. This bug is fixed.

## v0.4
- new: option `-t` to specify the max number of threads for multiprocessing
- changed: defaults to 2 threads if option `-p` is used without `-t`
- changed: automatically use option `-y` on 7z process when multiprocessing
  with `-p` is active, useful not to wait on user input
- new: option `-c` to limit the number of processors to utilize when
  compressing with chdman, indipendet from multiprocessing threads
- fix: did not extract archives properly in specific situations
- fix: if input was a directory, then the content was ignored, now all files in
  a directory are processed

## v0.3
- new: initial support for experimental multithreading, use `-p` option to
  activate

## v0.2
- new: check each archive, only extract files if supported files are found inside
- new: if an archive or directory contains .gdi files, then ignore all other files and only process .gdi files

## v0.1
- initial release
