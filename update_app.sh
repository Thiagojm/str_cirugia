#!/bin/bash

repos=(
  "/home/ubuntu/str_cirurgia"
)

echo ""
echo "Getting latest for" ${#repos[@]} "repositories using git pull"

for repo in "${repos[@]}"
do
  echo ""
  echo "****** Getting latest for" ${repo} "******"
  cd "${repo}"
  git reset --hard
  git pull
  echo "******************************************"
  echo ""
  echo "Restarting systemclt"
  echo ""
done
  sudo systemctl stop str_cirurgia.service
  sudo systemctl start str_cirurgia.service
  sudo systemctl status str_cirurgia.service