# Changes

Update history for [tochd](https://github.com/thingsiplay/tochd)

## Next

- new: option `-H`, `--hunksize` to specify the exact size of hunks in bytes
  used with chdman, only needed in special cases,
  [#6](https://github.com/thingsiplay/tochd/issues/6)
- changed: search for executables such as `7z` and `chdman` programs in
  scripts own installed directory first, this makes it more portable
- changed: temporary folders where archives are unpacked to will start with
  dot again, so they are hidden at default, but only if no path is specified
  with `--temp-dir`

## v0.12 - March 8, 2024

Note: We are jumping over v0.11 and combine it with next version v0.12.

- bug: counter for finish states like "Completed: 0" are disabled, when
  combining the options `-p` and `-s`, because counting these variables is not
  thread safe at the moment
- bug: cpu count was wrongly reported when using custom number for threads
- new setting in option: specify `-m auto` to determine "cd" or "dvd" format
  based on filesize with a 750 MB threshold (thanks AlexanderRavenheart
  [#3](https://github.com/thingsiplay/tochd/pull/3))
- changed: generation and handling of temporary folders refactored, now it's
  using proper builtin `tempfile` functionality instead custom logic, currently
  the folders are not hidden anymore (thanks AlexanderRavenheart
  [#3](https://github.com/thingsiplay/tochd/pull/3))
- changed: due to the new approach of temporary folders, the option `-E` will
  finally cause `Ctrl+c` to delete temporary files and folders before exiting
  (thanks AlexanderRavenheart
  [#3](https://github.com/thingsiplay/tochd/pull/3))
- removed: option `-f` and `--fast`, because nobody actually needs it, its an
  artefact of early testings to quickly generate huge files
- lot of internal code refactor for being more consistent styling and naming
  (thanks AlexanderRavenheart
  [#3](https://github.com/thingsiplay/tochd/pull/3))

## v0.10 - February 11, 2024

- new: option `-m` to specify disc format created by `chdman` backend,
  defaults to `cd`, but for certain emulators (such as ppsspp) `dvd` is
  recommended
- new: option `-s` to display additional stats, such as a summary at the end and
  how long the operation took
- new option `-n` to simply shorten the displayed path of printed jobs as
  filenames only, excluding the folder part
- changed: also the install and uninstall scripts are reworked
- removed: Makefile deleted, no need for PyInstaller packaged bundles, assuming
  most modern distributions can run the Python script anyway
- removed: PKGBUILD deleted, which was used to create the Archlinux package
  for the AUR, its just confusing and unnecessary for the end user and not
  needed to be part of the project

## v0.9 - July 06, 2022

- changed: now flushes the output of job message without buffering, useful for
  live monitoring and reading stdout the moment it is written
- new: added a "PKGBUILD" for use with `pacman`, can be used to generate an
  Archlinux package

## v0.8 - March 30, 2022

- new: pseudo compiled bundle of the script with pyinstaller to build a
  standalone executable, available on
  [Releases](https://github.com/thingsiplay/tochd/releases) page
- new: "Makefile" script for `make` to create the standalone bundle of Python
  script with the Python interpreter and package it into an archive
- changed: runs with default options `-X .`, if no options provided
- some little internal optimizations or additions, such as code comments

## v0.7 - March 26, 2022

- changed: when multithreading with option `-p`, the stdout and statistics from
  invoked `7z` and `chdman` commands are no longer hidden anymore, only the
  progress bar and stderr stream are hidden, use option `-q` to supress any
  output from these commands (how it worked previously)

## v0.6 - March 25, 2022 - Complete rewrite

- new implementation of entire script by rewriting from ground up, additional
  source code checks are done with mypy and flake8 to ensure some basic
  quality, hopefully more readable code and improved robustness

- changed: default behavior of `Ctrl+c` (keyboard interrupt, SIGINT) will stop
  current job process and continue with the next one in list
- changed: more reliable in removing temporary folders and unfinished files,
  even with multithreading enabled and on `Ctrl+c` signal
- new: option `-E` to change behavior of `Ctrl+c` to immadiately stop execution
  of entire script, which may leave temporary folders and unfinished files on
  the system

- new: option `-` (a single dash) to read files from stdin for each line
- changed: ignore files within same folder as .gdi files
- new: option `-R` to disable automatic renaming of .chd files created from an
  archive and leave original filename
- changed: default behavior for automatically renaming produced .chd filename
  from inside an archive to match the source archive name (this can be disable
  with new option `-R`)
- even more undiscussed new options: `--7z`, `--chdman`, `-f`, `-q`, `-X`

- changed: different job messages to indicate failure or success
- changed: does not wait to finish first group of .iso files anymore,
  previously script was producing .iso files first and then loading other types

## v0.5

- new: option `-d` to specify output directory for the temporary folder and final .chd file, if specified then all new files are created in this directory
- new: option `-r` to rename .chd files created from archives to match their archive filenames
- changed: added job index number to each "Processing" and "Finished" messages, useful if input and output paths differ or parallel option `-p` is active
- new: option `--list-apps` will list path of all found programs used by tochd
- new: projects Github link added to the bottom of `--help` output

## v0.4

- new: option `-t` to specify the max number of threads for multiprocessing
- changed: defaults to 2 threads if option `-p` is used without `-t`
- changed: automatically use option `-y` on 7z process when multiprocessing with `-p` is active, useful not to wait on user input
- new: option `-c` to limit the number of processors to utilize when compressing with chdman, indipendet from multiprocessing threads
- fix: did not extract archives properly in specific situations
- fix: if input was a directory, then the content was ignored, now all files in a directory are processed

## v0.3

- new: initial support for experimental multithreading, use `-p` option to activate

## v0.2

- new: check each archive, only extract files if supported files are found inside
- new: if an archive or directory contains .gdi files, then ignore all other files and only process .gdi files

## v0.1

- initial release
