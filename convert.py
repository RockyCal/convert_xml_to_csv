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
    description = None
    defining_citation = None
    related_to = None
    parent_organization = None
    abbreviation = None
    synonyms = None
    funding_info = None


class Citation:
    def __init__(self, title):
        self.title = title
        self.altTitle = ''
        self.date = ''
        self.date_type = ''
        self.edition = ''
        self.editionDate = None
        self.identifiers = []
        self.citedResponsibleParty = None
        self.presentationForm = None
        self.series = None
        self.otherCitationDetails = ''
        self.collectiveTitle = ''
        self.ISBN = ''
        self.ISSN = ''

    def form_citation(self):
        return self.title + '. ' + self.date + '. ' + self.edition + '. '

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

fieldnames = ['file_id', 'name', 'description', 'resource url', 'keywords', 'defining citation', 'related to',
              'parent organization', 'abbreviation', 'synonyms', 'funding info']

def get_value(elem):
    return elem.find('{http://www.isotc211.org/2005/gco}CharacterString').text

def parse_iso(root, record, writer):
    # File id
    record.file_id = root.find("{http://www.isotc211.org/2005/gmd}fileIdentifier"). \
        find("{http://www.isotc211.org/2005/gco}CharacterString").text
    print(record.file_id)

    md_data_id = root.find('{http://www.isotc211.org/2005/gmd}identificationInfo').find(
        '{http://www.isotc211.org/2005/gmd}MD_DataIdentification')

    # Name
    record.name = md_data_id.find('{http://www.isotc211.org/2005/gmd}citation').\
        find('{http://www.isotc211.org/2005/gmd}CI_Citation').find('{http://www.isotc211.org/2005/gmd}title').\
        find('{http://www.isotc211.org/2005/gco}CharacterString').text

    md_distribution = root.find('{http://www.isotc211.org/2005/gmd}distributionInfo').find('{http://www.isotc211.org/'
                                                                                           '2005/gmd}MD_Distribution')

    # URL can be in two different formats
    if md_distribution.find('{http://www.isotc211.org/2005/gmd}transferOptions') is not None:
        record.url = md_distribution.find('{http://www.isotc211.org/2005/gmd}transferOptions').\
            find('{http://www.isotc211.org/2005/gmd}MD_DigitalTransferOptions').\
            find('{http://www.isotc211.org/2005/gmd}onLine').\
            find('{http://www.isotc211.org/2005/gmd}CI_OnlineResource').\
            find('{http://www.isotc211.org/2005/gmd}linkage').find('{http://www.isotc211.org/2005/gmd}URL').text
    elif md_distribution.find('{http://www.isotc211.org/2005/gmd}distributor') is not None:
        record.url = md_distribution.find('{http://www.isotc211.org/2005/gmd}distributor').\
            find('{http://www.isotc211.org/2005/gmd}MD_Distributor').\
            find('{http://www.isotc211.org/2005/gmd}distributorTransferOptions').\
            find('{http://www.isotc211.org/2005/gmd}MD_DigitalTransferOptions').\
            find('{http://www.isotc211.org/2005/gmd}onLine').\
            find('{http://www.isotc211.org/2005/gmd}CI_OnlineResource').\
            find('{http://www.isotc211.org/2005/gmd}linkage').find('{http://www.isotc211.org/2005/gmd}URL').text

    # Description
    record.description = md_data_id.find('{http://www.isotc211.org/2005/gmd}abstract')

    # Keywords
    keywords = []
    if md_data_id.find('{http://www.isotc211.org/2005/gmd}descriptiveKeywords') is not None:
        for each in md_data_id.find('{http://www.isotc211.org/2005/gmd}descriptiveKeywords').\
                find('{http://www.isotc211.org/2005/gmd}MD_Keywords').\
                findall('{http://www.isotc211.org/2005/gmd}keyword'):
            keywords.append(each.find('{http://www.isotc211.org/2005/gco}CharacterString').text)
        record.keywords = ', '.join(keywords)

    # TODO: Citation
    citation = md_data_id.find('{http://www.isotc211.org/2005/gmd}citation').\
        find('{http://www.isotc211.org/2005/gmd}CI_Citation')

    citation_elems = ['{http://www.isotc211.org/2005/gmd}title',
                      '{http://www.isotc211.org/2005/gmd}alternativeTitle', '{http://www.isotc211.org/2005/gmd}date',
                      '{http://www.isotc211.org/2005/gmd}edition', '{http://www.isotc211.org/2005/gmd}editionDate',
                      '{http://www.isotc211.org/2005/gmd}identifier',
                      '{http://www.isotc211.org/2005/gmd}citedResponsibleParty',
                      '{http://www.isotc211.org/2005/gmd}presentationForm', '{http://www.isotc211.org/2005/gmd}series',
                      '{http://www.isotc211.org/2005/gmd}otherCitationDetails',
                      '{http://www.isotc211.org/2005/gmd}collectiveTitle',
                      '{http://www.isotc211.org/2005/gmd}ISBN', '{http://www.isotc211.org/2005/gmd}ISSN']
    # Get title
    title = citation.find('{http://www.isotc211.org/2005/gmd}title').find('{http://www.isotc211.org/2005/gco}'
                                                                          'CharacterString').text
    record_citation = Citation(title=title)
    ci_date = citation.find('{http://www.isotc211.org/2005/gmd}date').find('{http://www.isotc211.org/2005/gmd}CI_Date')
    # Get date type
    record_citation.date_type = ci_date.find('{http://www.isotc211.org/2005/gmd}dateType').\
        find('{http://www.isotc211.org/2005/gmd}CI_DateTypeCode').text
    # Get actual date
    if ci_date.find('{http://www.isotc211.org/2005/gmd}date').find('{http://www.isotc211.org/2005/gco}Date') is \
            not None:
        record_citation.date = ci_date.find('{http://www.isotc211.org/2005/gmd}date').\
            find('{http://www.isotc211.org/2005/gco}Date').text

    record_citation.edition = citation.findtext('{http://www.isotc211.org/2005/gmd}edition//{http://www.isotc211.org/'
                                                '2005/gco}CharacterString')

    # Organization
    record.parent_organization = root.find('{http://www.isotc211.org/2005/gmd}contact').\
        find('{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty')\
        .find('{http://www.isotc211.org/2005/gmd}organisationName')\
        .find('{http://www.isotc211.org/2005/gco}CharacterString').text


def parse_dublin_core(root, record, writer):
    print(record.file_id)
    dc = root.find('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')

    # Name
    record.name = dc.find('{http://purl.org/dc/elements/1.1/}title').text

    # Url
    record.url = dc.find('{http://purl.org/dc/elements/1.1/}identifier').text

    # Description
    if dc.find('{http://purl.org/dc/elements/1.1/}description') is not None:
        record.description = dc.find('{http://purl.org/dc/elements/1.1/}description').text

    # Keywords
    keywords = []
    for each in dc.findall('{http://purl.org/dc/elements/1.1/}subject'):
        if each.text is not None:
            keywords.append(each.text)
    record.keywords = ', '.join(keywords)

    # Citation
    if dc.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation') is not None:
        record.defining_citation = dc.find('{http://purl.org/dc/elements/1.1/}bibliographicCitation').text

    # References
    if dc.find('{http://purl.org/dc/terms/}references') is not None:
        record.related_to = dc.find('{http://purl.org/dc/terms/}references').text

    writer.writerow({'file_id': record.file_id, 'name': record.name, 'resource url': record.url, 'description': record.description, 'keywords':
                     record.keywords, 'defining citation': record.defining_citation, 'related to':
                     record.related_to, 'parent organization': record.parent_organization,
                     'abbreviation': record.abbreviation, 'synonyms': record.synonyms, 'funding info':
                     record.funding_info})


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
                elif root.tag == "{http://www.isotc211.org/2005/gmd}" \
                                 "MD_Metadata" or root.tag == "{http://www.isotc211.org/2005/gmi}MI_Metadata":
                    parse_iso(root, record, writer)


def search_from_source(source):
    soup = BeautifulSoup(urlopen(source))

    # Get all links in this page
    for each in soup.find_all('a'):

        # Check if directory. Directory will have format /metadata/[anything]/
        if re.fullmatch('/metadata/(.*)/', each['href']) and each['href'] != '/metadata/annotated/' and \
                        each['href'] != '/metadata/NGDS_Geoportal/':
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
        choice = input("Would you like to run through a single (d)irectory or a (s)ource with many directories? "
                       "Or (q)uit: ")
    except ValueError:
        print("Sorry, could not understand that, please enter 'd' or 's' ")
        continue
    if choice != 's' and choice != 'd' and choice != 'q':
        print("Not a valid option, please enter 'd' or 's' ")
        continue
    elif choice == 's':
        source_link = input("Please provide the source url: ")
        search_from_source(source_link)
        exit()
    elif choice == 'd':
        directory_link = input("Please provide the directory url: ")
        dir_request = Request(directory_link)
        search_dir(dir_request)
    elif choice == 'q':
        exit()