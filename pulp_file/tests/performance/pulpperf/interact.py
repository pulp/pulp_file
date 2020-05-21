import logging
import requests
import tempfile
import time

from pulp_smash import config

from .utils import measureit, urljoin

cfg = config.get_config()
BASE_ADDR = cfg.get_base_url()


def get(url, params={}):
    """Wrapper around requests.get with some simplification in our case."""
    url = BASE_ADDR + url

    r = requests.get(url=url, params=params)
    r.raise_for_status()
    data = r.json()
    return data


def get_results(url, params={}):
    """Wrapper around requests.get with some simplification in our case."""
    out = []
    params["limit"] = 100
    params["offset"] = 0
    while True:
        data = get(url, params)
        out += data["results"]
        params["offset"] += 100
        if data["next"] is None:
            break
    return out


def post(url, data):
    """Wrapper around requests.post with some simplification in our case."""
    url = BASE_ADDR + url

    r = requests.post(url=url, json=data)
    r.raise_for_status()
    return r.json()


def download(base_url, file_name, file_size):
    """Downlad file with expected size and drop it."""
    with tempfile.TemporaryFile() as downloaded_file:
        full_url = urljoin(base_url, file_name)
        duration, response = measureit(requests.get, full_url)
        response.raise_for_status()
        downloaded_file.write(response.content)
        assert downloaded_file.tell() == file_size
        return duration


def wait_for_tasks(tasks, timeout=None):
    """
    Wait for tasks to finish.

    Returns task info. If we time out, list of None is returned.
    """
    start = time.time()
    out = []
    step = 3
    for t in tasks:
        while True:
            if timeout is not None:
                now = time.time()
                if now >= start + timeout:
                    raise Exception("Task %s timeouted" % t)
            response = get(t)
            logging.debug("Task status is '%s', full response %s" % (response["state"], response))
            if response["state"] in ("failed", "cancelled", "completed"):
                out.append(response)
                break
            else:
                time.sleep(step)
    return out
