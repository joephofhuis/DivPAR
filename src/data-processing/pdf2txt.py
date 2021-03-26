#!/usr/bin/env python3

from glob import glob
from tqdm import tqdm
import os
import re
import PyPDF2
from tika import parser
import gzip

import signal
from contextlib import contextmanager


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        print('Parsing this page timed out...')
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError




def extract_pdf_pypdf2(path):
    text = ""
    with open(path, "rb") as pdf_file:
        pdfReader = PyPDF2.PdfFileReader(pdf_file)
        if pdfReader.isEncrypted:
            pdfReader.decrypt("")
        for i in range(1, pdfReader.numPages):
            with timeout(30):
                pageObj = pdfReader.getPage(i)
                s = pageObj.extractText()
                text = text + "\n" + s
    return text




def extract_pdf_tika(path):
    pdf_content = parser.from_file(path)
    text = pdf_content['content']
    return text


if __name__ == '__main__':

    errors = 0

    inputfiles = glob('jaarverslagen/nl/annuals 1/*.pdf')
    inputfiles.extend(glob('jaarverslagen/nl/annuals 2/*.pdf'))
    inputfiles.extend(glob('jaarverslagen/nl/annuals 3/*.pdf'))
    inputfiles.extend(glob('jaarverslagen/us/*.pdf'))

    outputdir = '../../data/raw-private'

    print(f'Processing {len(inputfiles)} files')

    for f in tqdm(inputfiles):
        dir, fn = os.path.split(f)
        country = dir.split('/')[7]
        year = re.findall('[1-2][0-9][0-9][0-9]', fn)[0]
        company = re.sub('[1-2][0-9][0-9][0-9]', '', fn).replace('_','').replace('.pdf','').strip().lower()
        print (country, year, company)
        path = os.path.join(outputdir, country, year)
        os.makedirs(path, exist_ok=True)
        txtfilename = os.path.join(path, f"{country}_{company}_{year}.txt.gz")
        if os.path.exists(txtfilename):
            # print(f'{txtfilename} already exists, skipping')
            continue
        try:
            text = extract_pdf_tika(f)
            if text is None:
                print("tika did not succed, trying pypdf2 instead...")
                text = extract_pdf_pypdf2(f)
                if len(text.strip())>0:
                    print('Succeeded!')
                else:
                    print('That did not work either.')
                    errors += 1
        except Exception as e:
            print (e)
            errors +=1
            continue

        with gzip.open(txtfilename, mode='wt') as fo:
            fo.write(text)
    print(f'{errors} PDFs could not be read.')
