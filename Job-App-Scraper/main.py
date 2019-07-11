import requests
import simplejson as json
from lxml import html

USERNAME = "gu1136576"
PASSWORD = "lecturer"

MAIN_URL = "https://ukjobs.uky.edu/hr/login"
LOGIN_URL = "https://ukjobs.uky.edu/hr/sessions"
COUNT = 0


def parse_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    f.close()
    return data


def create_result(content_url, username, password):
    session_requests = requests.session()
    result = session_requests.get(MAIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    payload = {
        "user[username]": username,
        "user[password]": password,
        "authenticity_token": authenticity_token
    }

    result = session_requests.post(LOGIN_URL, data=payload,
                                   headers=dict(referer=LOGIN_URL))

    if (result.status_code == 200):
        result = session_requests.get(content_url,
                                      headers=dict(referer=content_url))
        print(result.text)
        return result


def store_file(created_file, directory):
    print("Done storing " + created_file + " in " + directory)


def parse_result(html_result):
    # parse result applications and store in directories
    print("==============================================\n" +
          "==============================================\n" +
          "==============================================\n")
    return [0]


def main():
    config_data = parse_json("config.json")
    lecturer_one = config_data["fe02030"]
    lecturer_two = config_data["fe02031"]
    lecturer_three = config_data["fe02034"]

    # Leturer Position One
    result = create_result(lecturer_one["url"], lecturer_one["username"],
                           lecturer_one["password"])
    applications = parse_result(result)

    # Lecturer Position Two
    result = create_result(lecturer_two["url"], lecturer_two["username"],
                           lecturer_two["password"])
    applications = parse_result(result)

    # Lecturer Position Three
    result = create_result(lecturer_three["url"], lecturer_three["username"],
                           lecturer_three["password"])
    applications = parse_result(result)


if __name__ == '__main__':
    main()
