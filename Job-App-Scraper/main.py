#!/usr/local/bin/python3

###############################################################################
#   USAGE: Scrapes the hard coded Job Application pages for applicant results #
#   and uploads them to the comm.uky.edu filesystem                           #
###############################################################################

import requests
import time
import simplejson as json
from bs4 import BeautifulSoup
from lxml import html
from html_node import Result

###############################################################################
#    MAIN REQUEST URLS                                                        #
#    @MAIN_URL - The main login page for the UKJobs website.                  #
#        This page is static and contains one form which is the login form    #
#                                                                             #
#    @LOGIN_URL - The session handler for UKJobs HR Login.                    #
#        This is where the session should be posted to properly login.        #
###############################################################################
MAIN_URL = "https://ukjobs.uky.edu/hr/login"
LOGIN_URL = "https://ukjobs.uky.edu/hr/sessions"
UK_JOBS = "https://ukjobs.uky.edu"


def parse_json(json_file):
    """
        Usage:
            Used to parse the config file for scraping

        Parameters:
            : json_file (str) : The path to the config file
        
        Returns:
            : data : An object which contains the parsed json data
    """
    with open(json_file) as f:
        data = json.load(f)
    f.close()
    return data


def scrape_html(content_url, username, password):
    """
        Usage:
            Used to scrape the html from a job application page.
            Requires an active sessions and username/password.
        Parameters:
            : content_url (str) : The url with the HTML that we want to scrape
            : username (str) : The username for the user that
                                has the job posting
            : password (str) : The password for the user that
                                has the job posting
        Returns:
            : result (Reponse Object) : A response object that
                                        can be used to get the HTML Node
    """
    session_requests = requests.session()
    result = session_requests.get(MAIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(
        set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

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
        return result


def store_file(created_file, directory):
    """
        DocString to be done
    """
    print("Done storing " + created_file + " in " + directory)


def parse_result(html_result):
    """
        Usage:
            Scrape all applications from an HTML result
        Parameters:
            : html_result (str) : A large string containing the
                                entire html_node from the job posting page
        Returns:
            : applications : A list filled with lists that
            contains application data
    """
    # parse result applications and store in directories
    # returns list of lists (each table representing a result)
    soup = BeautifulSoup(html_result, features="lxml")
    results_table = soup.find_all('table', id="results")[0]
    even_results = [result for result in results_table.find_all('tr',
                                                                class_="even")]
    odd_results = [result for result in results_table.find_all('tr',
                                                               class_="odd")]

    all_results = [Result(result) for result in
                   (even_results+odd_results)]

    return all_results


def main():
    config_data = parse_json("config.json")
    lecturer_one = config_data["fe02030"]
    lecturer_two = config_data["fe02031"]
    lecturer_three = config_data["fe02034"]

    # Leturer Position One
    print("Scraping Lecturer One")
    result = scrape_html(lecturer_one["url"], lecturer_one["username"],
                         lecturer_one["password"])
    applications = parse_result(result.text)
    print([[applicants.name, applicants.vita, applicants.letter,
            applicants.special_request] for applicants in applications])

    # Lecturer Position Two
    print("Scraping Lecturer Two")
    result = scrape_html(lecturer_two["url"], lecturer_two["username"],
                         lecturer_two["password"])
    applications = parse_result(result.text)
    print([[applicants.name, applicants.vita, applicants.letter,
            applicants.special_request] for applicants in applications])
    
    # Lecturer Position Three
    print("Scraping Lecturer Three")
    result = scrape_html(lecturer_three["url"], lecturer_three["username"],
                         lecturer_three["password"])
    applications = parse_result(result.text)
    print([[applicants.name, applicants.vita, applicants.letter,
            applicants.special_request] for applicants in applications])

if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = (time.time() - start_time)
    print("Completed in " + str(run_time))
