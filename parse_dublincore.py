__author__ = 'Raquel'
import csv


class Resource:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    description = ""
    keywords = []
    defining_citation = ""
    references = ""

dc_dict = {'{http://purl.org/dc/elements/1.1/}title': 'name', '{http://purl.org/dc/elements/1.1/}description':
           'description', '{http://purl.org/dc/elements/1.1/}identifier': 'resource url',
           '{http://purl.org/dc/elements/1.1/}subject': 'keywords',
           '{http://purl.org/dc/elements/1.1/}bibliographicCitation': 'defining citation',
           '{http://purl.org/dc/elements/1.1/}references': 'related to', }


def parse_dublin_core(root):
    title = root.find('{http://purl.org/dc/elements/1.1/}title').text
    url = root.find('{http://purl.org/dc/elements/1.1/}identifier').text
    description = root.find('{http://purl.org/dc/elements/1.1/}description')
    keywords = []
    for each in root.findall('{http://purl.org/dc/elements/1.1/}subject'):
        keywords.append(each.text)
    if root.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation'):
        defining_citation = root.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation').text
    if root.find('{http://purl.org/dc/elements/1.1/}references'):
        related_to = root.find('{http://purl.org/dc/elements/1.1/}references').text