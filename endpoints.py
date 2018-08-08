from flask_restful import reqparse, abort, Resource

class MyResource(Resource):
    '''
    This is a base class that defines:
     - Main storage service articles which is a simple Python dictionary.
     - All nodes in incoming JSON structure that we are interested in.
     - Helper functions that can be used by all childs of this class.
    '''

    articles = {}

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('date', type=str)
    parser.add_argument('body', type=str)
    parser.add_argument('tags', type=str, action='append')

    def abort_if_doesnt_exist(self, id):
        '''
        Returns HTTP 404 error in case if a given article id 
        key does not exist in articles dict.
        '''

        if int(id) not in self.articles:
            abort(404, message=f'Article {id} does not exist')

    def abort_if_aleady_exist(self, id):
        '''
        Returns HTTP 404 error in case if a given article id 
        key already exists in articles dict.
        '''

        if int(id) in self.articles:
            abort(404, message=f'Article {id} already exists')

class Articles(MyResource):
    '''
    This class defines operations on endpoint /articles/{id}
    E.g. GET, PUT, DELETE ...
    ''' 

    def get(self, article_id):
        '''
        Endpoint GET /articles/{id} should return the JSON representation 
        of the article.
        '''

        self.abort_if_doesnt_exist(article_id)
        return self.articles[int(article_id)]

class ArticlesList(MyResource):
    '''
    This class defines operations on endpoint /articles
    '''

    def post(self):
        '''
        Endpoint POST /articles should handle the receipt of some article 
        data in json format, and store it within the service.
        '''
        args = self.parser.parse_args()
        
        self.abort_if_aleady_exist(args['id'])

        article = {}
        article['id'] = int(args['id'])
        article['title'] = args['title']
        article['date'] = args['date']
        article['body'] = args['body']
        article['tags'] = args['tags']

        self.articles[article['id']] = article

        return article['id']

class Tags(MyResource):
    '''
    This class defines operations on endpoint /tags/{tagName}/{date}
    '''

    def get(self, tagName, date):
        '''
        Endpoint GET /tags/{tagName}/{date} will return the list of 
        articles that have that tag name on the given date and some 
        summary data about that tag for that day.

        The GET /tag/{tagName}/{date} endpoint should produce the following JSON. Note that the actual url would look like /tags/health/20160922.

        {
            "tag" : "health",
            "count" : 17,
            "articles" : ["1", "7"],
            "related_tags" : ["science", "fitness"]
        }

        The related_tags field contains a list of tags that are on the articles that the current tag is on for the same day. It should not contain duplicates.

        The count field shows the number of tags for the tag for that day.

        The articles field contains a list of ids for the last 10 articles entered for that day.
        '''

        pass      

    
