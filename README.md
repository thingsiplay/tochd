# tochd

Convert game ISO and archives to CD CHD for emulation.

- Author: Tuncay D.
- Source: https://github.com/thingsiplay/tochd
- Releases: https://github.com/thingsiplay/tochd/releases
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

The script is written in Python 3.10 for Linux. No other Python module is
required. The following external applications are required to run the script:

```
7z
chdman
```

On my Manjaro system, they are available in the packages: `p7zip mame-tools`

## Installation

No special installation setup is required, other than the above base
requirements. Run the script from any directory you want. Give it the
executable bit, rename the script to exclude file extension and put it into a
folder that is in the systems `$PATH` . An installation script "install.sh" is
provided, but not required.

If you have an older Python version, then you might want to check the binary
[release](https://github.com/thingsiplay/tochd/releases) package, which bundles
up the script and Python interpreter to create a standalone executable.

### Optional: Install on Archlinux using PKGBUILD package

If you are using an Archlinux based system, then you can instead build an
Archlinux package and install with `pacman`. Use `makepkg` to generate a .zst
package or download from the
[https://github.com/thingsiplay/tochd/releases](releases) page.
Then use `sudo pacman -U tochd-x.x-x-any.pkg.tar.zst` command (where the `x`
should be replaced by the version number of generated package) to install into
the system. To remove the package, just use `sudo pacman -R tochd`. The
installation directory is under "/usr/bin" and differs from the
"install.sh" that is provided with the repository.

### Optional: Makefile and PyInstaller (you can ignore this part)

The included "Makefile" is to build the package with the standalone binary. It
will create a venv, update stuff in it and run PyInstaller from it. If the
process fails, then maybe the system package `mpdecimal` could be required. At
least this was required on my Manjaro system.

# Usage 

```
usage: tochd [OPTIONS] [FILE ...]

usage: tochd [-h] [--version] [--list-examples] [--list-formats]
             [--list-programs] [--7z CMD] [--chdman CMD] [-d DIR] [-R] [-p]
             [-t NUM] [-c NUM] [-f] [-q] [-E] [-X] [-]
             [file ...]
```

This is a commandline application without a graphical interface. The most basic
operation is to give it a filename, a list of files or directories to work on.
The default behaviour is to convert .iso and .cue+bin and .gdi files to .chd
files with same basename in their original folders. Archives such as .7z and
.zip are extracted and searched for files to convert. The progress information
from `7z` and `chdman` are printed to stdout.

## How to use the commandline options 

Options start with a dash and everything else is file or folder. In example
`tochd .` will search current working directory for files to convert. Using the
option `-X` like this `tochd -X .` will just list files without processing
them. The option `-d DIR` specifies a directory to output the created .chd
files into. In example `tochd -q -d ~/chd ~/Downloads` will process all files
it can find in the "Downloads" directory and save the resulting .chd files in a
folder named "chd" in the users home folder. The `-q` option means "quiet" and
will hide progress information from `7z` and `chdman`, but still print out the
current job information from the script itself.

You can also specify filenames directly or use shell globbing `*` in example to
give a list of files over. Usually that is not a problem, but if any filename
starts with a dash `-`, then the filename would be interpreted as an option.
But you can use the double dash `--` to indicate that anything following the
double dash is a filename, regardless what the first character is. In example
`tochd -- *.7z` will process all .7z files in current directory.

Use `tochd --help` to list all options and their brief description.

## Examples

```
$ tochd --help
$ tochd .
$ tochd -X .
$ tochd ~/Downloads
$ tochd -- *.7z
$ tochd -pfq ~/Downloads | grep 'Completed:' | grep -Eo '/.+$'
$ ls -1 | tochd -
```

## Example output

The following is an output from some files I used to test the program. The
failing jobs are supposed to fail, for one or another reason. "Completed" jobs
are files that are successfully created. "Failed" jobs point to the path that
would have been created.

```
$ tochd -fq cue iso gdi unsupported .
Job 1     Started:	/home/tuncay/Downloads/cue/Vampire Savior (English v1.0).7z
Job 1   Completed:	/home/tuncay/Downloads/cue/Vampire Savior (English v1.0).chd
Job 2     Started:	/home/tuncay/Downloads/cue/3 x 3 Eyes - Sanjiyan Hensei (ACD, SCD)(JPN).zip
Job 2      Failed:	/home/tuncay/Downloads/cue/3 x 3 Eyes - Sanjiyan Hensei (ACD, SCD)(JPN).chd
Job 3     Started:	/home/tuncay/Downloads/cue/Simpsons Wrestling, The (USA).7z
Job 3   Completed:	/home/tuncay/Downloads/cue/Simpsons Wrestling, The (USA).chd
Job 4     Started:	/home/tuncay/Downloads/cue/Shining Wisdom (USA) (DW0355).rar
Job 4   Completed:	/home/tuncay/Downloads/cue/Shining Wisdom (USA) (DW0355).chd
Job 5     Started:	/home/tuncay/Downloads/iso/Parodius_Portable_JPN_PSP-Caravan.iso
Job 5   Completed:	/home/tuncay/Downloads/iso/Parodius_Portable_JPN_PSP-Caravan.chd
Job 6     Started:	/home/tuncay/Downloads/iso/Bust_A_Move_Deluxe_USA_PSP-pSyPSP.iso
Job 6   Completed:	/home/tuncay/Downloads/iso/Bust_A_Move_Deluxe_USA_PSP-pSyPSP.chd
Job 7     Started:	/home/tuncay/Downloads/gdi/[GDI] Metal Slug 6.7z
Job 7   Completed:	/home/tuncay/Downloads/gdi/[GDI] Metal Slug 6.chd
Job 8     Started:	/home/tuncay/Downloads/gdi/[GDI] Virtua Striker 2 (US).7z
Job 8   Completed:	/home/tuncay/Downloads/gdi/[GDI] Virtua Striker 2 (US).chd
Job 9     Started:	/home/tuncay/Downloads/gdi/GigaWing 2.zip
Job 9   Completed:	/home/tuncay/Downloads/gdi/GigaWing 2.chd
Job 10    Started:	/home/tuncay/Downloads/unsupported/Dragon_Ball_Z_Shin_Budokai_USA_PSP-DMU.rar
Job 10     Failed:	/home/tuncay/Downloads/unsupported/Dragon_Ball_Z_Shin_Budokai_USA_PSP-DMU.chd
Job 11    Started:	/home/tuncay/Downloads/unsupported/ActRaiser 2 (USA) (MSU1) [Hack by Conn & Kurrono v4].7z
Job 11     Failed:	/home/tuncay/Downloads/unsupported/ActRaiser 2 (USA) (MSU1) [Hack by Conn & Kurrono v4].chd
Job 12    Started:	/home/tuncay/Downloads/missingfiles.gdi
Job 12     Failed:	/home/tuncay/Downloads/missingfiles.chd
```

## Cancel jobs

At default `Ctrl+c` in the terminal will abort current job and start next one.
Temporary folders and files are removed automatically, but it can't hurt to
check manually for confirmation. Temporary folders are hidden starting with a
dot in name.

## Multiprocessing support

At default all files are processed sequential, only one at a time. Use option
`-p` (short for `--parallel`) to activate multithreading with 2 threads. This
enables the processing of multiple jobs at the same time. Set number of max
threads with option `-t` (short for `--threads`).

### Drawbacks with multiprocessing / parallel option

- live progress bars and stderror messages of invoked processes from `7z` and
  `chdman` cannot be provided anymore, as they would have been overlapping on
  the terminal, but stdout messages such as statistics are still output
- user input won't be allowed and is automated as much as possible, because
  overlapping messages could lead to stuck on waiting for input and losing the
  context to what file it belongs to are potential problems

# Additional notes, workarounds and quirks

If you forcefully terminate the entire script while working, then unfinished
files and especially temporary folders cannot be removed anymore. These files
and folders can take up huge amount of space! Temporary folders are hidden
starting with a dot "." in the name, followed by the name of archive and some
random characters. Make sure these files are deleted. The regular `Ctrl+c` to
abort current job is *not* a forced termination of script (unless option `-E`
is in effect).

Some archives contain multiple folders, each with ISO files of same name. These
are usually intended to copy and overwrite files in a main folder as a meaning
of patching. However, the script has no understanding and knowledge about this
and would try to convert each .iso file on it's own. As a workaround all .iso
files in the archive are ignored when a sheet type such as CUE or GDI files are
found.

Somtimes .cue or .iso files found in an archive have a different name than the
archive filename itself. Sometimes one of them lack important informations and
you need to determine which of them is "correct". In example translations could
have important information encoded in the filename of the .cue, which would be
lost, as the .CHD file is automatically renamed to match the .zip or .7z
archive in example. Use in such situations option `-R` (short for
`--no-rename`) to prevent that and leave the original files name found inside
the archive.

There are cases where the audio files can be a different format than what the
.cue (or .gdi) files expect. In example there are cases where the audio files
are in .ape format and need to be converted to .wav first. If you are unsure
about this, then look into any provided readme file or the .cue sheet itself.
Then convert them before handing it over to .chd conversion.

