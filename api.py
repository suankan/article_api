'''
This is a Flask-RESTful app that implements API endpoints:

POST /articles
GET /articles/{id}
GET /tags/{tagName}/{date}
'''

from flask import Flask
from flask_restful import Api
import endpoints 

app = Flask(__name__)
api = Api(app)

api.add_resource(endpoints.ArticlesList, '/articles')
api.add_resource(endpoints.Articles, '/articles/<int:article_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
