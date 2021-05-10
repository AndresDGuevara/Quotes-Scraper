import scrapy

# Titulo = //h1/a/text() # titulo de la web
# citas = //span[@class="text" and @itemprop ="text"]/text()
# top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()

class QuotesSpider(scrapy.Spider):
    name = 'citas'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response): # parse es analizar un archivo para extraer informacion valiosa a partir de el
        print('*' * 10)
        print('\n\n\n')
        
        title = response.xpath('//h1/a/text()').extract()
        print(f'Titulo: {title}')
        print('\n\n\n')

        citas = response.xpath('//span[@class="text" and @itemprop ="text"]/text()').extract()
        print('Citas: ')
        for citas in citas:
            print(f'- {citas}')
        print('\n\n\n')

        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').extract()
        print('Top Ten Tags: ')
        for tag in top_ten_tags: # ciclo for para ver todo de manera grafica
            print(f'- {tag}')

        #print(response.status, response.headers)
        print('\n\n\n')
        print('*' * 10)

""" Este program Imprime el resultado en consola pero no lo guarda. """
        
