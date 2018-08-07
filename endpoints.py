from flask_restful import reqparse, abort, Resource

class MyResource(Resource):
    articles = {}

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('date', type=str)
    parser.add_argument('body', type=str)
    parser.add_argument('tags', type=str, action='append')

    def abort_if_doesnt_exist(self, id):
        if int(id) not in self.articles:
            abort(404, message=f'Article {id} does not exist')

    def abort_if_aleady_exist(self, id):
        if int(id) in self.articles:
            abort(404, message=f'Article {id} already exists')

class Articles(MyResource):
    
    def get(self, article_id):
        self.abort_if_doesnt_exist(article_id)
        return self.articles[int(article_id)]

class ArticlesList(MyResource):

    def post(self):
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
