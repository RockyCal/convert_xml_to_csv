__author__ = 'Raquel'

import xml.etree.ElementTree as eTree
from xml.etree.ElementTree import ParseError
from urllib.request import urlopen, Request, urljoin
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

namespaces = {'gmi': "http://www.isotc211.org/2005/gmi", 'gmd': "http://www.isotc211.org/2005/gmd", 'gco':
              'http://www.isotc211.org/2005/gco', 'gml': "http://www.opengis.net/gml/3.2", 'gmx':
              "http://www.isotc211.org/2005/gmx", 'gsr': "http://www.isotc211.org/2005/gsr",
              'gss': "http://www.isotc211.org/2005/gss", 'gts': "http://www.isotc211.org/2005/gts",
              'xlink': "http://www.w3.org/1999/xlink", 'xsi': "http://www.w3.org/2001/XMLSchema-instance",
              'saxon': "http://saxon.sf.net/", 'srv': "http://www.isotc211.org/2005/srv",
              'schemaLocation': "http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata"
                                "/published/xsd/schema.xsd"}
hydro10 = "http://hydro10.sdsc.edu/"
#source = "http://hydro10.sdsc.edu/metadata/"


def search_dir(request):
    curr_dir = BeautifulSoup(urlopen(request))
    dir_link = request.full_url
    for file in curr_dir.find_all('a'):
        if file['href'] != '/metadata/':
            file_link = urljoin(dir_link, file['href'])
            try:
                eTree.parse(urlopen(file_link))
            except ParseError as e:
                print("{}; {}".format(e.msg, request.full_url))
            tree = eTree.parse(urlopen(file_link))
            root = tree.getroot()
            print(root.tag)


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

choice = input("Would you like to run through a single (d)irectory or a (s)ource with many directories? ")
if choice == 's':
    source_link = input("Please provide the source url: ")
    search_from_source(source_link)
elif choice == 'd':
    directory_link = input("Please provide the directory url: ")
    dir_request = Request(directory_link)
    search_dir(dir_request)
else:
    print("Not a valid option")
    choice = input("Would you like to run through a single (d)irectory or a (s)ource with many directories? ")