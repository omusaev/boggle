#!/usr/bin/env bash

REPO_ROOT="$(realpath "$(dirname "$0")")/../../.."

docker build -f $REPO_ROOT/deploy/images/nginx/Dockerfile -t boggle-nginx $REPO_ROOT