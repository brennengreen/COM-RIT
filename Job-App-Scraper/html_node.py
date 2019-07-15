from bs4 import BeautifulSoup


class Result():
    def __init__(self, html_text):
        self.html = html_text
        self.type = "html_node"
        self.name = self.find_applicant_name()
        self.vita = self.get_media_path("Curriculum Vita")
        self.letter = self.get_media_path("Cover Letter")
        self.special_request = self.get_media_path("Specific Request 1")

    def __str__(self):
        return (self.type, self.html)

    def find_applicant_name(self):
        anchors = self.html.find_all("a")
        for a in anchors:
            if "href" not in a.attrs:
                continue
            if a["href"][0:21] == "/hr/job_applications/":
                if ',' in a.get_text():
                    return a.get_text()

    def get_media_path(self, media_text):
        anchors = self.html.find_all("a")
        for a in anchors:
            if "href" not in a.attrs:
                continue
            if a.get_text() == media_text:
                return a["href"]
