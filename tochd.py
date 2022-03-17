#!/bin/env python3

import sys
import atexit
import argparse
import multiprocessing
import subprocess
import shutil
import pathlib
import os.path
import random
import string
import re


def APP(var=None):
    META = {
            # Filename of current program.
            'name': fullpath(sys.argv[0]).stem,
            # Program version.
            'version': '0.5',
    }
    if var:
        return META[var]
    else:
        return META


# Test if the path is an iso file.
def is_iso(path=None):
    ext = ['iso', 'cue', 'gdi']
    if path is None:
        return ext
    suffix = path.suffix.lower().lstrip('.')
    if suffix in ext:
        return True
    else:
        return False


# Test if the path is an archive file.
def is_archive(path=None):
    ext = ['7z', 'zip', 'gz', 'gzip', 'bz2', 'bzip2', 'rar', 'tar']
    if path is None:
        return ext
    suffix = path.suffix.lower().lstrip('.')
    if suffix in ext:
        return True
    else:
        return False

# Checks if the archive file contains has any files that can be converted.
def archive_contains_supported_files(path):
    command = []
    command.append(shutil.which('7z'))
    command.append('l')
    command.append('-slt')
    command.append(path.as_posix())
    completed = subprocess.run(command, capture_output=True, text=True)
    ext = '|'.join(is_iso())
    return re.search(r'Path = .*\.(' + ext + ')', completed.stdout)


# Converts the input file, either an iso or an archive, into a .chd file.  It
# will not process further if the goal file already exists.
def convert(path, destdir, index, capture_output=False, chdprocessors=0,
        rename=False):
    if destdir:
        if pathlib.Path(destdir / path.name).with_suffix('.chd').exists():
            return
    else:
        if path.with_suffix('.chd').exists():
            return
    if is_iso(path):
        convert_iso(path, destdir, index, capture_output, chdprocessors)
    elif is_archive(path):
        convert_archive(path, destdir, index, capture_output, chdprocessors,
                rename)
    return


# Creates a temporary directory to extract the archive into.  From there the
# actual iso file will be converted into .chd, which then is moved to same
# folder where the archive is. 
def convert_archive(path, destdir, index, capture_output=False,
        chdprocessors=0, rename=False):

    if not archive_contains_supported_files(path):
        return
    print(f'Processing {index}: ' + path.as_posix() + ' ...')
    if destdir:
        tempdir = create_tempdir(pathlib.Path(destdir / path.name))
    else:
        tempdir = create_tempdir(path)
    command = []
    command.append(shutil.which('7z'))
    command.append('e')
    if capture_output:
        command.append('-y')
    command.append(path.as_posix())
    command.append('-o' + tempdir.as_posix())
    subprocess.run(command, capture_output=capture_output)
    gdi_files = [*tempdir.glob('*.gdi')]
    if gdi_files:
        files = gdi_files
    else:
        files = [*tempdir.iterdir()]
    outdir = None
    for file in files:
        if is_iso(file):
            outfile = file.with_suffix('.chd')
            command = []
            command.append(shutil.which('chdman'))
            command.append('createcd')
            if chdprocessors:
                command.append('--numprocessors')
                command.append(str(chdprocessors))
            command.append('--input')
            command.append(file.as_posix())
            command.append('--output')
            command.append(outfile.as_posix())
            subprocess.run(command, capture_output=capture_output)
            outdir = outfile.parent.parent
            if rename:
                createdfile = pathlib.Path(outdir / path.name).with_suffix('.chd')
                createdfile.unlink(missing_ok=True)
                shutil.move(outfile.as_posix(), createdfile.as_posix())
            else:
                createdfile = pathlib.Path(outdir.as_posix() + '/' + outfile.name)
                createdfile.unlink(missing_ok=True)
                shutil.move(outfile.as_posix(), createdfile.as_posix())
    shutil.rmtree(tempdir, ignore_errors=True)
    if outdir and createdfile.exists():
        print(f'Finished {index}: ' + createdfile.as_posix())
    return


# Create the chdman command to convert the actual iso file and rename it to
# replace the file extension.
def convert_iso(path, destdir, index, capture_output=False, chdprocessors=0):
    print(f'Processing {index}: ' + path.as_posix() + ' ...')
    outfile = None
    if is_iso(path):
        outfile = path.with_suffix('.chd')
        command = []
        command.append(shutil.which('chdman'))
        command.append('createcd')
        if chdprocessors:
            print(chdprocessors)
            command.append('--numprocessors')
            command.append(str(chdprocessors))
        command.append('--input')
        command.append(path.as_posix())
        command.append('--output')
        if destdir:
            outfile = pathlib.Path(destdir.as_posix() + '/' + outfile.name)
        command.append(outfile.as_posix())
        outfile.unlink(missing_ok=True)
        subprocess.run(command, capture_output=capture_output)
    if outfile and outfile.exists():
        print(f'Finished {index}: ' + outfile.as_posix())
    return


# Create multiple processes, one thread for each file.
# threads: how many threads time can be processed at the same time
# chdprocessors: how many cores should chdman utilize
def parallel_convert(files, destdir, startindex, threads, chdprocessors,
        rename):
    jobs = []
    if threads == 0:
        pool = multiprocessing.Pool()
    else:
        pool = multiprocessing.Pool(processes=threads)
    for index, file in enumerate(files, startindex):
        startindex = index + 1
        pool.apply_async(convert, (file, destdir, index, True,
            chdprocessors, rename,))
    pool.close()
    pool.join()
    return startindex


# Create a temporary folder in same directory as the input file.  It has the
# same name, but adds random characters at the end and a dot at the beginninig,
# to make it hidden.  Temporary folder will be deleted automatically after job
# or script is done, even on Ctrl+D.
def create_tempdir(path):
    tempdir = path.with_suffix('')
    tempdir = tempdir.with_name('.' + tempdir.name + '_' + generate_rand_str())
    tempdir.mkdir()
    atexit.register(shutil.rmtree, tempdir, ignore_errors=True)
    return tempdir


# Create a string with defined length that consists of random characters.
def generate_rand_str(length=4):
    population = string.ascii_uppercase + string.digits
    return ''.join(random.choices(population, k = length))


# Make the path a fullpath with all parts expanded and resolved. 
def fullpath(filename):
    return pathlib.Path(os.path.expandvars(filename)).expanduser().resolve()


# Check if all prerequisities are met.
def check_requirements():

    # Check if program is an executable in the environmental PATH.
    def which(program):
        path = shutil.which(program)
        if not path:
            # print(program + ' is not available.')
            print(f'{program} is not available.')
        return path

    if not which('chdman'):
        return 1
    if not which('7z'):
        return 1
    return 0


# Programs CLI options.
def parse_arguments():
    parser = argparse.ArgumentParser(
            description='Convert ISOs and archives into CD CHD for emulation.',
            epilog='Copyright © 2022 Tuncay D.'
            ' <https://github.com/thingsiplay/tochd>')
    parser.add_argument('file', nargs='*', default=[],
            help='input multiple files or folders with ISOs or archives,'
            ' all supported files from a given folder are processed')
    parser.add_argument('--version', default=False, action='store_true',
            help='print version and exit')
    parser.add_argument('--examples', default=False, action='store_true',
            help='show some usage examples and exit')
    parser.add_argument('--list-formats', default=False, action='store_true',
            help='list supported ISO and archive formats and exit')
    parser.add_argument('--list-apps', default=False, action='store_true',
            help='list path of all found programs and exit')
    parser.add_argument('-p', '--parallel', default=False, action='store_true',
            help='activate multithreading to convert multiple files at the'
            ' same time, set number of threads with option "-t"')
    parser.add_argument('-t', '--threads', metavar='NUM', default=2, type=int,
            choices=range(0, os.cpu_count()),
            help='max number of process threads to start when parallel option'
            ' is active, 0 is count of all cores'
            f' (available: {os.cpu_count()}), defaults to 2')
    parser.add_argument('-c', '--chdprocessors', metavar='NUM', default=0,
            type=int, choices=range(0, os.cpu_count()),
            help='limit the number of processors to utilize during compression'
            ' of the CHD file with chdman, 0 is count of all cores (available:'
            f' {os.cpu_count()}), defaults to 0')
    parser.add_argument('-d', '--output-dir', metavar='DIR', default=None,
            help='destination path to an existing folder, for creating'
            ' temporary and .chd files in, defaults to each input files'
            ' original directory')
    parser.add_argument('-r', '--rename', default=False, action='store_true',
            help='name created .chd files to match their archive filenames its'
            ' based on, only applicable when extracting from archives')
    return parser.parse_args()


# The beginning of the end.
def main():
    args = parse_arguments()

    if args.version:
        print(APP('name') + ' v' + APP('version'))
        return 0
    elif check_requirements():
        return 1
    elif args.list_apps:
        print('Python:', sys.executable)
        print('7z:', shutil.which('7z'))
        print('chdman:', shutil.which('chdman'))
        return 0
    elif args.list_formats:
        print('Supported ISO formats: ' + ', '.join(is_iso()) + '\n'
              'Supported archive formats: ' + ', '.join(is_archive()) + '')
        return 0
    elif args.examples or not args.file:
        print('Usage Examples:'
                '\n'
               f'\n    $ {APP("name")} --help'
               f'\n    $ {APP("name")} .'
               f'\n    $ {APP("name")} -p "~/Downloads/new_isos" "new_cuebins"'
               f'\n    $ {APP("name")} -pt4 -r *.7z'
               f'\n    $ {APP("name")} -d "~/roms/psx" file1.zip file2.iso')
        return 0

    if args.output_dir:
        output_dir = fullpath(args.output_dir)
        if not output_dir.exists() or not output_dir.is_dir():
            print('output-dir must point to an existing folder:', output_dir)
            print('Program terminates.')
            return 2
    else:
        output_dir = None

    # First collect the iso files from all directories and arguments.  Then
    # collect all remaining files, in general archives.  This way an archive
    # with same name of an existing iso or chd file will not be processed.
    iso_files = []
    other_files = []
    for arg in args.file:
        file = fullpath(arg)
        if file.is_file():
            if is_iso(file):
                iso_files.append(file)
            else:
                other_files.append(file)
        elif file.is_dir():
            gdi_files = list(file.glob('*.gdi'))
            if gdi_files:
                for file in gdi_files:
                    other_files.append(file)
            else:
                for file in file.iterdir():
                    if is_iso(file):
                        iso_files.append(file)
                    else:
                        other_files.append(file)

    if args.parallel:
        startindex = 1
        startindex = parallel_convert(iso_files, output_dir, startindex,
                args.threads, args.chdprocessors, args.rename)
        startindex = parallel_convert(other_files, output_dir, startindex,
                args.threads, args.chdprocessors, args.rename)
    else:
        startindex = 1
        for index, file in enumerate(iso_files, startindex):
            startindex = index + 1
            convert(file, output_dir, index, rename=args.rename)
        for index, file in enumerate(other_files, startindex):
            convert(file, output_dir, index, rename=args.rename)
    return 0


if __name__ == '__main__':
    sys.exit(main())
