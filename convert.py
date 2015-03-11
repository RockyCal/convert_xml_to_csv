__author__ = 'Raquel'

import xml.etree.ElementTree as eTree
from xml.etree.ElementTree import ParseError
from urllib.request import urlopen, Request, urljoin
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re
import csv


class Record:
    def __init__(self, file_id):
        self.file_id = file_id

namespaces = {'gmi': "http://www.isotc211.org/2005/gmi", 'gmd': "http://www.isotc211.org/2005/gmd", 'gco':
              'http://www.isotc211.org/2005/gco', 'gml': "http://www.opengis.net/gml/3.2", 'gmx':
              "http://www.isotc211.org/2005/gmx", 'gsr': "http://www.isotc211.org/2005/gsr",
              'gss': "http://www.isotc211.org/2005/gss", 'gts': "http://www.isotc211.org/2005/gts",
              'xlink': "http://www.w3.org/1999/xlink", 'xsi': "http://www.w3.org/2001/XMLSchema-instance",
              'saxon': "http://saxon.sf.net/", 'srv': "http://www.isotc211.org/2005/srv",
              'schemaLocation': "http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata"
              "/published/xsd/schema.xsd"}

hydro10 = "http://hydro10.sdsc.edu/"
# source = "http://hydro10.sdsc.edu/metadata/"

dublin_core = "http://dublincore.org/documents/dcmi-terms/"

fieldnames = ['name', 'description', 'resource url', 'keywords', 'defining citation', 'related to',
              'parent organization', 'abbreviation', 'synonyms', 'funding info']


def parse_dublin_core(root, record, writer):
    print(record.file_id)
    for child in root.iter():
        print(child.text)
    dc = root.find('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
    record.name = dc.find('{http://purl.org/dc/elements/1.1/}title').text
    record.url = dc.find('{http://purl.org/dc/elements/1.1/}identifier').text
    if dc.find('{http://purl.org/dc/elements/1.1/}description'):
        record.description = dc.find('{http://purl.org/dc/elements/1.1/}description').text
    else:
        record.description = None
    keywords = []
    for each in dc.findall('{http://purl.org/dc/elements/1.1/}subject'):
        if each.text is not None:
            keywords.append(each.text)
    record.keywords = ', '.join(keywords)
    if dc.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation'):
        record.defining_citation = dc.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation').text
    else:
        record.defining_citation = ""
    record.related_to = dc.find('{http://purl.org/dc/terms/}references').text
    writer.writerow({'name': record.name, 'resource url': record.url, 'description': record.description, 'keywords':
                     record.keywords, 'defining citation': record.defining_citation, 'related to':
                     record.related_to, 'parent organization': '', 'abbreviation': '', 'synonyms': '',
                     'funding info': ''})


def search_dir(request):
    resource_title = re.sub('http://hydro10.sdsc.edu/metadata/', '', request.full_url).strip('/ ')
    with open('{}.csv'.format(resource_title), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        curr_dir = BeautifulSoup(urlopen(request))
        dir_link = request.full_url
        for file in curr_dir.find_all('a'):
            record = Record(file.text)
            if file['href'] != '/metadata/':
                file_link = urljoin(dir_link, file['href'])
                try:
                    eTree.parse(urlopen(file_link))
                except ParseError as e:
                    print("{}; {}".format(e.msg, request.full_url))
                tree = eTree.parse(urlopen(file_link))
                root = tree.getroot()
                if root.tag == "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF":
                    parse_dublin_core(root, record, writer)
                #elif root.tag == "{http://www.isotc211.org/2005/gmd}MD_Metdata" or root.tag == "{http://www.isotc211.org/" \
                #                                                                              "2005/gmi}MI_Metdata":
                # parse_iso(root, writer)


def search_from_source(source):
    soup = BeautifulSoup(urlopen(source))

    # Get all links in this page
    for each in soup.find_all('a'):

        # Check if directory. Directory will have format /metadata/[anything]/
        if re.fullmatch('/metadata/(.*)/', each['href']) and each['href'] != '/metadata/annotated/':
            req = Request(urljoin(hydro10, each['href']))
            try:
                urlopen(req)
            except HTTPError as e:
                print("Error with link: {}, {}, {}".format(e.reason, e.code, e.headers))
            except URLError as e:
                print("Error with link: {}".format(e.reason))
            # URL to directory works so now get all the files in that directory
            # Each 'file' is a http link to xml file
            search_dir(req)


"""Initialize by asking user for type of input and link to it"""
while True:
    try:
        choice = input("Would you like to run through a single (d)irectory or a (s)ource with many directories?")
    except ValueError:
        print("Sorry, could not understand that, please enter 'd' or 's' ")
        continue
    if choice != 's' and choice != 'd':
        print("Not a valid option, please enter 'd' or 's' ")
        continue
    elif choice == 's':
        source_link = input("Please provide the source url: ")
        search_from_source(source_link)
    elif choice == 'd':
        directory_link = input("Please provide the directory url: ")
        dir_request = Request(directory_link)
        search_dir(dir_request)