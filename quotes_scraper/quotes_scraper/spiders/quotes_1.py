import scrapy

# Titulo = //h1/a/text() # titulo de la web
# citas = //span[@class="text" and @itemprop ="text"]/text()
# top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href

'/page/2/'
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    # atributo custom para guardar el formato json de forma automatica con los comandos 
    # en la terminal 
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }


    def parse_only_quotes(self, response, **kwargs): # ** se usa para desempaquetar el diccionario en esta funcion
        if kwargs: # aqui se existe kwargs se guarda el diccionario en la variable quotes
            quotes = kwargs['quotes']
        # las citas de la primera y de la segunda pagina esta combinadas aqui:
        quotes.extend(response.xpath('//span[@class="text" and @itemprop ="text"]/text()').extract()) 

        # en este bloque llamamos lo del tercer link en adelante
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link: 
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs = {'quotes': quotes}) 
        else: # con este else y yield exportamos todas las citas a este diccionario, cuando ya no existan mas links
            yield{
                'quotes': quotes
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').extract()
        quotes = response.xpath('//span[@class="text" and @itemprop ="text"]/text()').extract()
        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').extract()

        # aqui transformams a parse en un generador con el keyword yield
        # yield lo que hace es un return parcial de datos, devolvemos un diccionario 
        # sin cortar con la ejecucion de la funcion parse 
        yield {
            'title': title,
            'top_ten_tags': top_ten_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link: #aqui le decimos a scrapy que sigua todos los links del boton next hasta el ultimo
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs = {'quotes': quotes}) #callback ejecuta toda la funcion parse en cada pagina hasta la ultima 
            # cb_kwargs es keyword arguments, es un diccionario en el cual yo le paso argumentos a mi otra funcion. 'quotes' donde tengo almacenada las citas de la primea pagina, 
            # quotes se le pasa al metodo de la funcion only_quotes 



        """ Para ejecutar este spider en consola utilizamos este comando con el nombre
        del archivo que yo quiera darle, puede ser json para front-end or 
        csv para analizis de datos o cualquiera que se requiera
        llamamos el spider con el comando:
        scrapy crawl quotes -o quotes.json 
        -o quiere decir output + el nombre del archivo + el formato que escoja"""

        # para eliminar el archivo y crear otro mismo con resultados renovados 
        # sin necesidad de hacerlo manualmente:
        # rm quotes.json && scrapy crawl quotes -o quotes.json
        # y en windows: 
        # del quotes.json && scrapy crawl quotes -o quotes.json