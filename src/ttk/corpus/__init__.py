
import urllib.request as req
import zipfile, os


from nltk.corpus import CategorizedPlaintextCorpusReader

import pathlib

from ttk import get_env_dir

# elevate modules
from ttk.corpus.CategorizedDatedCorpusReader import *
from ttk.corpus.CategorizedDatedCorpusReporter import *

DATE_CORPUS_FILENAME = '2017-08-22_headline_dated_corpus.zip'
CAT_CORPUS_FILENAME = '2017-08-16_headline_categorized_corpus.zip'


def load_headline_corpus(with_dates=True, force_get=False, verbose=False):
    # set up paths
    if with_dates:
        zip_file_name = DATE_CORPUS_FILENAME        
    else:
        zip_file_name = CAT_CORPUS_FILENAME
    
    # github download url
    url = 'https://github.com/tacticsiege/TacticCorpora/raw/master/headlines/archive/' + zip_file_name

    
    env_dir = get_env_dir()
    # archive paths
    archive_dir = env_dir + 'corpus\\archive\\'
    archive_file_name = archive_dir + zip_file_name
    # extracted corpus paths
    corpus_root = 'dated' if with_dates else 'categorized'
    saved_dir = env_dir + 'corpus\\' + corpus_root
    
    # check if the data is downloaded
    downloaded = os.path.exists(archive_file_name)

    # download the data from github
    if not downloaded:
        pathlib.Path(archive_dir).mkdir(parents=True, exist_ok=True)
        if verbose:
            print ('Downloading:', url, '...')
        with req.urlopen(url) as d, open(archive_file_name, 'wb') as tmpFile:
            data = d.read()
            tmpFile.write(data)
        if verbose:
            print ('Complete, saved to:', archive_file_name)

    # extract the data if the root directory doesn't exist
    extracted = os.path.exists(saved_dir)
    if not extracted:
        pathlib.Path(saved_dir).mkdir(parents=True, exist_ok=True)
        if verbose:
            print ('Opening:', archive_file_name)
        archive = zipfile.ZipFile(archive_file_name)        
        archive.extractall(saved_dir)
        archive.close()
        if verbose:
            print ('Extracted to:', saved_dir)
    
    file_pattern = r'.*_corpus\.txt'
    
    if with_dates:
        cat_pattern = r'(.*)/'
        # HACK: fix this in archive later
        saved_dir = saved_dir + '\\2017_08_22\\corpus'
        if verbose:
            print ('Loading corpus from:', saved_dir)
        corpus = CategorizedDatedCorpusReader(saved_dir, file_pattern=file_pattern, cat_pattern=cat_pattern)
    else:
        cat_pattern = ".*_(.*)_corpus.txt"
        if verbose:
            print ('Loading corpus from:', saved_dir)
        corpus = CategorizedPlaintextCorpusReader(saved_dir, file_pattern=file_pattern, cat_pattern=cat_pattern)

    if corpus is not None and verbose:
        print ('Corpus loaded.')

    return corpus