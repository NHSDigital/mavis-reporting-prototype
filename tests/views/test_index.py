def default_url():
    return "/reporting/"


def test_that_index_redirects_to_region(client):
    response = client.get(default_url(), follow_redirects=False)
    redirect_to = response.headers["Location"]
    assert redirect_to.endswith("/reporting/region/Y55")
