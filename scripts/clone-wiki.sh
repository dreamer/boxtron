#!/bin/env bash
git -C .. clone git@github.com:dreamer/steam-dos.wiki.git
git -C ../steam-dos.wiki remote add gitlab git@gitlab.com:dreamer-tan/steam-dos.wiki.git
git -C ../steam-dos.wiki fetch --all
