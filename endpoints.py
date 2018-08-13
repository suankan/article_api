from flask_restful import reqparse, abort, Resource
from articles import Article, Articles
import jsonpickle

class MyResource(Resource):
    '''
    This is a base class that defines:
     - Main storage service articles which is a simple Python dictionary.
     - All nodes in incoming JSON structure that we are interested in.
     - Helper functions that can be used by all childs of this class.
    '''

    storage = Articles()

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('date', type=str)
    parser.add_argument('body', type=str)
    parser.add_argument('tags', type=str, action='append')

    def abort_if_article_doesnt_exist(self, id):
        '''Returns HTTP 404 error in case if a given article id key does not exist in articles dict.
        '''
        if not self.storage.article_exists(id):
            abort(404, message=f'Article {id} does not exist')

    def abort_if_article_aleady_exist(self, id):
        '''Returns HTTP 404 error in case if a given article id key already exists in articles dict.
        '''
        if self.storage.article_exists(id):
            abort(404, message=f'Article {id} already exists')

class ArticleRes(MyResource):
    '''This class defines operations on endpoint /articles/{id}
    E.g. GET, PUT, DELETE ...
    ''' 

    def get(self, id):
        '''Endpoint GET /articles/{id} should return JSON representation 
        of the article with a given id
        '''
        self.abort_if_article_doesnt_exist(id)
        result = self.storage.get(id)
        return jsonpickle.encode(result, unpicklable=False)

class ArticleListRes(MyResource):
    '''
    This class defines operations on endpoint /articles
    '''

    def get(self):
        result = dict(self.storage.get_all())
        return jsonpickle.encode(result, unpicklable=False)

    def post(self):
        '''Endpoint POST /articles should handle the receipt of some article 
        data in json format, and store it within the service.
        '''
        args = self.parser.parse_args()

        self.abort_if_article_aleady_exist(args['id'])

        article = Article(args['id'], args['title'], args['date'], args['body'], args['tags'])

        result = self.storage.add(article)
        return jsonpickle.encode(result, unpicklable=False)

class TagsRes(MyResource):
    '''This class defines operations on endpoint /tags/{tag_name}/{date}
    '''

    def get(self, tag_name, date):

        result = self.storage.get_tag_summary(tag_name, date)
        return jsonpickle.encode(result, unpicklable=False)


