#!/bin/env python

import signal
import atexit
import sys
import argparse
import multiprocessing
import subprocess
import shutil
import os.path
import random
import string
import re

from pathlib import Path
from typing import TypeAlias


Argparse: TypeAlias = argparse.Namespace
CompletedProcess: TypeAlias = subprocess.CompletedProcess


class App:
    """ Contains all settings and meta information for the application. """

    name: str = 'tochd'
    version: str = '0.6'
    types = {
        'sheet': ('gdi', 'cue',),
        'image': ('iso',),
        'archive': ('7z', 'zip', 'gz', 'gzip', 'bz2', 'bzip2', 'rar', 'tar',)
    }
    exclude_hidden = True

    def __init__(self, args: Argparse) -> None:
        """ Construct application attributes used as settings. """

        self.print_version: bool = args.version
        self.fast: bool = args.fast
        self.list_programs: bool = args.list_programs
        self.list_formats: bool = args.list_formats
        self.list_examples: bool = args.list_examples
        self.path: Path = Path(sys.argv[0])
        self.programs: dict[str, Path] = {
            'Python': Path(sys.executable),
            'chdman': App.which(args.chdman),
            '7z': App.which(args.p7z),
        }
        self.output_dir: Path | None = App.existing_dir(args.output_dir)
        self.no_rename: bool = args.no_rename
        self.files: list[File] = self.get_files(args.file)
        if args.stdin:
            self.files.extend(self.get_files(get_stdin_lines()))
        self.chdprocessors: int = args.chdprocessors
        self.parallel: bool = args.parallel
        self.threads: int = args.threads
        self.quiet: bool = args.quiet or args.parallel
        self.dry_run: bool = args.dry_run
        self.emergency_break: bool = args.emergency_break
        self.pending_temp_list: list[Path] = []

    def get_files(self, files: list[str]) -> list:
        """ Filter and convert list of strings to list of supported Files. """

        new_list: list[File] = []
        for file in files:
            path: Path = fullpath(file)
            supported: File | None
            if path.is_file():
                supported = self.get_supported_file(path)
                if supported:
                    new_list.append(supported)
            elif path.is_dir():
                for dir_entry in path.iterdir():
                    supported = self.get_supported_file(dir_entry)
                    if supported:
                        new_list.append(supported)
        new_list = self.filter_other_in_gdi_dirs(new_list)
        new_list = self.filter_images_in_sheet_dirs(new_list)
        return new_list

    def filter_other_in_gdi_dirs(self, list_of_files):
        """ Remove all other files from list within same dir as .gdi. """

        gdi_dirs = [f.input.parent for f in list_of_files
                    if f.input.suffix == '.gdi']
        if gdi_dirs:
            filtered_list: list[File] = []
            for file in list_of_files:
                if (file.input.parent not in gdi_dirs
                        or file.input.suffix == '.gdi'):
                    filtered_list.append(file)
            return filtered_list
        else:
            return list_of_files

    def filter_images_in_sheet_dirs(self, list_of_files):
        """ Remove all image files from list within same dir as sheets. """

        sheet_dirs = [f.input.parent for f in list_of_files
                      if f.type == 'sheet']
        if sheet_dirs:
            filtered_list: list[File] = []
            for file in list_of_files:
                if (file.input.parent in sheet_dirs
                        and file.input.suffix == '.iso'):
                    continue
                else:
                    filtered_list.append(file)
            return filtered_list
        else:
            return list_of_files

    def get_supported_file(self, path: Path):
        """ Transform Path to a File, if supported type and not hidden dir. """

        if not (self.exclude_hidden
                and path.name.startswith('.')):
            file: File = File(path, dir=self.output_dir)
            if file.type:
                return file
        return None

    def register_pending_temp_list(self, file: Path):
        """ Add file to list of marked for deletion. """

        self.pending_temp_list.append(file)

    def unregister_pending_temp_list(self, file: Path):
        """ Remove file from list of marked for deletion. """

        self.pending_temp_list.remove(file)

    def clean_pending_temp_list(self):
        """ Delete all temporary folders on disk marked for deletion. """

        for file in self.pending_temp_list:
            self.delete_temp_dir(file)
        self.pending_temp_list = []

    def delete_temp_dir(self, path: Path):
        """ Delete folder structure on disk if it is a temporary folder. """

        if (path.is_dir()
                and path.name.startswith('.')
                and '_' in path.suffix
                and not path.as_posix() == Path('~').expanduser().as_posix()
                and not path.as_posix() == '/'
                and not path.as_posix() == fullpath('.').as_posix()):
            shutil.rmtree(path.as_posix(), ignore_errors=True)
        return path

    def convert(self, file_list: list, startindex: int = 1) -> int:
        """ Convert all input files from specific filetype to CHD. """

        lastindex: int = startindex
        if self.parallel:
            if self.threads == 0:
                pool = multiprocessing.Pool()
            else:
                pool = multiprocessing.Pool(processes=self.threads)
        for jobindex, file in enumerate(file_list, startindex):
            lastindex = jobindex + 1
            if self.dry_run:
                self.message_job('Skipped', file.input, jobindex)
                continue
            elif file.output.exists():
                self.message_job('Skipped', file.input, jobindex)
                continue
            elif (file.type == 'image' or file.type == 'sheet'):
                self.register_pending_temp_list(file.output)
                if self.parallel:
                    pool.apply_async(self.convert_file, (file, jobindex,))
                else:
                    self.convert_file(file, jobindex)
                self.unregister_pending_temp_list(file.output)
            elif file.type == 'archive':
                if file.tempdir:
                    self.register_pending_temp_list(file.tempdir)
                self.register_pending_temp_list(file.output)
                if self.parallel:
                    pool.apply_async(self.convert_archive, (file, jobindex,))
                else:
                    self.convert_archive(file, jobindex)
                self.unregister_pending_temp_list(file.output)
            else:
                self.message_job('Skipped', file.input, jobindex)
                continue
        if self.parallel:
            pool.close()
            pool.join()
        return lastindex

    def convert_file(self, file, jobindex: int) -> CompletedProcess:
        """ Convert File to CHD executing chdman. """

        if jobindex:
            self.message_job('Started', file.input, jobindex)
        command: list[str] = []
        command.append(self.programs['chdman'].as_posix())
        command.append('createcd')
        if self.fast:
            command.append('--compression')
            # none=Uncompressed, cdlz=CD LZMA, cdzl=CD Deflate, cdfl=CD FLAC
            command.append('none')
        if self.chdprocessors:
            command.append('--numprocessors')
            command.append(str(self.chdprocessors))
        command.append('--input')
        command.append(file.input.as_posix())
        command.append('--output')
        command.append(file.output.as_posix())

        completed = subprocess.run(command, capture_output=self.quiet)
        if jobindex:
            if (completed.returncode == 0
                    and file.output.exists()):
                self.message_job('Completed', file.output, jobindex)
            else:
                self.message_job('Failed', file.output, jobindex)
                file.output.unlink(missing_ok=True)
        return completed

    def convert_archive(self, archive,
                        jobindex: int) -> CompletedProcess | None:
        """ Extract and convert an archive to CHD. """

        self.message_job('Started', archive.input, jobindex)
        archlist: list[File] = self.listing_from_archive(archive)
        archlist = [f for f in archlist
                    if f.type == 'image'
                    or f.type == 'sheet']
        archlist = self.filter_other_in_gdi_dirs(archlist)
        archlist = self.filter_images_in_sheet_dirs(archlist)
        # workaround
        if [f for f in archlist if f.type == 'sheet']:
            archlist = [f for f in archlist if not f.input.suffix == '.iso']

        if not archlist:
            self.message_job('Failed', archive.output, jobindex)
            return None

        self.register_pending_temp_list(archive.tempdir)
        command: list[str] = []
        command.append(self.programs['7z'].as_posix())
        command.append('x')
        if self.quiet:
            command.append('-y')
        command.append(archive.input.as_posix())
        command.append(f'-o{archive.tempdir.as_posix()}')

        completed = subprocess.run(command, capture_output=self.quiet)
        if completed.returncode == 0:
            for file in archlist:
                completed = self.convert_file(file, 0)
                if self.no_rename:
                    dest_path = archive.output.with_name(file.output.name)
                else:
                    dest_path = archive.output
                dest_path.unlink(missing_ok=True)
                if completed.returncode == 0:
                    shutil.move(file.output.as_posix(), dest_path.as_posix())
                    if dest_path.exists():
                        self.message_job('Completed', dest_path, jobindex)
                else:
                    self.message_job('Failed', dest_path, jobindex)
        else:
            self.message_job('Failed', archive.output, jobindex)

        self.delete_temp_dir(archive.tempdir)
        return completed

    def listing_from_archive(self, file) -> list:
        """ Get a list of all paths in archive as File. """

        command: list[str] = []
        command.append(self.programs['7z'].as_posix())
        command.append('l')
        command.append('-slt')
        if self.quiet:
            command.append('-y')
        command.append(file.input.as_posix())
        completed = subprocess.run(command, capture_output=True, text=True)
        if completed.returncode == 0:
            listing: list[str]
            listing = re.findall(r'Path = (.+)', completed.stdout, re.M)
            return [File(file.tempdir / Path(entry)) for entry in listing[1:]]
        else:
            return []

    def message_job(self, message: str, path: Path, jobindex: int) -> None:
        """ Print job message with correct formatting. """

        pad_size: int = 12
        pad_size = pad_size - len(str(jobindex))
        padded_msg = message.rjust(pad_size)
        print('Job', jobindex, padded_msg + ':\t', path.as_posix())
        return None

    @classmethod
    def which(cls, command: str) -> Path:
        """ Find command in $PATH or get fullpath. """

        program: str | None = shutil.which(command)
        path: Path
        if program:
            path = Path(program)
        else:
            path = fullpath(command)
            if not path.exists():
                raise FileNotFoundError(path)
            elif not path.is_file():
                raise OSError('Path is not a file:', path)
            elif not os.access(path, os.X_OK):
                raise PermissionError(path)
        return path

    @classmethod
    def existing_dir(cls, path: str | None) -> Path | None:
        """ Check if path is an existing dir and get fullpath. """

        if path:
            dir: Path = fullpath(path)
            if not dir.exists():
                raise FileNotFoundError(dir)
            elif not dir.is_dir():
                raise NotADirectoryError(dir)
            elif not os.access(dir, os.W_OK):
                raise PermissionError(dir)
            return dir
        else:
            return None

    @classmethod
    def match_type(cls, path: Path) -> str | None:
        """ Check and get supported file type of paths extension. """

        if path.suffix:
            suffix: str = path.suffix.lower().lstrip('.')
            for type, extensions in App.types.items():
                if suffix in extensions:
                    return type
        return None


class File:
    """ Transforms a Path to File object with additional attributes. """

    def __init__(self, input: Path, dir: Path | None = None):
        """ Constructs File attributes. """

        self.input: Path = input
        if dir:
            output = dir.joinpath(input.name)
        else:
            output = input
        self.output: Path = output.with_suffix('.chd')
        self.tempdir: Path | None = None
        self.type: str | None = App.match_type(self.input)
        if self.type == 'archive':
            self.tempdir = self.construct_tempdir()

    def construct_tempdir(self) -> Path:
        """ Build path for temporary folder. """

        name: str = f'.{self.input.name}_{File.random_str()}'
        return self.output.with_name(name)

    @classmethod
    def random_str(cls, length: int = 10) -> str:
        """ Build random string consisting of uppercase chars and digits. """

        population = string.ascii_uppercase + string.digits
        return ''.join(random.choices(population, k=length))


def fullpath(file: str) -> Path:
    """ Transform str to path, resolve env vars, tilde and make absolute. """

    expandedfile: str = os.path.expandvars(file)
    path: Path = Path(expandedfile).expanduser().resolve()
    return path


def cpucount() -> int:
    """ Get actual count of CPU number. """

    count = os.cpu_count()
    if count is None:
        return 0
    else:
        return int(count + 1)


def get_stdin_lines() -> list[str]:
    """ Read each line from stdin and split by newline char. """

    stdin: list[str] = []
    for line in sys.stdin.readlines():
        if line:
            stdin.extend(line.split('\n'))
    stdin_set: set[str] = set(stdin)
    stdin_set.discard('')
    return list(stdin_set)


def parse_arguments(args: list[str] | None = None) -> Argparse:
    """ Programs CLI options. """

    parser = argparse.ArgumentParser(
        description=('Convert game ISO and archives to CD CHD for emulation.'),
        epilog=('Copyright © 2022 Tuncay D. '
                '<https://github.com/thingsiplay/tochd>')
    )

    parser.add_argument(
        'file',
        default=[],
        nargs='*',
        help=('input multiple files or folders with ISOs or archives, all '
              'supported files from a given folder are processed, in addition '
              'use option dash "-" to read files from stdin for each line, '
              'note: option "--" indicates everything after it is a file, '
              'even those starting with a "-"')
    )

    parser.add_argument(
        '--version',
        default=False,
        action='store_true',
        help='print version and exit'
    )

    parser.add_argument(
        '--list-examples',
        default=False,
        action='store_true',
        help='print usage examples and exit'
    )

    parser.add_argument(
        '--list-formats',
        default=False,
        action='store_true',
        help='list all supported filetypes and extensions and exit'
    )

    parser.add_argument(
        '--list-programs',
        default=False,
        action='store_true',
        help='list name and path of all found programs and exit'
    )

    parser.add_argument(
        '--7z',
        dest='p7z',
        metavar='CMD',
        default='7z',
        help='change path or command name of 7z program'
    )

    parser.add_argument(
        '--chdman',
        metavar='CMD',
        default='chdman',
        help='change path or command name of chdman program'
    )

    parser.add_argument(
        '-d', '--output-dir',
        metavar='DIR',
        default=None,
        help=('destination path to an existing directory to save the CHD file '
              'under, the temporary subfolder will be created here too, '
              'defaults to each input files original directory')
    )

    parser.add_argument(
        '-R', '--no-rename',
        default=False,
        action='store_true',
        help=('disable automatic renaming for CHD files that were build from '
              'archives, no test for "if file already exists" can be provided '
              'beforehand, only applicable to archive sources')
    )

    parser.add_argument(
        '-p', '--parallel',
        default=False,
        action='store_true',
        help=('activate multithreading to process multiple files at the same '
              'time, causes supressing the output of sub commands and '
              'automates user input as much as possible, set number of '
              'threads with option "-t"')
    )

    parser.add_argument(
        '-t', '--threads',
        metavar='NUM',
        default=2,
        type=int,
        choices=range(0, cpucount()),
        help=('max number of threaded processes to run in parallel, requires '
              'option "-p" to be active, "0" is count of all cores '
              f'(available: {os.cpu_count()}), defaults to "2"')
    )

    parser.add_argument(
        '-c', '--chdprocessors',
        metavar='NUM',
        default=0,
        type=int,
        choices=range(0, cpucount()),
        help=('limit the number of processor cores to utilize during '
              'compression of the CHD files with "chdman", 0 will not limit '
              f'the cores (available: {os.cpu_count()}), defaults to "0"')
    )

    parser.add_argument(
        '-f', '--fast',
        default=False,
        action='store_true',
        help=('no compression for CHD files with "chdman", allows for quickly '
              'testing creation of files')
    )

    parser.add_argument(
        '-q', '--quiet',
        default=False,
        action='store_true',
        help=('supress output from external programs, print job messages '
              'only, automate user input if needed')
    )

    parser.add_argument(
        '-E', '--emergency-break',
        default=False,
        action='store_true',
        help=('Ctrl+c (SIGINT) will stop execution of script immadiately '
              'with exit code 255, without this option the script defaults to '
              'canceling current job process properly and continue with next '
              'job process')
    )

    parser.add_argument(
        '-X', '--dry-run',
        default=False,
        action='store_true',
        help=('do not execute the conversion or extraction commands, list the '
              'jobs and files only that would have been processed')
    )

    parser.add_argument(
        '-',
        dest='stdin',
        default=False,
        action='store_true',
        help=('read files from stdin for each line, additionally break up '
              'lines containing any newline character "\\n"')
    )

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    """ Run the application. """

    def example(arguments: str, stdin: str | None = None):
        """ Template to build example line for --list-examples option. """

        if stdin:
            stdin = f'{stdin} | '
        else:
            stdin = ''
        return f'$ {stdin}{app.name} {arguments}'

    def signal_SIGINT(*args):
        """ Shutdown clean and gracefully on Ctrl+c keyboard interruption. """

        app.clean_pending_temp_list
        try:
            sys.exit(3)
        except SystemExit:
            if app.emergency_break:
                sys.exit(255)

    def signal_SIGTERM(*args):
        """ Forcefully shutdown on TERM signal. May leave unfinished files. """

        app.clean_pending_temp_list
        sys.exit(255)

    app: App = App(parse_arguments(args))

    atexit.register(signal_SIGINT)
    signal.signal(signal.SIGTERM, signal_SIGTERM)
    signal.signal(signal.SIGINT, signal_SIGINT)

    if app.print_version:
        print(f'{app.name} v{app.version}')
        return 0
    elif app.list_programs:
        for name, path in app.programs.items():
            print(name + ':', path.as_posix())
        return 0
    elif app.list_formats:
        for filetype, extension in app.types.items():
            print(filetype + ':', ', '.join(extension))
        return 0
    elif app.list_examples:
        print(example('--help'))
        print(example('.'))
        print(example('~/Downloads'))
        print(example('-q -- *'))
        print(example("-pf ~/Downloads | grep 'Completed:' | grep -Eo '/.+$'"))
        print(example('-d ~/converted -- *.7z > tochd.log'))
        print(example('-', stdin='ls -1'))
        return 0

    app.convert(app.files, startindex=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
