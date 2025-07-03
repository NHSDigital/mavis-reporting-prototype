import urllib.parse


def dict_without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def url_without_param(url, param):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(url)
    query_without_param = dict_without_keys(query_params, "token")
    parsed_url._replace(query=query_without_param)
    return urllib.parse.urlunparse(parsed_url)
