import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    page_count = 1
    max_pages = 10
    
    def start_requests(self):
        yield scrapy.Request(url='https://lista.mercadolivre.com.br/tenis-corrida-masculino', callback=self.parse)

    def parse(self, response):
        sneakers = response.xpath('//li[@class="ui-search-layout__item"]')

        for sneaker in sneakers: 
            name = sneaker.xpath('.//h2/a/text()').get()
            brand = sneaker.xpath('.//span[@class="ui-search-item__brand-discoverability ui-search-item__group__element"]/text()').get()

            old_price_int = sneaker.xpath('.//s/span[@class="andes-money-amount__fraction"]/text()').get()
            old_price_cents = sneaker.xpath('.//s//span[@class="andes-money-amount__cents andes-money-amount__cents--superscript-16"]/text()').get()

            new_price_int = sneaker.xpath('.//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]//span[@class="andes-money-amount__fraction"]/text()').get()
            new_price_cent = sneaker.xpath('.//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]//span[@class="andes-money-amount__cents andes-money-amount__cents--superscript-24"]/text()').get()

            reviews_rating_number = sneaker.xpath('.//span[@class="ui-search-reviews__rating-number"]/text()').get()
            reviews_amount = sneaker.xpath('.//span[@class="ui-search-reviews__amount"]/text()').get()

            yield {
                'brand': brand if brand else 'None',
                'name': name,
                'old_price_int': old_price_int if old_price_int else 'None',
                'old_price_cents': old_price_cents if old_price_cents else 'None',
                'new_price_int': new_price_int if new_price_int else 'None',
                'new_price_cent': new_price_cent if new_price_cent else 'None',
                'reviews_rating_number': reviews_rating_number if reviews_rating_number else 'None',
                'reviews_amount': reviews_amount if reviews_amount else 'None'
            }
    
        if self.page_count < self.max_pages:
            next_page = response.xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]/a/@href').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)


            
