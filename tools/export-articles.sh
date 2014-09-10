#!/bin/bash
set -eu
cd $(dirname $0)
PYTHON=python2.7

if [ $# -ne 1 ]
then
    echo "Usage: $0 <zendesk_sub_domain>"
    exit 1
fi

domain=$1

echo ">>> Generating site map..."
articles=$($PYTHON print-sitemap.py $domain | \
    grep article | \
    awk -F' ' '{print $2}')

output_directory=export-$domain
rm -rf $output_directory && mkdir -p $output_directory

for article in $articles
do
    echo ">>> Exporting article #$article..."
    output_file=$output_directory/$article.html
    $PYTHON print-article.py $domain $article > $output_file
done
