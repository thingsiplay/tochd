# tochd

Convert game ISO and archives to CD CHD for emulation.

- Author: Tuncay D.
- Website: [tochd-converter](https://thingsiplay.game.blog/tochd-converter)
- Source: [Github](https://github.com/thingsiplay/tochd)
- Releases: [Github Releases](https://github.com/thingsiplay/tochd/releases)
- Update Notes: [CHANGES](CHANGES.md)
- License: [MIT License](LICENSE)

## What is this program for and what are CHD files?

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

## Requirements

The script was originally written for Python 3.10 for Linux. No other Python
module is required. The following external applications are required to run
the script:

```bash
7z
chdman
```

On my Archlinux-based distribution, the programs are available in the
packages: `p7zip mame-tools`

### Installation

#### Manual installation

No special installation setup is required, other than the above base
requirements. Give `tochd.py` the executable bit, rename the script to exclude
file extension and put it into a directory found in the systems `$PATH` . To
automate these steps, an installation script is provided, but not required. If
you cannot install from AUR, then use following commands to install newest
version manually:

```bash
git clone https://github.com/thingsiplay/tochd
cd tochd
bash suggested_install.sh
tochd --help
```

#### AUR: Install with package manager on Archlinux

The package is available in the Arch User Repository:
[AUR Package Details](https://aur.archlinux.org/packages/tochd)

- `yay -S tochd`
- `pamac install tochd`

## Usage

```bash
usage: tochd [OPTIONS] [FILE ...]

usage: tochd [-h] [--version]
             [--list-examples] [--list-formats] [--list-programs]
             [--7z CMD] [--chdman CMD]
             [-d DIR] [-R] [-p] [-t NUM] [-c NUM] [-m FORMAT]
             [-f] [-q] [-n] [-s] [-E] [-X] [-]
             [file ...]
```

This is a commandline application without a graphical interface. The most basic
operation is to give it a filename, a list of files or directories to work on.
The default behaviour is to convert .iso and .cue+bin and .gdi files to .chd
files with same basename in their original folders. Archives such as .7z and
.zip are extracted and searched for files to convert. The progress information
from `7z` and `chdman` are printed to stdout.

### How to use the commandline options

Options start with a dash and everything else is a file or folder. In example
`tochd .` will search current working directory for files to convert. Use
option `-X` like in `tochd -X .` to list files without processing them. The
option `-d DIR` specifies a directory to output all created .chd files into. In
example `tochd -q -d ~/new_chds ~/Downloads` will process all files it can find
in the "Downloads" directory and save the created .chd files in a folder named
"new_chds" under users home. The `-q` option means "quiet" and will hide
progress information from `7z` and `chdman`, but still output current job
information from this script itself.

You can also specify filenames directly or use shell globbing `*` in example to
give a list of files over. Usually that is not a problem, but if any filename
starts with a dash `-`, then the filename would be interpreted as an option. To
prevent that, you can use double dash option `--` to indicate that anything
following the double dash is a filename and not an option. In example
`tochd -q -- -name_starting_with_dash.iso` would recognize `-q` as an option
and `-name_starting_with_dash.iso` as a filename.

Use `tochd --help` to list all options and their brief description.

### Examples

```bash
tochd --help
tochd -q .
tochd --quiet --stats --names ~/Downloads
tochd -p -- *.7z
```

### Example output

The following is an output from some files I used to test the program. The
failing jobs are supposed to fail, for one or another reason. "Completed" jobs
are files that are successfully created. "Failed" jobs point to the path that
would have been created.

```bash
$ tochd -q cue iso gdi unsupported .
Job 1     Started:    /home/tuncay/Downloads/cue/Vampire Savior (English v1.0).7z
Job 1   Completed:    /home/tuncay/Downloads/cue/Vampire Savior (English v1.0).chd
Job 2     Started:    /home/tuncay/Downloads/cue/3 x 3 Eyes - Sanjiyan Hensei (ACD, SCD)(JPN).zip
Job 2      Failed:    /home/tuncay/Downloads/cue/3 x 3 Eyes - Sanjiyan Hensei (ACD, SCD)(JPN).chd
Job 3     Started:    /home/tuncay/Downloads/cue/Simpsons Wrestling, The (USA).7z
Job 3   Completed:    /home/tuncay/Downloads/cue/Simpsons Wrestling, The (USA).chd
Job 4     Started:    /home/tuncay/Downloads/cue/Shining Wisdom (USA) (DW0355).rar
Job 4   Completed:    /home/tuncay/Downloads/cue/Shining Wisdom (USA) (DW0355).chd
Job 5     Started:    /home/tuncay/Downloads/iso/Parodius_Portable_JPN_PSP-Caravan.iso
Job 5   Completed:    /home/tuncay/Downloads/iso/Parodius_Portable_JPN_PSP-Caravan.chd
Job 6     Started:    /home/tuncay/Downloads/iso/Bust_A_Move_Deluxe_USA_PSP-pSyPSP.iso
Job 6   Completed:    /home/tuncay/Downloads/iso/Bust_A_Move_Deluxe_USA_PSP-pSyPSP.chd
Job 7     Started:    /home/tuncay/Downloads/gdi/[GDI] Metal Slug 6.7z
Job 7   Completed:    /home/tuncay/Downloads/gdi/[GDI] Metal Slug 6.chd
Job 8     Started:    /home/tuncay/Downloads/gdi/[GDI] Virtua Striker 2 (US).7z
Job 8   Completed:    /home/tuncay/Downloads/gdi/[GDI] Virtua Striker 2 (US).chd
Job 9     Started:    /home/tuncay/Downloads/gdi/GigaWing 2.zip
Job 9   Completed:    /home/tuncay/Downloads/gdi/GigaWing 2.chd
Job 10    Started:    /home/tuncay/Downloads/unsupported/Dragon_Ball_Z_Shin_Budokai_USA_PSP-DMU.rar
Job 10     Failed:    /home/tuncay/Downloads/unsupported/Dragon_Ball_Z_Shin_Budokai_USA_PSP-DMU.chd
Job 11    Started:    /home/tuncay/Downloads/unsupported/ActRaiser 2 (USA) (MSU1) [Hack by Conn & Kurrono v4].7z
Job 11     Failed:    /home/tuncay/Downloads/unsupported/ActRaiser 2 (USA) (MSU1) [Hack by Conn & Kurrono v4].chd
Job 12    Started:    /home/tuncay/Downloads/missingfiles.gdi
Job 12     Failed:    /home/tuncay/Downloads/missingfiles.chd
```

### Cancel jobs

At default `Ctrl+c` in the terminal will abort current job and start next one.
Temporary folders and files are removed automatically, but it can't hurt to
check manually for confirmation. Temporary folders are hidden starting with a
dot in name.

### Multiprocessing support

At default all files are processed sequential, only one at a time. Use option
`-p` (short for `--parallel`) to activate multithreading with 2 threads. This
enables the processing of multiple jobs at the same time. Set number of max
threads with option `-t` (short for `--threads`).

#### Drawbacks with multiprocessing / parallel option

- live progress bars and stderror messages of invoked processes from `7z` and
  `chdman` cannot be provided anymore, as they would have been overlapping on
  the terminal, but stdout messages such as statistics are still output
- user input won't be allowed and is automated as much as possible, because
  overlapping messages could lead to stuck on waiting for input and losing the
  context to what file it belongs to are potential problems

## Additional notes, workarounds and quirks

### Forcefully terminating script will leave unfinished files

- If you forcefully terminate the entire script while working, then unfinished
  files and especially temporary folders cannot be removed anymore. These files
  and folders can take up huge amount of space! Temporary folders are hidden
  starting with a dot "." in the name, followed by the name of archive and some
  random characters. Make sure these files are deleted. The regular `Ctrl+c` to
  abort current job is _not_ a forced termination of script (unless option `-E`
  is in effect).

### Files and archives that need special preparation before converting

- Some archives contain multiple folders, each with ISO files of same name. These
  are usually intended to copy and overwrite files in a main folder as a meaning
  of patching. However, the script has no understanding and knowledge about this
  and would try to convert each .iso file on it's own. As a workaround all .iso
  files in the archive are ignored when a sheet type such as CUE or GDI files are
  found.
- There are cases where the audio files can be a different format than what the
  .cue (or .gdi) files expect. In example there are cases where the audio files
  are in .ape format and need to be converted to .wav first. If you are unsure
  about this, then look into any provided readme file or the .cue sheet itself.
  Then convert them before handing it over to .chd conversion.

### Automatic renaming output files based on archive filename

- Sometimes .cue or .iso files found in an archive have a different name than the
  archive filename itself. Sometimes one of them lack important informations and
  you need to determine which of them is "correct". In example translations could
  have important information encoded in the filename of the .cue, which would be
  lost, as the .CHD file is automatically renamed to match the .zip or .7z
  archive in example. Use in such situations option `-R` (short for
  `--no-rename`) to prevent that and leave the original files name found inside
  the archive.

### Use DVD format for certain emulators instead

- Some emulators don't work well with the standard CD format created by
  `chdman createcd` command, which is the default internal command in `tochd`.
  The developers of ppsspp emulator recommends instead using the
  `chdman createdvd` command to vastly improve performance of PSP games
  converted to CHD format. For this reason I have added an option to `tochd`,
  so you can use the DVD format instead with `--mode dvd` . Do not use this
  blindly for all emulators. In fact, most are regular CDs anyway and `tochd`
  defaults to `--mode cd` .
