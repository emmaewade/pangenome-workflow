import argparse
import parse_taxon
import make_genbank_refseq_file
import parse_biosample
import pandas as pd
import numpy as np
import argparse
import sys
import time
#import entrez_parse_taxon

'''
python utils/main.py \
    --accsofinterest ../data/accessions_of_interest.txt \
    --taxons 'Streptococcus' \
    --outdir results/ \
    --outfilename testing_masterfile 

'''


def parse_arguments():
    parser = argparse.ArgumentParser("")
    parser.add_argument('--accsofinterest', help='file name of accessions of interest', default=None, required=True, type=str) #eventually change to filename
    parser.add_argument('--taxons', help='taxons IDs to parse', default=None, required=False, type=str) #eventually change to filename
    parser.add_argument('--outdir', help="Master file output directory", default=".", type=str)
    parser.add_argument('--outfilename', default="master_file", type=str)
    parser.add_argument('--parse_biosample', action='store_true')
    # parser.add_argument('--')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    print(args)
    
    #if no taxon provided: parse for species ids
    if args.taxons != None and args.accsofinterest != 'None': 
        #species_ids = parse_taxon.get_species_ids(args.taxons)
        #rank_name = "species"  # Specify the rank you want to search for 
        #taxon_id = "616" # Taxon ID for Serratia
        # Example usage
        #taxon_id = '1304'  # Example taxon ID to search for
        #rank_name = 'species'  # Example rank name to search for
        species_ids = parse_taxon.get_species_ids(args.taxons)
        print(species_ids)
        in_genbank = make_genbank_refseq_file.genbank_table(species_ids, 'taxid') 
        in_refseq = make_genbank_refseq_file.refseq_table(species_ids, 'taxid') 
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, args.accsofinterest)
        
    ###doesn't work!####
    elif args.taxons == None and args.accsofinterst != None: 
        #read in accessions
        #accession_ids = open(args.accsofinterest).readlines()
        with open(args.accsofinterest, 'r') as file:
            accession_ids = file.readlines()
        accession_ids = [line.strip() for line in accession_ids]
        in_genbank = make_genbank_refseq_file.genbank_table(accession_ids, 'assembly_accession')
        in_refseq = make_genbank_refseq_file.refseq_table(accession_ids, 'assembly_accession')
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, args.accsofinterest) #doesn't work!
        
    elif args.taxons != None and args.accsofinterest == 'None': 
        #rank_name = 'genus'  # Example rank name to search for
        species_ids = parse_taxon.get_species_ids(args.taxons)
        print(species_ids)
        in_genbank = make_genbank_refseq_file.genbank_table(species_ids, 'taxid') 
        in_refseq = make_genbank_refseq_file.refseq_table(species_ids, 'taxid') 
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, args.accsofinterest) #just makes interest a copy of genbank
    
    
    #joined = make_genbank_refseq_file.join_experiment_tables(species_ids) ###need to an argument for my data
    if args.parse_biosample : 
        metadata = parse_biosample.parse_entrez(joined['biosample'],endcount=None)
        joined = pd.merge(joined, metadata, on = 'biosample', how = 'outer')
    
    save = True
    if save:
        joined.to_csv(f"{args.outdir}/{args.outfilename}.csv")
        return(f"{args.outdir}/{args.outfilename}.csv")
    
if __name__ == "__main__":
    main()

    

'''
1) Get species ids from parsing
2) Make giant genbank x refseq file from all species ids
3) Join accessions of interest to giant table
4) If biosampleparse, join biosample on biosample

Instead: 
1) Given accessions of interest
2) Find the accessions of interest in the refseq and genbank files
3) 

need:
 - function to find genbank and refseq by species ids
 - function to find by genbank and refseq by accessions 
 - 
'''