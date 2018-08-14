# article_api

## Description

This is a Python coding for this task https://ffxblue.github.io/interview-tests/test/article-api/

## Installation and execution instructions

1. Git clone this repo
2. `cd article_api` into the created repo directory
3. Build a docker image via provided Dockerfile 
```
docker build -t article_api .
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
article_api         latest              e9d011492fb7        14 seconds ago      92.1MB
```
4. Run a container with the entire REST API application from the built image
```
docker run -d --rm --name article_api -p 5000:5000 article_api
```
5. Now you are ready to interact with articles_api app. Feel free to compose your own sample JSON files or just use my samples from the `sample_articles` directory. You can also run bash script `add_test_articles.sh` that will quickly send all my sample articles JSONs to the article_api app.
```
./add_test_articles.sh 
"{\"body\": \"some text, potentially containing simple markup about how potato chips are great\", \"date\": \"2016-09-22\", \"id\": 0, \"tags\": [\"science0\", \"fitness0\", \"health\"], \"title\": \"latest science shows that potato chips are better for you than sugar\"}"
"{\"body\": \"some text, potentially containing simple markup about how potato chips are great\", \"date\": \"2016-09-22\", \"id\": 1, \"tags\": [\"science1\", \"health\", \"fitness1\"], \"title\": \"latest science shows that potato chips are better for you than sugar\"}"
"{\"body\": \"some text, potentially containing simple markup about how potato chips are great\", \"date\": \"2016-09-23\", \"id\": 2, \"tags\": [\"science2\", \"health\", \"fitness2\"], \"title\": \"latest science shows that potato chips are better for you than sugar\"}"
"{\"body\": \"some text, potentially containing simple markup about how potato chips are great\", \"date\": \"2016-09-23\", \"id\": 3, \"tags\": [\"science3\", \"fitness3\", \"health\"], \"title\": \"latest science shows that potato chips are better for you than sugar\"}"
```

## Running unit tests

The above Dockerfile creates a minimal python:alpine image (92.1MB) with minimal shell.

1. Run docker image interactively:
```
docker run -it --rm --name article_api -p 5000:5000 article_api sh
/article_api # python --version
Python 3.7.0
/article_api # pwd
/article_api
/article_api # ls -la
total 60
drwxr-xr-x    6 root     root          4096 Aug 14 02:21 .
drwxr-xr-x    1 root     root          4096 Aug 14 02:21 ..
drwxr-xr-x    7 root     root          4096 Aug 14 02:00 .git
-rw-r--r--    1 root     root            36 Aug 13 14:37 .gitignore
drwxr-xr-x    2 root     root          4096 Aug  9 05:23 .vscode
-rw-r--r--    1 root     root           157 Aug 14 02:20 Dockerfile
drwxr-xr-x    2 root     root          4096 Aug 14 01:40 __pycache__
-rwxr-xr-x    1 root     root           164 Aug 14 01:59 add_test_articles.sh
-rw-r--r--    1 root     root           515 Aug 13 04:36 api.py
-rw-r--r--    1 root     root          5537 Aug 14 01:40 articles.py
-rw-r--r--    1 root     root          6116 Aug 14 01:35 articles_test.py
-rw-r--r--    1 root     root          2643 Aug 13 04:36 endpoints.py
drwxr-xr-x    2 root     root          4096 Aug 14 01:58 sample_articles
```

2. Run unit tests:
```
/article_api # python3 articles_test.py -v
test_article_add (__main__.TestArticlesStorage) ... ok
test_article_add_existing (__main__.TestArticlesStorage) ... ok
test_get (__main__.TestArticlesStorage) ... ok
test_get_all (__main__.TestArticlesStorage) ... ok
test_get_article_ids (__main__.TestArticlesStorage) ... ok
test_get_count (__main__.TestArticlesStorage) ... ok
test_get_last_article_ids (__main__.TestArticlesStorage) ... ok
test_get_non_existing (__main__.TestArticlesStorage) ... ok
test_get_related_tags (__main__.TestArticlesStorage) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.031s

OK
```

## Application design description

There is a comprehensive documentation inside of the actual Python code. 
And here is a general design-kind of overview of this app.

### File `articles.py` 
Implements a generic Python module which implements Articles storage and methods for adding, removing, getting items from it as well as some helper complementary functions to geat with search and tags.
`articles` module is UI or API agnostic and its input/output is limited to pure Python objects (e.g. non json-serialised). 

This separation is done in order to:
* Make the whole structure more granular and easy to understand and change
* Simplify Unit testing and limit it to basic Python operations.

`articles` module is fully Unit-tested by `articles_test.py`

### File `endpoints.py` 
Implements Flask-RESTful rest api endpoints classes:
*class ArticleRes(MyResource)*
*class ArticleListRes(MyResource)*
*class TagsRes(MyResource)*

Its functionality:
1. Calls `articles` module and makes conversion (json-encoding) of input/output.
2. Is used by Flask-RESTful application `api.py` which routes API requests to it.
3. Uses `flask_restful` module `reqparse` for parsing user input in rest API calls.

### File `api.py`

1. Bootstraps Flask-RESTful application.
2. Routes REST API calls to the endpoints.

NOTE! There are no unit tests for `endpoints.py` and `api.py`
This has been deliberately left for TODO due to lack of time.

## List of assumptions

1. If we try to add an article which ID already exists in the storage - we don't accept it and return 404 error with explanation message.
2. If we try to get an article which ID does not exist in the storage - we return 404 error with appropriate message.
3. When storing an article, if tags list contains duplicate tags - we discard the duplicates.
4. We are not given with requirements how to implement the storage. OrderedDict is used for storage.
5. Terminology "last 10 articles entered for that day". Naturallty getting the last N articles in a given day sounds like we have to return the last N articles in chronological order. However the original task description specifies article date format without hours, minutes and seconds. To keep it simple, we will assume "last N articles in a given day" as last N articles that have been added to our articles registry in the same order how they were added. If there are less than N articles on a given day then just return the found amount.
6. The task description for generating the tags summary says nothing on whether or not the original tag (which summary is generated for) should exist in the list of related tags. However looking at the example JSON data and example tag summagy we see that the original tag is excluded from the related tags list. Hence we exclude it too.
       
