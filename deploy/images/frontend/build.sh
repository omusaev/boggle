#!/usr/bin/env bash

REPO_ROOT="$(realpath "$(dirname "$0")")/../../.."

docker build -f $REPO_ROOT/deploy/images/frontend/Dockerfile -t boggle-frontend $REPO_ROOT
