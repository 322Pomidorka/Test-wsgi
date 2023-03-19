import re


class URLDispatch(object):

    def __init__(self, view_list):
        self.view_list = view_list

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        for prefix, view in self.view_list:
            if path_info == prefix or path_info == prefix + '/':
                return view(environ, start_response)
            match = re.match(prefix, path_info) or re.match(prefix, path_info + '/')
            if match and match.groupdict():
                environ['url_params'] = match.groupdict()
                return view(environ, start_response)
        start_response('404 Not Found',
                       [('content-type', 'text/plain')])
        return [b'not found']
