import time
import requests


def check(host):
    while True:
        time.sleep(60 * 10)
        requests.get(host + '/check')