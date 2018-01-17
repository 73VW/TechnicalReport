#!/bin/sh

set -xe

cd TechnicalReportGenerator
make all

# deploy
test "${TRAVIS_PULL_REQUEST}" = "false" \
  && test "${TRAVIS_BRANCH}" = "master" \
  && ( \
    mkdir build
    cp *.pdf build
    cd build
    git init
    git config user.name "TravisCI"
    git config user.email "travis@he-arc.test"
    git add .
    git commit -m "Deployed to github build branch"
    git push -f -q "https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}" master:build
  ) \
  || echo ":-)"
