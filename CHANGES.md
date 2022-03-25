# Changes

Update history for **tochd**.

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
