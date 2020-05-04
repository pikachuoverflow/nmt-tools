#!/usr/bin/env python3

import argparse
import sys
import re

metrics_ex = [
    "Size:", "KernelPageSize:", "MMUPageSize:", "Rss:", "Pss:", "Shared_Clean:", "Shared_Dirty:",
    "Private_Clean:", "Private_Dirty:", "Referenced:", "Anonymous:", "LazyFree:", "AnonHugePages:",
    "ShmemPmdMapped:", "FilePmdMapped:", "Shared_Hugetlb:", "Private_Hugetlb:", "Swap:", "SwapPss:", "Locked:"
]

metrics = ["Shared_Clean:", "Shared_Dirty:", "Shared_Hugetlb:",
           "Private_Clean:", "Private_Dirty:", "Private_Hugetlb:", 'Rss:', 'Pss:']


def parse_file(file_name):
    values = {}
    for metric in metrics:
        values[metric] = 0

    with open(file_name, 'r') as f:
        for line in f:
            for metric in metrics:
                if line.startswith(metric):
                    values[metric] += extract_value(line)

    for k, v in sorted(values.items()):
        print('{} {}'.format(k, v))


def extract_value(line):
    kb = re.findall('\d+', line)
    if len(kb) > 0:
        return int(kb.pop())
    else:
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="smaps parser")
    parser.add_argument('-p', '--pid', help='PID')
    parser.add_argument('-f', '--file', help='path to smaps file')
    args = parser.parse_args()

    if args.pid is not None:
        parse_file('/proc/{}/smaps'.format(args.pid))
    elif args.file is not None:
        parse_file(args.file)
    else:
        parser.print_usage()
