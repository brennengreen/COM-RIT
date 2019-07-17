#!/usr/local/bin/python3

###############################################################################
#   USAGE: Scrapes the hard coded Job Application pages for applicant results #
#   and uploads them to the comm.uky.edu filesystem                           #
###############################################################################

import requests
import datetime
import time
import simplejson as json
import wget
import os
from bs4 import BeautifulSoup
from lxml import html
from html_node import Result

###############################################################################
#    MAIN REQUEST URLS                                                        #
#    MAIN_URL - The main login page for the UKJobs website.                  #
#        This page is static and contains one form which is the login form    #
#                                                                             #
#    LOGIN_URL - The session handler for UKJobs HR Login.                    #
#        This is where the session should be posted to properly login.        #
###############################################################################
MAIN_URL = "https://ukjobs.uky.edu/hr/login"
LOGIN_URL = "https://ukjobs.uky.edu/hr/sessions"
UK_JOBS = "https://ukjobs.uky.edu"
LECT_ORG = "/Volumes/COM Web Pages/data/jobsearch/app/webroot/files/Lecturer Org/"
LECT_GEN = "/Volumes/COM Web Pages/data/jobsearch/app/webroot/files/Lecturer Gen/"
session_requests = requests.session()


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


def download_path(path, dir_path, file_name):
    """
        Usage:
            Return a response object that is the media file contained in a url.
        Parameters:
            : path (str) : A path which is the url to a media file that will
            be downloaded.
        Returns:
            : file (response) : The response object which is the file we're
            trying to download.
    """
    response = session_requests.get(path)
    f = open(os.path.join(dir_path, file_name), 'wb')
    f.write(response.content)
    f.close()


def sort_applicants(category_path, applicant_list):
    """
        Usage:
            Sort all applicants in a specified list to a specified category
            directory.
        Parameters:
            : category_path (str) : A string that represents the path to a
            specified category directory
            : applicant_list (html_node/Result) : A list of applicants that
            need to be categorized
    """
    for applicant in applicant_list:
        applicant_folder = applicant.name.replace(", ", " ").title()
        applicant_folder = applicant_folder.replace(" ", "_")
        full_path = os.path.join(category_path + applicant_folder)

        try:
            os.mkdir(full_path)
        except FileExistsError:
            # There is no reason to "handle" this error further
            # if the file already exists it was already added to the 
            # file system and just needs to be ignored
            continue
        
        print("Now sorting applicant: " + applicant.name)
        
        vita_path = UK_JOBS + applicant.vita
        letter_path = UK_JOBS + applicant.letter
        evidence_path = UK_JOBS + applicant.special_request

        download_path(vita_path, full_path, "vita.pdf")
        download_path(letter_path, full_path, "letter.pdf")
        download_path(evidence_path, full_path, "evidence.pdf")


def main():
    print("---- DAILY SCRAPE ----\n---- {date} ----".format(date=datetime.datetime.now()))
    config_data = parse_json("config.json")
    lecturer_one = config_data["fe02030"]
    lecturer_two = config_data["fe02031"]
    lecturer_three = config_data["fe02034"]

    # Leturer Position One
    print("Scraping Lecturer One")
    result = scrape_html(lecturer_one["url"], lecturer_one["username"],
                         lecturer_one["password"])
    applications = parse_result(result.text)
    sort_applicants(LECT_GEN, applications)

    # Lecturer Position Two
    print("\n\nScraping Lecturer Two")
    result = scrape_html(lecturer_two["url"], lecturer_two["username"],
                         lecturer_two["password"])
    applications = parse_result(result.text)
    sort_applicants(LECT_ORG, applications)

    # Lecturer Position Three
    print("\n\nScraping Lecturer Three")
    result = scrape_html(lecturer_three["url"], lecturer_three["username"],
                         lecturer_three["password"])
    applications = parse_result(result.text)
    sort_applicants(LECT_ORG, applications)


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = (time.time() - start_time)
    print("Completed in " + str(run_time))
