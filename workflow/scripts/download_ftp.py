import pandas as pd
import fnmatch
from ftplib import FTP
import sys
import time
import argparse
from itertools import repeat
import numpy as np
#import asyncio
from multiprocessing import Pool
import tqdm



def job(url):
    file_name = str(url.split('/')[-1])
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    f.write(u.read())
    f.close()

'''
def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped
''' 
def parse_arguments():
    parser = argparse.ArgumentParser("")
    parser.add_argument('--downloadsuffix', help='file type to download i.e. genomic.gbff.gz', default=None, required=True, type=str)
    parser.add_argument('--masterfile', help="Master file name and path", default=None, required=True, type=str)
    parser.add_argument('--outdir', default="Output directory of accession files", type=str)
    parser.add_argument('--databank', help="Genbank or RefSeq", choices=['Genbank', 'RefSeq'], default='Genbank')
    parser.add_argument('--filtercolumn', help="prev_assembly_accession or interest_assembly_accession", choices=['prev_assembly_accession', 'interest_assembly_accession'], default='interest_assembly_accession') #need a better way to filter!!! 
    # parser.add_argument('--')
    args = parser.parse_args()
    return args

#@background
def download(p, downloadto, downloadsuffix):
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    #sys.stdout.write(p)
    try:
        todirect = p[28:] #remove beginning --> cut to path
    except:
        sys.stdout.write(f"NAN : {p}\n")
        pass
    try: 
        ftp.cwd(todirect)
    except:
        sys.stdout.write(f"Pass at change working directory : {todirect}\n")
        pass
    try: 
        files = ftp.nlst()
    except:
        sys.stdout.write(f"Pass at list directory : {todirect}\n")
        pass
    if len(files) == 0:
        emptydirs += 1
    for file in files:
        #sys.stdout.write(f"File : {file}")
        if fnmatch.fnmatch(file, f'*{downloadsuffix}') :  #To download specific files.
            #print("Downloading..." + file)
            #sys.stdout.write(f"File matches pattern: {file}")
            try:
                ftp.retrbinary("RETR " + file ,open(downloadto + '/' + file, 'wb').write)
            except EOFError:    # To avoid EOF errors.
                sys.stdout.write(f"Pass at write : {todirect}")
                pass
    ftp.close()
    
def download_star(args):
    return download(*args)
            
def download_ftp(ftppaths, downloadto, downloadsuffix):
    i = 0
    emptydirs = 0
    #print(ftppaths)
    #return
    pool = Pool(100)
    inputs = zip(ftppaths, repeat(downloadto), repeat(downloadsuffix))
    with Pool(10) as pool:
        #downs = pool.starmap(download, tqdm(inputs, total=len(ftppaths)))
        results = list(tqdm.tqdm(pool.imap(download_star, inputs), total=len(ftppaths)))
        
        
    '''
    for p in ftppaths:
        download(p, downloadto, downloadsuffix)
        i+=1
        if i % 100 == 0: sys.stdout.write(f"Count : {i} Time: {time.asctime()}\n")
    '''
    #sys.stdout.write(f"No matching files in {emptydirs} directories\n")


if __name__ == "__main__":
    #Count : 32540 Time: Mon Nov  7 11:07:29 2022
    #if some abyss fac result is _____, then download 
    args = parse_arguments()
    #print(args)
    fulldf = pd.read_csv(f"{args.masterfile}", dtype='unicode')
    filterdf = fulldf[fulldf[f'{args.filtercolumn}'].notnull()]
    if args.databank == "Genbank" : ftp_paths = filterdf['genbank_ftp_path']
    elif args.databank == "RefSeq" : ftp_paths = filterdf['refseq_ftp_path']
    del(fulldf)
    del(filterdf)
    download_ftp(ftp_paths, args.outdir, args.downloadsuffix)
    