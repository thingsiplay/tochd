# tochd

Convert game ISO and archives to CD CHD for emulation.

- Author: Tuncay D.
- Project: https://github.com/thingsiplay/tochd
- Update Notes: [CHANGES](CHANGES.md) 
- License: [MIT License](LICENSE)

# What is this program for and what are CHD files?

Automation script written in Python as a frontend to `7z` and `chdman` for
converting CD formats into CD CHD.

When you are playing CD based games on RetroArch or possibly on any emulator
which supports CHD files, then you might want to convert your ISO and CUE+BIN
or GDI files into the CHD format. It has the advantage good compression and
produces a single file for each CD. This saves a lot of space and makes
organization easier.

To achieve this, the separate program `chdman` from the MAME tools is invoked,
which introduced the CHD format in the first place. Often you need to extract
those various CD formats from archives such as .7z or .zip files too. The
program `7z` is used to extract those files, before handing them over for
conversion.

# Requirements

The script is written in **Python 3.10** and with **Linux** in mind and may
not work on other environments. It was not tested or reported otherwise. At
least two external applications are essential and required to run the script:

```
7z
chdman
```

My operating system is Manjaro and the programs can be found in installing
following packages:

```
pamac install p7zip mame-tools
```

## Installation

Just copy or move the file "tochd.py" in a directory that is in the systems
`$PATH` and give it the executable bit. Optionally rename it to "tochd". Now
you should be able to run the script from any directory by command 
`tochd --help` in example.

# Usage 

This is a commandline application and has no graphical user interface. The
usage is simple: pass over one or multiple filenames or possibly directory
paths and that's it. All given files and all files from any given directory are
processed automatically, provided the formats are supported. Such a command
could look like `tochd .` to lookup all files in current directory. Or
`tochd -p Downloads/*.7z` to activate multithreading and looking for all ".7z"
files in directory "Downloads". The CD CHD files are created in their original
directories, but a destination path can be specified with `-d` .

At default `Ctrl+c` in the terminal will abort current job and start next one.
Temporary folders and files should be removed, but it can't hurt to check
manually for confirmation. Temporary folders are hidden starting with a dot in
name.

## Examples

```
$ tochd --help
$ tochd .
$ tochd ~/Downloads
$ tochd -q -- *
$ tochd -pfq ~/Downloads | grep 'Completed:' | grep -Eo '/.+$'
$ tochd -d ~/converted -- *.7z > tochd.log
$ ls -1 | tochd -
```

## Multiprocessing support

At default all files are processed sequential, only one at a time. Use option
`-p` (short for `--parallel`) to activate multithreading with 2 threads. This
enables the processing of multiple jobs at the same time. Set number of max
threads with option `-t` (short for `--threads`).

### Drawbacks with multiprocessing / parallel option

- live progress bars and stderror messages of invoked processes from `7z` and
  `chdman` cannot be provided anymore, as they would have been overlapping on
  the terminal, but stdout messages such as statistics are still output
- user input won't be allowed and automated as much as possible, because
  overlapping messages and stuck on waiting or losing the context to what file
  it belongs to are potential problems

# Additional notes, workarounds and quirks

This program is still beta software. Watch out for unfinished .chd files and
undeleted hidden temporary folders, especially when cancelling jobs or
forcefully terminating the script while working. These files and folders can
take up a huge amount of space! They are hidden and start with a dot "." in
their name, followed by the archives original name and random characters.

Make sure to use the option double dash `--` if any given filename starts with
a dash "-", as it would otherwise be interpreted as an option. Alternatively
enclose each filename or path in quotes or use stdin for filenames, because
nothing from stdin is interpreted as options.

Some archives contain multiple folders, each with ISO files of same name. These
are usually intended to copy and overwrite files in a main folder as a meaning
of patching. However, the script has no understanding and knowledge about this
and would try to convert each .iso file on it's own. As a workaround all .iso
files in the archive are ignored when a sheet type such as CUE or GDI files are
found.
