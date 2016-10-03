# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EpScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #author friends
    heading = scrapy.Field()
    full_story_link = scrapy.Field()
    author = scrapy.Field()
    author_age = scrapy.Field()
    author_gender = scrapy.Field()
    num_responses = scrapy.Field()
    num_likes = scrapy.Field()
    story_date = scrapy.Field()
    group_link = scrapy.Field()
    group_name = scrapy.Field()
    full_story = scrapy.Field()
    replies = scrapy.Field()
    comments = scrapy.Field()
    full_story = scrapy.Field()
    full_comment = scrapy.Field()
    comment_author_name = scrapy.Field()
    comment_author_age = scrapy.Field()
    comment_author_gender = scrapy.Field()
    comment_date = scrapy.Field()
    comment_likes = scrapy.Field()
    comment_id = scrapy.Field()
    full_reply = scrapy.Field()

    pass
