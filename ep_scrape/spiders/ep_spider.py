import scrapy

from ep_scrape.items import EpScrapeItem

class EPSpider(scrapy.Spider):
    name = "ep"
    allowed_domains = ["experienceproject.com"]
    start_urls = [
        "http://www.experienceproject.com/sitemap.php?view=g&alpha=v&page=1" #e.g. scrape v1 page
    ]

    # for each submenu 1,2,3 etc..
    def parse(self, response):
        for href in response.xpath('//a[@class = "sitemap_submenu"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_sub_menus)

    # go to each group
    def parse_sub_menus(self, response):
        for href in response.xpath('//div[@class = "content"]//a[starts-with(@href, "/groups/")]'):
            url = response.urljoin(href.xpath('@href').extract()[0])
            request = scrapy.Request(url, callback = self.get_story_details) # yield request of redirecting to group links
            yield request
            
    # extract group info and every story and replies
    def get_story_details(self, response):
        if response.url.startswith('http://www.experienceproject.com/groups'):
            for sel in response.xpath('//div[contains(@class,"titled-story-expression")]'):
                full_story_url = sel.xpath('.//div[@class = "content"]//a[@class = "title"]/@href').extract()[0] or sel.xpath('.//div[@class = "content"]//a[@class = "title"]/@href').extract()
                url = response.urljoin(full_story_url)
                item = EpScrapeItem()
                item['heading'] = sel.xpath('.//div[@class = "content"]//a[@class = "title"]/text()').extract()
                item['full_story_link'] = url
                item['author'] = sel.xpath('.//div[@class = "foot"]//span[@class = "member"]//span[@class = "member-username-with-status"]//a[contains(@class,"member-username")]/text()').extract()
                item['author_age'] = sel.xpath('.//div[@class = "foot"]//span[@class="member"]//span[@class = "member-age-gender-abbreviated"]//span[@class="age"]/text()').extract()
                item['author_gender'] = sel.xpath('.//div[@class = "foot"]//span[@class="member"]//span[@class = "member-age-gender-abbreviated"]//span[@class="gender"]/text()').extract()
                item['num_responses'] =  sel.xpath('.//div[@class = "foot"]//span[@class="stats"]//span[@class = "responses"]/text()').extract()
                item['num_likes'] = sel.xpath('.//div[@class = "foot"]//span[@class="stats"]//span[@class="likes"]//span[contains(@class, "like-count")]//span[@class="count"]/text()').extract()
                item['story_date'] = sel.xpath('.//div[@class = "foot"]//span[@class="date"]//span[@class = "model-create-date"]/text()').extract()
                if url:
                    request = scrapy.Request(url, callback = self.get_story_details) # yield request of redirecting to group links
                    request.meta['item'] = item
                    yield request

        if response.url.startswith('http://www.experienceproject.com/stories'):
            item = response.meta['item']
            item['replies'] = []
            item['comments'] = []

            item['full_story'] = response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "content"]//p/text()').extract() or response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "content"]/text()').extract()
            #should be h2 or h1
            item['group_name'] = response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "title"]//div[@class = "title-container"]//h2[@class = "story-top-group-title"]/a/text()').extract() or response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "title"]//div[@class = "title-container"]//h1[@class = "story-top-group-title"]/a/text()').extract()
            item['group_link'] = response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "title"]//div[@class = "title-container"]//h2[@class = "story-top-group-title"]/a/@href').extract() or response.xpath('//div[contains(@class,"story-page-expression")]//div[@class = "expression-content"]//div[@class = "title"]//div[@class = "title-container"]//h1[@class = "story-top-group-title"]/a/@href').extract()

            comment_author_name = './/div[@class = "response-footer"]//span[@class = "member-username-with-status"]//a[contains(@class, "member-username")]/text()'
            comment_author_age = './/div[@class = "response-footer"]//span[@class = "member-age-gender-abbreviated"]//span[@class = "age"]/text()'
            comment_author_gender = './/div[@class = "response-footer"]//span[@class = "member-age-gender-abbreviated"]//span[@class = "gender"]/text()'
            comment_date = './/div[@class = "response-footer"]//span[contains(@class,"model-create-date")]/text()'
            comment_likes = './/div[@class = "response-footer"]//span[contains(@class,"like-count")]//span[@class = "count"]/text()'
            
            for sel in response.xpath('//div[@model-type = "StoryComment"]'):
                comment_id = sel.xpath('@comment-id').extract()
                item['comments'].append({
                    'full_comment': sel.xpath('.//div[@class="comment-content-container"]//div[@class = "response-content"]//p/text()').extract(),
                    'comment_author_name': sel.xpath(comment_author_name).extract(),
                    'comment_author_age': sel.xpath(comment_author_age).extract(),
                    'comment_author_gender': sel.xpath(comment_author_gender).extract(),
                    'comment_date': sel.xpath(comment_date).extract(),
                    'comment_likes': sel.xpath(comment_likes).extract(),
                    'comment_id': comment_id})

                reply = "//div[@class = 'inner-responses']//div[@comment-id = " + str(comment_id[0]) + "]" #"//div[@id = 'inner-responses-StoryComment-" + str(comment_id[0]) + "']//div[@model-type = 'StoryCommentReply']" #//div[@model-type = 'StoryCommentReply']
                for sel in response.xpath(reply):
                    item['replies'].append({ 
                    'reply_comment_id': sel.xpath('@comment-id').extract() ,
                    'full_reply': sel.xpath('.//div[@class = "response-content"]//p/text()').extract(),
                    'reply_author_name': sel.xpath(comment_author_name).extract(),
                    'reply_author_age': sel.xpath(comment_author_age).extract(),
                    'reply_author_gender': sel.xpath(comment_author_gender).extract(),
                    'reply_date': sel.xpath(comment_date).extract(),
                    'reply_likes': sel.xpath(comment_likes).extract(),
                     })
            yield item
            return
            