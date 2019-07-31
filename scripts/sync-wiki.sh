#!/bin/bash

# Sync GitHub and GitLab wikis while allowing edits on both.

readonly github_addr=git@github.com:dreamer/steam-dos.wiki.git
readonly gitlab_addr=git@gitlab.com:luxtorpeda/boxtron.wiki.git
readonly repo_name=boxtron.wiki

git_cmd () {
	git -C "../$repo_name" "$@"
}

set -x

cd "$(git rev-parse --show-toplevel)" || exit
if [ ! -d "../$repo_name" ] ; then
	git -C ".." clone "$github_addr" "$repo_name"
	git_cmd remote add gitlab "$gitlab_addr"
fi

git_cmd fetch --all
git_cmd pull
if ! git_cmd merge gitlab/master ; then
	echo 'Error: automatic merge failed.'
	exit 1
fi
git_cmd push gitlab master
