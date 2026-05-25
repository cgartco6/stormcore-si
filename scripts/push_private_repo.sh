#!/bin/bash

REPO_NAME=$1
USERNAME=$2
TOKEN=$3

git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin https://${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git

git push -u origin main
