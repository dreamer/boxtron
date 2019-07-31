#!/usr/bin/python3

# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import os
import re
import subprocess

REPORTS_PATH = '../boxtron.wiki/Compatibility-reports-(Steam).md'


def go_to_root():
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
    os.chdir(root.strip())


def parse_link(md_link):
    link_pattern = re.compile(r'\[(.*)\]\((.*)\)')
    match = link_pattern.match(md_link)
    return match.group(1), match.group(2)


def list_reports():
    with open(REPORTS_PATH) as reports_md:
        in_table = False
        for line in reports_md:
            if line.startswith('|---'):
                in_table = True
                continue
            if not in_table:
                continue
            yield tuple([x.strip() for x in line.split('|')][1:])


def ellipsis(value, length):
    shorter = list(value)[:length]
    if len(value) > length:
        shorter[-1] = '…'
    return ''.join(shorter)


def main():
    all_games = {}
    names = {}

    for report in list_reports():
        app_link, name, rating, _ver, _desc = report
        app_id, _app_url = parse_link(app_link)
        if app_id not in all_games:
            all_games[app_id] = []
            names[app_id] = name
        all_games[app_id].append(rating.lower())

    num_total = len(all_games)
    num_solid_platinum = 0
    num_silver_or_worse = 0
    for app_id, ratings in all_games.items():
        print('{}\t{:30} {}'.format(app_id, ellipsis(names[app_id], 30),
                                    ratings))
        if all(map(lambda x: x == 'platinum', ratings)):
            num_solid_platinum += 1
        if 'silver' in ratings or \
           'bronze' in ratings or \
           'broken' in ratings:
            num_silver_or_worse += 1

    print()
    print('All games: ', num_total)
    print('Platinum:  ', num_solid_platinum)
    print('Gold:      ', num_total - num_solid_platinum - num_silver_or_worse)
    print('<= Silver: ', num_silver_or_worse)


if __name__ == "__main__":
    go_to_root()
    main()
