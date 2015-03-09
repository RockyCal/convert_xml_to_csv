#convert_xml_to_csv

---TEMPORARY---

So the goal of this is to get data out of the xml files on hydro10.sdsc.edu/metadata and put it into csv files

The headers are in write_csv.py in the headers dictionary. The keys are the headers and the values are the xml tags that correspond to that header

This is the updated link for those terms and those explanations: http://dublincore.org/documents/dcmi-terms/

An important aside: this notation {http://alink.com}term is a tag with a namespace. It's how they appear as alink:term on the xml file. It's supposed to refer to a document schema. You'll see the dublin core tags have a purl link that doesn't work. The replacement is the link I gave you in teh previous message

element tree in python 3:
https://docs.python.org/3.4/library/xml.etree.elementtree.html