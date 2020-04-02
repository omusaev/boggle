#!/usr/bin/env bash

: "${ADDR:=changeme}"
: "${PLAYBOOK:=app.yml}"


if [[ $# -gt 0 ]]; then
    PLAYBOOK=$1
fi

#TODO realpath does not exist on macos, "there has to be a better way"
REPO_ROOT="$(realpath "$(dirname "$0")")/../../.."

ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i $ADDR, -u ubuntu --private-key $REPO_ROOT/deploy/terraform/aws/ssh/aws.pem $REPO_ROOT/deploy/ansible/playbooks/$PLAYBOOK
