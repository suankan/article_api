#!/bin/bash

for i in 0 1 2 3; do
    curl --data "@sample_articles/sample_article_$i.json" -H "Content-Type: application/json" http://127.0.0.1:5000/articles
done
