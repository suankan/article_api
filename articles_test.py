'''
Unit tests for articles modules
'''

import unittest
from testfixtures import compare
from collections import OrderedDict, namedtuple
from articles import Article, Articles


class TestArticlesStorage(unittest.TestCase):
    '''
    Tests for Articles module.
    '''

    def setup_test(self):
        '''
        Make ourselves a way to quickly setup articles storage.
        '''

        self.article_0 = Article(
            0,
            "Some title 0",
            "2016-09-22",
            "Some body text 0",
            ['tag0', 'tag1', 'tag2', 'tag3']
        )

        self.article_1 = Article(
            1,
            "Some title 1",
            "2016-09-22",
            "Some body text 1",
            ['tag0', 'tag4', 'tag5', 'tag6']
        )

        self.article_2 = Article(
            2,
            "Some title 2",
            "2016-09-23",
            "Some body text 2",
            ['tag0', 'tag1', 'tag2', 'tag3']
        )

        self.article_3 = Article(
            3,
            "Some title 3",
            "2016-09-23",
            "Some body text 3",
            ['tag0', 'tag1', 'tag2', 'tag3']
        )

        self.article_4 = Article(
            4,
            "Some title 4",
            "2016-09-23",
            "Some body text 4",
            ['tag0', 'tag1', 'tag2', 'tag3']
        )

        self.articles = Articles()

    def teardown_test(self):
        self.articles = None

    def test_article_add(self):
        '''
        Test function Articles.add() when it successfully adds a new article.
        '''

        # Setup test
        self.setup_test()

        result = self.articles.add(self.article_0)
        compare(self.article_0, result)

        # Teardown test
        self.teardown_test()

    def test_article_add_existing(self):
        '''
        Test function Articles.add() throws exception when it fails to add a new article when article with such id already exists.
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)

        with self.assertRaises(Exception):
            self.articles.add(self.article_0)

        # Teardown test
        self.teardown_test()

    def test_get_all(self):
        '''
        Test function Articles.get_all
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)
        self.articles.add(self.article_1)

        expected = OrderedDict()
        expected[0] = self.article_0
        expected[1] = self.article_1

        result = self.articles.get_all()

        compare(expected, result)

        # Teardown test
        self.teardown_test()

    def test_get(self):
        '''
        Test that fucntion Articles.get() resturns correct item
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)

        result = self.articles.get(0)
        compare(result, self.article_0)

        # Teardown test
        self.teardown_test()

    def test_get_non_existing(self):
        '''
        Test that function Articles.get() throws exception when requested item is not there
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)

        with self.assertRaises(Exception):
            self.articles.get(1)

        # Teardown test
        self.teardown_test()

    def test_get_article_ids(self):
        '''
        Test that function Articles.get_last_article_ids(date, n) returns correct list of article ids. 
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)
        self.articles.add(self.article_1)
        self.articles.add(self.article_2)
        self.articles.add(self.article_3)
        self.articles.add(self.article_4)

        result = self.articles.get_article_ids('2016-09-23')
        expected = [2, 3, 4]

        self.assertEqual(result, expected)

        # Teardown test
        self.teardown_test()

    def test_get_count(self):
        '''
        Test that function Articles.get_count(tag_name, date) returns the number of occurrences of the given tag_name across all articles submitted on the given date.
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)
        self.articles.add(self.article_1)
        self.articles.add(self.article_2)
        self.articles.add(self.article_3)
        self.articles.add(self.article_4)

        result = self.articles.get_count('tag0', '2016-09-23')

        self.assertEqual(result, 3)

        # Teardown test
        self.teardown_test()

    def test_get_related_tags(self):
        '''
        Test that function Articles.get_related_tags(tag_name, date) returns the list of tags that are on the articles that the current tag is on for the same day.
        '''

        # Setup test
        self.setup_test()
        self.articles.add(self.article_0)
        self.articles.add(self.article_1)
        self.articles.add(self.article_2)
        self.articles.add(self.article_3)
        self.articles.add(self.article_4)

        result = self.articles.get_related_tags('tag0', '2016-09-22')
        result.sort()
        expected = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6']
        expected.sort()

        self.assertEqual(result, expected)

        # Teardown test
        self.teardown_test()


if __name__ == '__main__':
    unittest.main()