import scrapy

# Titulo = //h1/a/text() # titulo de la web
# citas = //span[@class="text" and @itemprop ="text"]/text()
# top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href
# author = //small[@class="author" and @itemprop="author"]/text()


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']
    # atributo custom para guardar el formato json de forma automatica con los comandos 
    # en la terminal 
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24, # PETICIONES A SCRAPY A LA VEZ, EN ESTE CASO 24
        'MEMUSAGE_LIMIT_MB': 2048, # cantidad de memoria RAM que le permitimos a scrapy
        'MEMUSAGE_NOTIFY_MAIL': ['david.784@outlook.com'], #email de notificacion en caso de superar el limite de MB
        'ROBOTSTXT_OBEY': True, #decirle si obedece o no al archivo robots.txt
        'USER_AGENT': 'VitO', # dejar el nombre de quien hizo estas peticiones en lugar de chrome, firefox etc.
        'FEED_EXPORT_ENCODING': 'utf-8' # caracteres especiales de manera correcta
    }


    def parse_only_quotes(self, response, **kwargs): # ** se usa para desempaquetar el diccionario en esta funcion
        if kwargs: # aqui se existe kwargs se guarda el diccionario en la variable quotes
            quotes = kwargs['quotes']
            authors = kwargs['authors']
        # las citas de la primera y de la segunda pagina esta combinadas aqui:
        quotes.extend(response.xpath('//span[@class="text" and @itemprop ="text"]/text()').extract()) 
        authors.extend(response.xpath('//small[@class="author" and @itemprop="author"]/text()').extract())

        # en este bloque llamamos lo del tercer link en adelante
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link: 
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs = {'quotes': quotes, 'authors': authors}) 
        else: # con este else y yield exportamos todas las citas a este diccionario, cuando ya no existan mas links
            yield{
                'quotes': list(zip(quotes, authors))
            }
         

    def parse(self, response):
        title = response.xpath('//h1/a/text()').extract()
        quotes = response.xpath('//span[@class="text" and @itemprop ="text"]/text()').extract()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').extract()
        authors = response.xpath('//small[@class="author" and @itemprop="author"]/text()').extract()

        # Si existe dentro de la ejecución de este spider un atributo de nombre top lo voy a guardar en mi variable top. 
        # Si no se envía el atributo en la ejecución se guarda None en top
        top = getattr(self, 'top', None) 
        if top:
            top = int(top) # extraer el numero de tags
            top_tags = top_tags[:top] # apartir de ese numero hacemos slicing 
        # comando en la terminal: scrapy crawl quotes -a top= valor que yo quiera

        # aqui transformams a parse en un generador con el keyword yield
        # yield lo que hace es un return parcial de datos, devolvemos un diccionario 
        # sin cortar con la ejecucion de la funcion parse 
        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link: #aqui le decimos a scrapy que sigua todos los links del boton next hasta el ultimo
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs = {'quotes': quotes, 'authors': authors}) #callback ejecuta toda la funcion parse en cada pagina hasta la ultima 
            # cb_kwargs es keyword arguments, es un diccionario en el cual yo le paso argumentos a mi otra funcion. 'quotes' donde tengo almacenada las citas de la primea pagina, 
            # quotes se le pasa al metodo de la funcion only_quotes 



# """ Para ejecutar este spider en consola utilizamos este comando con el nombre 
# del archivo que yo quiera darle, puede ser json para front-end or 
# csv para analizis de datos o cualquiera que se requiera
# llamamos el spider con el comando:
# scrapy crawl quotes -o quotes.json 
# -o quiere decir output + el nombre del archivo + el formato que escoja"""

# para eliminar el archivo y crear otro mismo con resultados renovados 
# sin necesidad de hacerlo manualmente:
# rm quotes.json && scrapy crawl quotes -o quotes.json
# y en windows: 
# del quotes.json && scrapy crawl quotes -o quotes.json