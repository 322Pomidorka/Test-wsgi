import views
from middleware.urldispatch import URLDispatch

view_list = [
    ('/', views.AnimeIndex),
    ('/anime/add', views.AnimeCreate),
    (r'^/anime/(?P<id>\d+)/$', views.AnimeRead),
    (r'^/anime/(?P<id>\d+)/edit/$', views.AnimeUpdate),
    (r'^/anime/(?P<id>\d+)/delete/$', views.AnimeDelete),
    ('/test', views.AnimeXlsx),
    ('/genre/add', views.GenreAdd),
]

dispatch = URLDispatch(view_list)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from db.query_set import create_db

    create_db()
    httpd = make_server('127.0.0.1', 8080, dispatch)
    httpd.serve_forever()
