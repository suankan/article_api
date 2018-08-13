'''
This is a general python module implementing Articles storage and operations like add, get etc as well as some complementary helper methods.

As a pure Python class, it knows nothing about the format of returned data, no JSON or anything. The reason for that is to allsimplify usage with any arbitrary frontend like API, UI etc.
'''

from collections import OrderedDict, namedtuple
from datetime import datetime

class Article():
    '''
    This class describes an Article object.

    ASSUMPTION:
    If the given tags list contains duplicate tags - we discard the duplicates.
    '''
    def __init__(self, id, title, date, body, tags):
        self.id = int(id)
        self.title = str(title)
        self.date = str(date)
        self.body = str(body)
        self.tags = list(set(tags))

class Articles():
    '''
    This is a storage (registry) of multiple objects.

    ASSUMPTION:
    We are not given with requirements how to implement the storage. However it is said to keep it simple. So we will just use OrderedDict for storage.
    '''

    def __init__(self):
        self.articles = OrderedDict()

    def article_exists(self, id):
        if id in self.articles:
            return True
        else:
            return False

    def add(self, article):
        '''
        This method adds a new article to storage if it does not exist.
        Otherwise throws exception.
        '''

        if self.article_exists(article.id):
            raise Exception(f'Article with id {article.id} already exists')
        else:
            self.articles[article.id] = article
            return self.articles[article.id]

    def get_all(self):
        '''
        Returns all items in storage
        '''
        return self.articles

    def get(self, id = None):
        '''Returns existing article by id if it exists
        Otherwise throws exception.
        '''

        if id == None:
            # return all objects in storage
            return self.articles

        if self.article_exists(id):
            return self.articles[id]
        else:
            raise Exception(f'Article with id {id} does not exist in the storage {self.articles}')

    def get_tag_summary(self, tag_name, date):
        '''Returns dict data about the given tag_name for the given date. 
        
        Arguments:
        tag_name -- tag to generate summary for. 
        date -- datetime object indicating the day to generate summary for.

        Example output: 
        {
            "tag" : "health",
            "count" : 17,
            "articles" : ["1", "7"],
            "related_tags" : ["science", "fitness"]
        }
        '''

        tag_summary = {
            'tag' : tag_name,
            'count' : self.get_count(tag_name, date),
            'articles' : self.get_last_article_ids(date, 10),
            'related_tags' : self.get_related_tags(tag_name, date),
        }

        return tag_summary

    def get_last_article_ids(self, date, n):
        '''Returns the list of last n article ids which were submitted on the given date.

        We have to make an ASSUMPTION here.

        Naturallty getting the last N articles in a given day sounds like
        we have to return the last N articles in chronological order.

        However the original task description specifies article date format without hours, minutes and seconds.

        To keep it simple, we will assume "last N articles in a given day" as last N articles that have been added to our articles registry in the same order how they were added. If there are less than N articles on a given day then just return the found amount.
        '''

        return self.get_article_ids(date)[-n:]

    def get_article_ids(self, date):
        '''Returns the list of article ids which were submitted on the given date.
        '''

        result = []

        for id, article in self.articles.items():
            date1 = datetime.strptime(article.date, '%Y-%m-%d')
            date2 = datetime.strptime(date, '%Y-%m-%d')
            timediff = date1 - date2
            if timediff.days == 0:
                result.append(article.id)

        return result

    def get_related_tags(self, tag_name, date):
        '''Returns the list of tags that are on the articles that the current tag is on for the same day. It should not contain duplicates.

        ASSUMPTION:
        The task description for generating the tags summary says nothing on whether or not the original tag (which summary is generated for) should exist in the list of related tags. 

        However looking at the example JSON data and example tag summagy we see that the original tag is excluded from the related tags list.

        Hence we exclude it too.
        '''

        result = set()

        for id in self.get_article_ids(date):
            tag_name_found = False
            for tag in self.articles[id].tags:
                result.add(tag)
                if tag == tag_name:
                    tag_name_found = True
            
            if not tag_name_found:
                # In this case we discard whatever we added to result.
                result = set()

        result.remove(tag_name)
        return list(result)

    def get_count(self, tag_name, date):
        '''Returns the number of occurrences of the given tag_name across all articles submitted on the given date.
        '''

        count = 0

        for id in self.get_article_ids(date):
            if tag_name in self.articles[id].tags:
                count += 1

        return count


