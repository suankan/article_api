'''
REST API for three endpoints.

The first endpoint, POST /articles should handle the receipt of some article data in json format, and store it within the service.

The second endpoint GET /articles/{id} should return the JSON representation of the article.

The final endpoint, GET /tags/{tagName}/{date} will return the list of articles that have that tag name on the given date and some summary data about that tag for that day.

An article has the following attributes id, title, date, body, and list of tags. for example:

{
  "id": "1",
  "title": "latest science shows that potato chips are better for you than sugar",
  "date" : "2016-09-22",
  "body" : "some text, potentially containing simple markup about how potato chips are great",
  "tags" : ["health", "fitness", "science"]
}
The GET /tag/{tagName}/{date} endpoint should produce the following JSON. Note that the actual url would look like /tags/health/20160922.

{
  "tag" : "health",
  "count" : 17,
    "articles" :
      [
        "1",
        "7"
      ],
    "related_tags" :
      [
        "science",
        "fitness"
      ]
}
The related_tags field contains a list of tags that are on the articles that the current tag is on for the same day. It should not contain duplicates.

The count field shows the number of tags for the tag for that day.

The articles field contains a list of ids for the last 10 articles entered for that day.
'''

from flask import Flask
from flask_restful import Api
import endpoints 

app = Flask(__name__)
api = Api(app)

api.add_resource(endpoints.ArticlesList, '/articles')
api.add_resource(endpoints.Articles, '/articles/<article_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
