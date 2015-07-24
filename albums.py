# coding=utf-8

import os
import urllib
import settings

from tapioca_facebook import Facebook

api = Facebook(
    access_token=settings.ACCESS_TOKEN, client_id=settings.CLIENT_ID
)

def salvar_fotos(album):
    print(u'Salvando o album: %s' % album.name().data())
    caminho_desse_arquivo = os.path.abspath(__file__)
    dir_desse_arquivo = os.path.dirname(caminho_desse_arquivo)
    dir_album = os.path.join(dir_desse_arquivo, album.name().data())
    try:
        os.makedirs(dir_album)
    except OSError:
        print(u'Pasta já existe')
    for foto in api.user_photos(id=album.id().data()).get():
        try:
            nome_foto = foto.name().data() + '.jpg'
        except AttributeError:
            nome_foto = foto.id().data() + '.jpg'
        caminho_foto = os.path.join(dir_album, nome_foto)
        foto_objeto = api.object(id=foto.id().data()).get()
        try:
            urllib.urlretrieve(
                foto_objeto.images().data()[0]['source'],
                caminho_foto
            )
        except Exception as ex:
            print(u'Não deu para baixar')
            print(ex)

def main():
    albuns = api.user_albums(id='me').get()
    for album in albuns:
        salvar_fotos(album)

if __name__ == '__main__':
    main()
