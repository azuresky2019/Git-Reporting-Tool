import requests

def connectivity(dummy_url, timeout):
    try:
        _ = requests.get(dummy_url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("Failed connecting to the internet. Please check your connection and try again !")
    return False


def auth_to_me(git_url, user, pass_wrd):
    r = requests.get(git_url, auth=(user, pass_wrd))
    if r.status_code == 200:
        return True
    else:
        return False

def get_json_url(git_url):
    json_get = requests.get(git_url)
    return json_get.json()
