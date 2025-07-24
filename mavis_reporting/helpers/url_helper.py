from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode, urlunparse


def dict_without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def url_without_param(url, param):
    parsed_url = urlparse(url)
    query_params_as_dict = parse_qs(parsed_url.query)
    if param in query_params_as_dict:
        query_param_pairs = parse_qsl(parsed_url.query)
        query_pairs_without_param = [
            (p, v) for (p, v) in query_param_pairs if p != param
        ]

        parsed_url = parsed_url._replace(query=urlencode(query_pairs_without_param))
        return urlunparse(parsed_url)
    else:
        return url


def prepend_path(url, prefix):
    parsed_url = urlparse(url)
    prefixed_url = parsed_url._replace(path=(prefix + parsed_url.path))
    return urlunparse(prefixed_url)
