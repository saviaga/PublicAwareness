# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash
from lxml import html
import requests
import json

app = Flask(__name__)

def bitly_url(long_url):
    query_params = {'access_token': '14bd2a852998d18016986adc3cb83e2cc9d89e25',
                    'longUrl': long_url}

    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    response = requests.get(endpoint, params=query_params, verify=False)

    data = json.loads((response.content).decode('utf-8'))
    short_url=data['data']['url']
    print (data['data']['url'])

    return short_url


@app.route("/")
def hello():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def imprime():
    opcion1 = request.form['opcion1']
    opcion2 = request.form['opcion2']

    if ((opcion1 == 'SEGOB') and (opcion2 == 'veracruz123')):

        #        return render_template("profile.html",opcion1=opcion1)
        return render_template("notas.html", opcion1=opcion1)
    else:

        return render_template('error.html')


@app.route("/notas", methods=['POST'])
def scrap_note():
    global Link
    global answer
    global Medio
    global a1
    global Titulo_get
    global Texto1
    global Texto
    global news
    global Textos #texto for versiones


    news= {}
    answer = request.form.getlist('myInputs[]')

    for a in answer:
        a1=a
        news[a]=a

    #loop through dictionary
    for x in news:
        print("valores ",news[x])

    print(list(news.keys()))
    # This will create a list of buyers:

    # Inputs = []
    # task_Option = request.form.getlist['myInputs[]']

    task_Option = request.form['taskOption']
    print(task_Option)
    # for tas in task_Option:
    #    print(tas)
    # Link  = request.form['link_id']


    if task_Option == 'XEU':
            try:

                Medio = "XEU"
                for d in news:

                    page = requests.get(news[d])
                    tree = html.fromstring(page.content)

                    Titulo_get = tree.xpath('//div[@class="fgtitulo"]/text()')
                    Titulo_f = Titulo_get[0]
                    Texto = tree.xpath('//div[@class="fatrece"]//text()')
                    Texto = [x.rstrip() for x in Texto]

                    Textof=Texto[1]

                    parrafo = 0
                    for siguiente in Texto:
                        if (parrafo < 5):

                            Textof = Textof + " " + siguiente
                            parrafo = parrafo + 1


                    Fecha_get = tree.xpath('//div[@class="faonce"]/text()')
                    Fecha_get = [x.rstrip() for x in Fecha_get]
                    Fecha_getf = Fecha_get[3][1:]

                    news[d] = [Titulo_f]
                    news[d].append(Textof)
                    news[d].append(Fecha_getf)
                    #it stores the link at the end to retrieve it in html
                    short_url = bitly_url(d)
                    news[d].append(short_url)
                    news[d].append("XEU")

                    print("titulo1 desp 2o append ", news[d])
                    for k in news:
                        print(k)

            except Exception as e:
                mensaje = ("error", e)

    if task_Option == 'veracruzanos':
        try:
            Medio = "Veracruzanos"
            for d in news:
                print("dic value ", news[d])
                page = requests.get(news[d])
                # page.encoding = 'latin-1'
                tree = html.fromstring(page.content)

                Titulo_get = tree.xpath('//h1[@class="entry-title"]/text()')
                Titulo_f = Titulo_get[0]

                Texto = tree.xpath('//div[@class="td-post-content"]//text()')
                Texto = [x.rstrip() for x in Texto]

                Textof = Texto[1]

                parrafo = 0
                for siguiente in Texto:
                    if (parrafo < 7):
                        Textof = Textof + " " + siguiente
                        parrafo = parrafo + 1

                Fecha_get = tree.xpath('//time[@class="entry-date updated td-module-date"]/text()')
                Fecha_getf = Fecha_get[0]


                news[d] = [Titulo_f]
                news[d].append(Textof)
                news[d].append(Fecha_getf)
                short_url = bitly_url(d)
                news[d].append(short_url)
                news[d].append("Veracruzanos.info")

        except Exception as e:
            mensaje = ("error", e)
    if task_Option == 'alcalor':
        try:
            Medio = "Al Calor Político"
            for d in news:
                print("dic value ", news[d])
                page = requests.get(news[d])
                # page.encoding = 'latin-1'
                tree = html.fromstring(page.content)

                Titulo_get = tree.xpath('//div[@id="areasuperior"]/h1/text()')

                Titulo_f = Titulo_get[0]

                Texto = tree.xpath('//div[@class="cuerponota"]//text()')
                Texto = [x.rstrip() for x in Texto]

                Textof = Texto[1]

                parrafo = 0
                for siguiente in Texto:
                    if (parrafo < 3):
                        Textof = Textof + " " + siguiente
                        parrafo = parrafo + 1

                Fecha_get = tree.xpath('//span[@id="lugar"]/text()')
                Fecha_getf = Fecha_get[0]

                news[d] = [Titulo_f]
                news[d].append(Textof)
                news[d].append(Fecha_getf)
                short_url = bitly_url(d)
                news[d].append(short_url)
                news[d].append("Al Calor Político")

        except Exception as e:
            mensaje = ("error", e)
    if task_Option == 'imagen':
        try:
            Medio = "Imagen del Golfo"
            for d in news:
                print("dic value ", news[d])
                page = requests.get(news[d])
                tree = html.fromstring(page.content)

                Titulo_get = tree.xpath('//td[@class="titulonota1"]/text()')
                Titulo_f = Titulo_get[0]

                Texto = tree.xpath('//span[@class="Estilo58 style16"]//text()')
                Texto = [x.rstrip() for x in Texto]

                Textof = Texto[1]

                parrafo=0
                for siguiente in Texto:
                    if (parrafo < 3):
                        Textof = Textof + " " + siguiente
                        parrafo = parrafo + 1

                Fecha_get = tree.xpath('//span[@class="style16 Estilo48 Estilo56"]/text()')
                Fecha_getf = Fecha_get[0]
                fechaf=Fecha_getf.strip("-")

                print("fecha", type(fechaf.encode("utf-8")))
                pedazo = fechaf.split("-")
                anio = pedazo[1]
                mes = pedazo[2]
                diayhora = pedazo[3].split(" ")
                dia = diayhora[0]
                hora = diayhora[1]
                fechaok=dia+ " "+ mes+" " + anio+ " " + hora

                print("fecha ",fechaok)

                news[d] = [Titulo_f]
                news[d].append(Textof)
                news[d].append(fechaok)
                short_url = bitly_url(d)
                news[d].append(short_url)
                news[d].append("Imagen del Golfo")

                print("titulo1 desp 2o append ", news[d])
                for k in news:
                    print(k)




        except Exception as e:
            mensaje = ("error", e)
    if task_Option == 'versiones':
        try:
            Medio = "Versiones"
            for d in news:
                print("dic value ", news[d])
                page = requests.get(news[d])

                tree = html.fromstring(page.content)
                Titulo_get = tree.xpath('//span[@class="u-salidin-izquierda"]/text()')
                print("titulo versiones")
                Titulo_f = Titulo_get[1]
                print(Titulo_f)

                Texto = tree.xpath('//div[@class="anli-ss"]/following-sibling::div[1]//text()')
                Texto = [x.rstrip() for x in Texto]
                Textof = Texto[2]
                print(Textof)

                print("tamaño del texto(parrafos y lineas en blanco ", len(Texto))
                # vamos a contar vacios para solo poner 2 parrafos

                Textos = ""
                for t in Texto:
                    Textos = Textos + t

                Fecha_get = tree.xpath('//p[@class="fecha"]/text()')
                #Fecha_get = [x.rstrip() for x in Fecha_get]
                Fecha_getf = Fecha_get[0].encode("utf-8")
                print("fecha ", Fecha_get)


                news[d] = [Titulo_f]
                news[d].append(Textos)
                news[d].append(Fecha_getf)
                short_url = bitly_url(d)
                news[d].append(short_url)
                news[d].append("Versiones")



        except Exception as e:
            mensaje = ("error", e)
    return render_template("notas.html", datos=task_Option, noticias=news)





if __name__ == "__main__":
    app.debug = True
    app.run()