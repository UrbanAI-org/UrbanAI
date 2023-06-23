import pytest
import requests
import os

url = f"http://localhost:9999/"

def count_file():
    dir_path = '../data/pcd'
    count = 0
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


@pytest.fixture
def download():
    before_count = count_file(url + 'download')
    requests.post()
    after_count = count_file()
    assert before_count + 1 == after_count
    assert requests.get().status_code == 200
    
