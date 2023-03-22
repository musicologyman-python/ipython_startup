import csv
import io

from functools import singledispatch
from itertools import chain
from pathlib import Path
from typing import Protocol, runtime_checkable

_BOM = b'\xef\xbb\xbf'

@runtime_checkable
class CsvReaderFactoryProtocol(Protocol):
    def create(fp, *args, **kwargs) -> csv.reader:
        ...

class CsvReaderFactory():
    def create(fp, *args, **kwargs) -> csv.reader:
        return csv.reader(fp, *args, **kwargs)
    
class CsvDictReaderFactory():
    def create(fp, fieldnames, *args, **kwargs) -> csv.reader:
        return csv.DictReader(fp, fieldnames, *args, **kwargs)


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

@singledispatch
def read_csv(p: Path, reader_factory: CsvReaderFactoryProtocol, 
             dialect='excel', transform=tuple, fieldnames=None):
    
    encoding = 'utf-8-sig' if supports_excel(p) else 'utf-8'
    with p.open(encoding=encoding) as fp:
        return [transform(row) for row 
                in reader_factory.create(fp, dialect=dialect)]

@read_csv.register
def _(filename: str, reader_type=csv.reader, dialect='excel', transform=tuple):
    return read_csv(Path(filename), reader_type=reader_type, dialect=dialect,
                    transform=transform)

@singledispatch
def write_csv(p: Path, rows, writer_type=csv.writer, supports_excel=False):
    encoding = 'utf-8-sig' if supports_excel else 'utf-8'
    with p.open(mode='w') as fp:
        writer = writer_type(fp)
        try:
            writer.writeheader()
        except AttributeError:
            ...
        writer.writerows(rows)

def _test():
    ...

if __name__ == '__main__':
    _test()
