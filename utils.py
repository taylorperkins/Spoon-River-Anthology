import os
import fnmatch
import re


def remove_ascii(line):
    return re.sub(r'[\x90-\x99]', '', line)


def read_cleaned_text(base_dir):
    for file_name in os.listdir(base_dir):
        if fnmatch.fnmatch(file_name, '*_cleaned_poem.txt'):
            with open(f'{base_dir}{file_name}', 'r+', encoding="utf-8") as f:
                poem = [remove_ascii(line) for line in f.read().splitlines()]

                yield poem
