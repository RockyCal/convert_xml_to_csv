__author__ = 'Raquel'


class Header:
    # Class to represent csv headers
    def __init__(self, name, required):
        self.name = name
        self.required = required

    def is_required(self):
        return self.required

headers_dict = {'name': 1, 'description': 1, 'resource url': 1, 'keywords': 0, 'defining citation': 0, 'related to': 0,
                'parent organization': 0, 'abbreviation': 0, 'synonyms': 0, 'funding info': 0}

headers = []
for k, v in headers_dict.items():
    if headers_dict[k] == 1:
        header_string = '{}*'.format(k)
        headers.append(header_string)
    else:
        headers.append(k)

for each in headers:
    print(each)