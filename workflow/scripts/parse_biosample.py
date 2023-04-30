import pandas as pd
import numpy as np
import argparse
import sys
import time
from Bio import Entrez
import xml.etree.ElementTree as et

def parse_entrez(join_biosamples, email = "eew226@msstate.edu",  endcount = None):
    Entrez.email = email
    biosamples = {}
    separator = "\t"
    query = set()
    header_set = set()
    count = 0
    sys.stdout.write(f"Entrez start time: {time.asctime()}\n")
    sys.stdout.write(f"Number of samples: {join_biosamples.size}\n\n")
    handle = Entrez.efetch(db="biosample", id=join_biosamples)
    if False:
        print("taxid is {}".format(taxid))
    tree = et.parse(handle)
    root = tree.getroot()
    for sample in root:
        #if args.debug:
        if False:
            indent(sample)
            et.dump(sample)
        BIOSAMPLE = sample.attrib['accession']
        if BIOSAMPLE not in biosamples:
           biosamples[BIOSAMPLE] = {}
        for attributes in root.iter('Attributes'): # sample to root?
            for metadata in attributes:
                keyname = metadata.attrib['attribute_name']
                if 'harmonized_name' in metadata.attrib:
                    keyname = metadata.attrib['harmonized_name']
                header_set.add(keyname)
                biosamples[BIOSAMPLE][keyname] = metadata.text
        count += 1
        if(count%100 == 0):
            sys.stdout.write(f"Count : {count} Time: {time.asctime()}\n")
        if(count is endcount):
                metadata = pd.DataFrame(biosamples).T
                metadata.index.name = 'biosample'
                metadata.reset_index(inplace=True)
                return metadata 
    metadata = pd.DataFrame(biosamples).T
    metadata.index.name = 'biosample'
    metadata.reset_index(inplace=True)
    return metadata   
'''
def parse_entrez(join_biosamples, email = "eew226@msstate.edu",  endcount = 200):
    Entrez.email = email
    biosamples = {}
    separator = "\t"
    query = set()
    header_set = set()
    count = 0
    sys.stdout.write(f"Entrez start time: {time.asctime()}\n")
    sys.stdout.write(f"Number of samples: {join_biosamples.size}\n\n")
    for sampid in join_biosamples:
        handle = Entrez.efetch(db="biosample", id=sampid)
        if False:
            print("taxid is {}".format(taxid))
        tree = et.parse(handle)
        root = tree.getroot()
        for sample in root:
            #if args.debug:
            if False:
                indent(sample)
                et.dump(sample)
            BIOSAMPLE = sample.attrib['accession']
            if BIOSAMPLE not in biosamples:
                biosamples[BIOSAMPLE] = {}
            for attributes in root.iter('Attributes'): # sample to root?
                for metadata in attributes:
                    keyname = metadata.attrib['attribute_name']
                    if 'harmonized_name' in metadata.attrib:
                        keyname = metadata.attrib['harmonized_name']
                    header_set.add(keyname)
                    biosamples[BIOSAMPLE][keyname] = metadata.text
            count += 1
            if(count%100 == 0):
                sys.stdout.write(f"Count : {count} Time: {time.asctime()}\n")
            if count == endcount:
                metadata = pd.DataFrame(biosamples).T
                metadata.index.name = 'biosample'
                metadata.reset_index(inplace=True)
                return metadata    
                
                
    metadata = pd.DataFrame(biosamples).T
    metadata.index.name = 'biosample'
    metadata.reset_index(inplace=True)
    
    return metadata


Entrez.email = "eew226@msstate.edu"
join_biosamples = joined['biosample']
biosamples = {}
separator = "\t"
query = set()
header_set = set()
count = 0
sys.stdout.write(f"Entrez start time: {time.asctime()}\n")
sys.stdout.write(f"Number of samples: {join_biosamples.size}\n\n")
handle = Entrez.efetch(db="biosample", id=join_biosamples)
if False:
    print("taxid is {}".format(taxid))
tree = et.parse(handle)
root = tree.getroot()
for sample in root:
    #if args.debug:
    if False:
        indent(sample)
        et.dump(sample)
    BIOSAMPLE = sample.attrib['accession']
    if BIOSAMPLE not in biosamples:
       biosamples[BIOSAMPLE] = {}
    for attributes in root.iter('Attributes'): # sample to root?
        for metadata in attributes:
            keyname = metadata.attrib['attribute_name']
            if 'harmonized_name' in metadata.attrib:
                keyname = metadata.attrib['harmonized_name']
            header_set.add(keyname)
            biosamples[BIOSAMPLE][keyname] = metadata.text
    count += 1
    if(count%100 == 0):
        sys.stdout.write(f"Count : {count} Time: {time.asctime()}\n")
metadata = pd.DataFrame(biosamples).T
metadata.index.name = 'biosample'
metadata.reset_index(inplace=True)
return metadata   
'''