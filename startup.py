import csv
import io

from functools import singledispatch
from itertools import chain
from math import floor, log10
from pathlib import Path
from typing import Protocol, runtime_checkable

_BOM = b'\xef\xbb\xbf'

def get_all_files(parent: Path=Path.cwd()):
    return chain((p for p in parent.iterdir()
                  if p.is_file() and not p.is_symlink()),
                 *(get_all_files(p) for p in parent.iterdir()
                   if p.is_dir() and not p.is_symlink()))

@singledispatch
def read_all_lines(p: Path):
    with p.open() as fp:
        return [s.rstrip() for s in fp]

@read_all_lines.register
def _(filename: str):
    return read_all_lines(Path(filename))

@singledispatch
def has_bom(stm: io.FileIO):
    return stm[:3] == _BOM

@has_bom.register
def _(filename: str):
    with io.FileIO(filename) as fp:
        return has_bom(fp)

@has_bom.register
def _(p: Path):
    with p.open(mode='rb') as fp:
        return fp.read(3) == BOM

@singledispatch
def supports_excel(p: Path):
    return has_bom(p)

@supports_excel.register
def _(filename: str):
    return supports_excel(Path(filename))

# TODO: implement line wrapping, scroll control
def print_numbered(lines: list[str]) -> None:
    number_width = floor(log10(len(lines))) + 2
    format_string = f'{{0:>{number_width}}} {{1}}'
    for i, line in enumerate(lines):
        print(format_string.format(i, line))

def _test():
    ...

if __name__ == '__main__':
    _test()
