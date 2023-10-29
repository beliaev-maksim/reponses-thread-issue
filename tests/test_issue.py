from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import requests
import responses

@responses.activate
def test_get_threading():
    url = "http://test.org/get"
    responses.get(url, json={"status": "ok"})

    with ThreadPoolExecutor() as pool:
        r = pool.map(requests.get, [url, url])

    results = list(r)
    assert len(results) == 2
    assert results[0].json() == {"status": "ok"}
    assert results[1].json() == {"status": "ok"}

@responses.activate
def test_get_multiprocessing():
    url = "http://fake.org/get"
    responses.get(url, json={"status": "ok"})

    with ProcessPoolExecutor() as pool:
        r = pool.map(requests.get, [url, url])    # tries to reach non existant `http://test.org/get`

    results = list(r)
    assert len(results) == 2
    assert results[0].json() == {"status": "ok"}
    assert results[1].json() == {"status": "ok"}


if __name__ == "__main__":
    print("Running threading...")
    test_get_threading()
    print("Running multiprocessing...")
    test_get_multiprocessing()
