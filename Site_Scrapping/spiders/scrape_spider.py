import scrapy

class FunSpider(scrapy.Spider):
    name = "blog_scrape"

    start_urls = [
        'https://blog.scrapinghub.com/'
        ]

    def parse(self,response):
        for url in response.css('.read-more .more-link::attr(href)').getall():
            yield scrapy.Request(url, callback=self.parse_blog_data)
        
        next_link = response.css('.blog-pagination .next-posts-link::attr(href)').get()
        if next_link is not None:
            yield response.follow(next_link, self.parse)

    def parse_blog_data(self,response):
        yield {
                'tite':response.css(".post-header h1 span::text").get(),
                'date':response.css('.post-header .date a::text').get(),
                'author':response.css('.post-header .author a::text').get(),
                'blog_data':response.css('.post-body p::text').getall()

                }
        
