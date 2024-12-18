#!/usr/bin/python

# Validate the format of all the .txt files because its fiddly...

import os


def _emit_error(ent, error, line):
    if len(line) > 50:
        line = line[:50] + '...'
    print(f'{ent:25} {error:55} {line}')


if __name__ == '__main__':
    all = []

    for ent in os.listdir('.'):
        if not ent.endswith('.txt'):
            continue

        warnings = 0
        with open(ent) as f:
            if ent == 'all.txt':
                continue

            line = f.readline().rstrip()
            if line != '#separator:semicolon':
                _emit_error(ent, 'first line is not "#separator:semicolon"', line)
                warnings += 1

            line = f.readline().rstrip()
            if line != '#html:false':
                _emit_error(ent, 'second line is not "#html:false"', line)
                warnings += 1

            for line in f.readlines():
                line = line.rstrip()
                if line.startswith('#'):
                    continue

                if line.find(';') == -1:
                    _emit_error(ent, 'missing field separator', line)
                    warnings += 1

                elif len(line.split(';')) > 2:
                    _emit_error(
                        ent,
                        'too many field separators, do not use semicolons',
                        line)
                    warnings += 1

                elif line.find('; ') != -1:
                    _emit_error(ent, 'whitespace after field separator', line)
                    warnings += 1

                else:
                    all.append(line)

        if warnings > 0:
            print(f'>>> {warnings} warnings for file')
            print()

        else:
            with open('all.txt', 'w') as f:
                f.write('#separator:semicolon\n')
                f.write('#html:false\n')
                for line in all:
                    f.write(f'{line}\n')