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
  rm my_pdf.pdf
  git pull
  echo "******************************************"
  echo ""
  echo "Restarting systemclt"
  echo ""
done
  sudo systemctl stop str-cirurgia.service
  sudo systemctl start str-cirurgia.service
  sudo systemctl status str-cirurgia.service