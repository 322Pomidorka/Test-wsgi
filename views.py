import os.path
import wsgiref.util
import html
from db.query_set import get_all_anime, create_xlsx, get_all_genre, add_genre
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qs
from db.query_set import create_anime


env = Environment(loader=FileSystemLoader('templates'))


class BaseView(object):

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response


class AnimeIndex(BaseView):

    def __iter__(self):

        anime_list = get_all_anime()
        print(anime_list)
        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield str.encode(env.get_template('home.html').render({'anime_list': anime_list}))


class AnimeCreate(BaseView):

    def __iter__(self):
        if self.environ['REQUEST_METHOD'].upper() == 'POST':

            content_length = int(self.environ['CONTENT_LENGTH'])
            values = parse_qs(html.unescape(self.environ['wsgi.input'].read(content_length).decode('ascii')))

            data = {
                'title': values['title'].pop(),
                'year': values['year'].pop(),
                'count_episodes': values['count_episodes'].pop(),
                'genre': html.unescape(values['genre'].pop()),
            }
            create_anime(**data)
            self.start_response('302 Found',
                                [('Content Type', 'text/plain'),
                                 ('Location', '/')])
            return

        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield str.encode(env.get_template('add.html').render({'genre_list': get_all_genre()}))


class AnimeRead(BaseView):
    def __iter__(self):
        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield b'Anime home  --> Read'


class AnimeUpdate(BaseView):

    def __iter__(self):
        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield b'Anime home  --> Update'


class AnimeDelete(BaseView):

    def __iter__(self):
        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield b'Anime home --> Delete'


class AnimeXlsx(BaseView):
    def __iter__(self):
        create_xlsx()
        headers = [('Content-Description', 'File Transfer'),
                   ('Content-Type', 'application/octet-stream'),
                   ('Content-Disposition', 'attachment; filename="' + os.path.basename('anime.xlsx') + '"'),
                   ('Expires', '0'),
                   ('Cache-Control', 'must-revalidate'),
                   ('Pragma', 'public'),
                   ('Content-Length', str(os.stat('anime.xlsx').st_size))]

        f = open('anime.xlsx', 'rb')
        self.start_response('200 OK', headers)
        return wsgiref.util.FileWrapper(f)


class GenreAdd(BaseView):
    def __iter__(self):
        if self.environ['REQUEST_METHOD'].upper() == 'POST':
            content_length = int(self.environ['CONTENT_LENGTH'])
            values = parse_qs(html.unescape(self.environ['wsgi.input'].read(content_length).decode('ascii')))
            add_genre(values['title'].pop())
            self.start_response('302 Found',
                                [('Content Type', 'text/plain'),
                                 ('Location', '/')])
            return

        self.start_response('200 OK', [('Content Type', 'text/plain')])
        yield str.encode(env.get_template('add_genre.html').render())