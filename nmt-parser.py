#!/usr/bin/env python3

import argparse
import glob
import re
import enum

field_names = [
    'File Name', 'Java Heap', 'Class', 'Thread', 'Code', 'GC', 'Compiler', 'Internal', 'Symbol',
    'Native Memory Tracking', 'Arena Chunk', 'Unknown', 'Total'
]


def parse_amount_kb(line, regex):
    try:
        s1 = re.findall(regex, line)
        return int(re.findall('\d+', s1[0])[0])
    except Exception:
        return ''


def parse_line(line, mode, section, results):
    if section in line:
        if mode == Mode.reserved:
            results[section] = parse_amount_kb(line, 'reserved=\d+KB')
        elif mode == Mode.committed:
            results[section] = parse_amount_kb(line, 'committed=\d+KB')
        else:
            results[section] = None


def parse_file(file_name, mode):
    results = dict()
    with open(file_name, 'r') as f:
        for line in f:
            for field_name in field_names:
                parse_line(line, mode, field_name, results)
    results['File Name'] = file_name
    return results


def normalize(string):
    try:
        return '{:,}'.format(string)
    except ValueError:
        return string


def main(files, mode):
    print(';'.join(field_names))
    for file in files:
        for file_name in glob.glob(file):
            results = parse_file(file_name, mode)
            print(';'.join(normalize(results[key]) for key in field_names))


class Mode(enum.Enum):
    committed = 'committed'
    reserved = 'reserved'

    def __str__(self):
        return self.value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Memory report parser")
    parser.add_argument('-f', '--files', nargs="+", help='Input files', required=True)
    parser.add_argument('-m', '--mode', type=Mode, choices=list(Mode), help='Statistics mode', required=True)
    args = parser.parse_args()
    main(args.files, args.mode)
