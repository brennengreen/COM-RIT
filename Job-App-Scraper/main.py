import requests
from lxml import html

USERNAME = "gu1136576"
PASSWORD = "lecturer"

MAIN_URL = "https://ukjobs.uky.edu/hr/login"
LOGIN_URL = "https://ukjobs.uky.edu/hr/sessions"
CONTENT_URL = "https://ukjobs.uky.edu/hr/postings/236596/job_applications"


def main():
    session_requests = requests.session()
    result = session_requests.get(MAIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    payload = {
        "user[username]":USERNAME,
        "user[password]":PASSWORD,
        "authenticity_token":authenticity_token
    }

    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer=LOGIN_URL))

    if (result.status_code == 200):
        result = session_requests.get(CONTENT_URL, headers = dict(referer=CONTENT_URL))
    print(result.text)


if __name__ == '__main__':
    main()