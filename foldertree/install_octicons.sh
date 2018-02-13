#!/bin/sh

set -xe
version="7.1.0"
fname="v${version}.zip"
DIR="octicons"

wget https://github.com/primer/octicons/archive/${fname}
unzip ${fname}
rm ${fname}
mv ${DIR}-${version}/lib/svg ./svg
rm -r ${DIR}-${version}
mv svg ${DIR}
wget https://cdn.travis-ci.org/images/favicon-c566132d45ab1a9bcae64d8d90e4378a.svg -O ${DIR}/travis.svg
wget https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg -O ${DIR}/python.svg

FILES=${DIR}/*
for f in $FILES
do
    inkscape -z -e ${f%%.*}.png -w 200 -h 200 ${f}
    rm ${f}
done
