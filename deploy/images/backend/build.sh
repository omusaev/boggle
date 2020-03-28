#!/usr/bin/env bash

REPO_ROOT="$(realpath "$(dirname "$0")")/../../.."

docker build -f $REPO_ROOT/deploy/images/backend/Dockerfile -t boggle-backend $REPO_ROOT
