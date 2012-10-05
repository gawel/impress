#!/bin/sh
git clone git@github.com:gawel/impress.git pages
cd pages
git checkout gh-pages
rm index.html
../bin/impress -i ../docs/index.rst -o .
git add -A
git commit -m "update docs"
git push origin gh-pages
cd ..
rm -Rf pages
