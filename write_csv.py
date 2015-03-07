__author__ = 'Raquel'


class Header:
    # Class to represent csv headers
    def __init__(self, name, required):
        self.name = name
        self.required = required

    def is_required(self):
        return self.required

headers = {'name': 1, 'description': 1, 'resource url': 1, 'keywords': 0, 'defining citation': 0, 'related to': 0,
           'parent organization': 0, 'abbreviation': 0, 'synonyms': 0, 'funding info': 0}

dc_dict = {'{http://purl.org/dc/elements/1.1/}name': 'name', '{http://purl.org/dc/elements/1.1/}description':
           'description', '{http://purl.org/dc/elements/1.1/}identifier': 'resource url',
           '{http://purl.org/dc/elements/1.1/}subject': 'keywords',
           '{http://purl.org/dc/elements/1.1/}bibliographicCitation': 'defining citation', }