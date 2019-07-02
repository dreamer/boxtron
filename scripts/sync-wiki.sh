#!/bin/env bash

# Sync GitHub and GitLab wikis while allowing edits on both.

readonly github_addr=git@github.com:dreamer/steam-dos.wiki.git
readonly gitlab_addr=git@gitlab.com:dreamer-tan/steam-dos.wiki.git

set -x

cd "$(git rev-parse --show-toplevel)" || exit
if [ ! -d ../steam-dos.wiki ] ; then
	git -C .. clone "$github_addr"
	git -C ../steam-dos.wiki remote add gitlab "$gitlab_addr"
fi

git -C ../steam-dos.wiki fetch --all
git -C ../steam-dos.wiki pull
if ! git -C ../steam-dos.wiki merge gitlab/master ; then
	echo 'Error: automatic merge failed.'
	exit 1
fi
git -C ../steam-dos.wiki push gitlab master
