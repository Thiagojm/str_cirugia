#!/bin/bash

repos=(
  "/home/ubuntu/str_cirurgia"
)

echo ""
echo "Getting latest for" ${#repos[@]} "repositories using pull --rebase"

for repo in "${repos[@]}"
do
  rm my_pdf.pdf
  echo ""
  echo "****** Getting latest for" ${repo} "******"
  cd "${repo}"
  git pull --rebase
  echo "******************************************"
  echo ""
  echo "Restarting systemclt - input sudo password"
  echo ""
done
  sudo systemctl stop str-cirurgia.service
  sudo systemctl start str-cirurgia.service
  sudo systemctl status str-cirurgia.service