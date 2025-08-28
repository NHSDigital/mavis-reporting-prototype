def default_url():
    return "/reporting/"


def test_that_index_redirects_to_region(client):
    client.post("/reporting/login", data={"role": "region"}, follow_redirects=False)
    response = client.get("/reporting/", follow_redirects=False)
    redirect_to = response.headers["Location"]
    assert redirect_to.endswith("/reporting/region/Y55")
