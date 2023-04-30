import pandas as pd
import fnmatch
from ftplib import FTP
import sys
import time
import argparse
#import parse_taxon
#import make_genbank_refseq_file
#import parse_biosample
import pandas as pd
import numpy as np
import argparse
import sys
import time


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


def download_ftp(ftppaths, downloadto, downloadsuffix):
     # Username: anonymous password: anonymous@
    #downloadto = "/anvil/projects/x-mcb200143/pg_project/data/ftp_downloads/" 
    i = 0
    emptydirs = 0
    #print(ftppaths)
    #return
    for p in ftppaths:
        ftp = FTP('ftp.ncbi.nlm.nih.gov')
        ftp.login()
        #sys.stdout.write(p)
        try:
            todirect = p[28:] #remove beginning --> cut to path
        except:
            sys.stdout.write(f"NAN : {p}\n")
            continue
        try: 
            ftp.cwd(todirect)
        except:
            sys.stdout.write(f"Pass at change working directory : {todirect}\n")
            continue
        try: 
            files = ftp.nlst()
        except:
            sys.stdout.write(f"Pass at list directory : {todirect}\n")
            continue
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
                    continue
        i+=1
        #if i == 5: break
        if i % 1000 == 0: sys.stdout.write(f"Count : {i} Time: {time.asctime()}\n")
        ftp.close()
    sys.stdout.write(f"No gbff files in {emptydirs} directories\n")


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
    