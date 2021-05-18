# -*- coding:utf-8 -*-
import os
import argparse
import dataclasses
import json
import re
import shutil
import time
import zipfile
from typing import List, Optional

WIN32_PATH_SEP = '\\'
PATH_SEP = '/'
PACKAGE_PATTERN = re.compile(r'^(package( +)(.+);)\n$', re.M)

DEFAULT_SPEC_FILE = 'package.json'
SPEC_FILE_ENCODING = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', help="Output file name.", default='')
parser.add_argument('--spec', '-c', help="Path to package.json", default=DEFAULT_SPEC_FILE)
parser.add_argument('dirname', help="Directory name containing files to pack.")

temp_dir = f'temp_dir_{int(time.time())}'  # Use different dirname each time.


@dataclasses.dataclass
class PackageSpec:
    required_files: List[str]
    remove_package_statement: bool = True


def package(dirname: str,
            spec_file: str,
            output_file: Optional[str] = None):
    if not os.path.isdir(dirname):
        raise ValueError(f"Target directory {dirname} does not exist or not a directory.")

    if DEFAULT_SPEC_FILE == spec_file:
        spec_file = os.path.join(dirname, spec_file)

    with open(spec_file, 'r', encoding=SPEC_FILE_ENCODING) as f:
        kw = json.load(f)
        spec = PackageSpec(**kw)

    os.makedirs(temp_dir, exist_ok=True)
    for name in spec.required_files:
        src = os.path.join(dirname, name)
        rfp = open(src, 'r', encoding=SPEC_FILE_ENCODING)
        content = rfp.read()
        rfp.close()

        if spec.remove_package_statement:
            # Remove leading 'package {package_name};' from each source code file.
            content = PACKAGE_PATTERN.sub('', content, 1)

        dest = os.path.join(temp_dir, name)
        wfp = open(dest, 'w', encoding=SPEC_FILE_ENCODING)
        wfp.write(content)
        wfp.close()

        print(f'Added {src} -> {dest}')

    # Create zip file.
    if not output_file:
        _, name = os.path.split(dirname)
        output_file = f'{name}.zip'

    zfp = zipfile.ZipFile(output_file, 'w')
    for name in spec.required_files:
        path = os.path.join(temp_dir, name)
        zfp.write(path, name)

    zfp.close()
    print(f'Package {output_file} created.')


def cleanup():
    if not os.path.exists(temp_dir):
        return

    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} cleaned.")


if __name__ == '__main__':
    args = parser.parse_args()
    dirname_ = args.dirname.replace(WIN32_PATH_SEP, PATH_SEP)
    dirname_ = dirname_.rstrip('/')

    spec_file_ = args.spec.replace(WIN32_PATH_SEP, PATH_SEP)
    output_file_ = args.output.replace(WIN32_PATH_SEP, PATH_SEP)

    try:
        package(dirname_, spec_file_, output_file_)
    finally:
        cleanup()
