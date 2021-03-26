#!/usr/bin/env python3

import re
import csv
import gzip
import json
import os
from tqdm import tqdm
from glob import glob

# The phrase offset, the amount the search goes forth to match something after we find a trigger.
phraseoffset = 4


regexes = {k: [re.compile(v2, re.I) for v2 in v] for k,v in json.load(open('searchstrings.json')).items()}

frames = ['marketperspective', 'moralperspective', 'innovationperspective']
allfiles =  glob('../../data/raw-private/**/**/*.txt.gz')
outputfile = '../../data/intermediate/automatedcoding.csv'


def splitintosentences(document):
    text = document.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    sentences = text.split('.')
    return sentences

with open(outputfile, mode='w', newline='') as fo:
    fieldnames = ['country', 'year', 'company', 'marketperspective', 'moralperspective','innovationperspective']
    writer = csv.DictWriter(fo, fieldnames=fieldnames)
    writer.writeheader()
    for f in tqdm(allfiles):
        document = gzip.open(f, mode='rt').read()

        matches_form = {}
        for frame in frames:
            matches_form[frame] = 0
            phrases = splitintosentences(document)
            phrase_count = 0
            trigger = None
            for phrase in phrases:
                if not trigger:
                    for trigger_regex in regexes['trigger']:
                        trigger = any(trigger_regex.finditer(phrase))
                if trigger:
                    phrase_count += 1
                    for rex in regexes[frame]:
                        match = rex.findall(phrase)
                        if match:
                            #logging.info("** MATCH FOR " + frame + " **\n")
                            #logging.info("TRIGGER \n%s" % trigger)
                            #logging.info("MATCH USED:\n%s" % rex)
                            #logging.info("PHRASE WE ARE ANALYSING:\n%s" % phrase)
                            #logging.info("MATCH FOUND IN PHRASE:\n%s\n\n" % match)
                            trigger = None
                            matches_form[frame] += 1
                            break
                    if phrase_count > phraseoffset:
                        phrase_count = 0
                        trigger = None
        #print(f)
        #print(matches_form)
        #print('\n\n\n')
        country, company, year = os.path.split(f)[1].split('_')
        matches_form['country'] = country
        matches_form['year'] = int(year[:4])
        matches_form['company'] = company
        writer.writerow(matches_form)

