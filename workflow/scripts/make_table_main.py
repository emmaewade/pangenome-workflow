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
    --accortaxon accession \
    --filename ../data/accessions_of_interest.txt \
    --outdir results/ \
    --outfilename testing_masterfile 

'''


def parse_arguments():
    parser = argparse.ArgumentParser("")
    parser.add_argument('--filename', help='file name of accessions of interest', default="None", required=False, type=str) #eventually change to filename
    #parser.add_argument('--taxons', help='taxons IDs to parse', default="None", required=False, type=str) #eventually change to filename
    parser.add_argument('--outdir', help="Master file output directory", default=".", type=str)
    parser.add_argument('--outfilename', default="master_file", type=str)
    #parser.add_argument('--parse_biosample', action='store_true')
    parser.add_argument('--accortaxon', choices=['accession', 'taxonomy'], required=True, type=str) #eventually change to filename
    parser.add_argument('--gen', help="Master file output directory", required=True, type=str)
    parser.add_argument('--ref', help="Master file output directory", required=True, type=str)
    parser.add_argument('--names', help="Master file output directory", required=True, type=str)
    parser.add_argument('--nodes', help="Master file output directory", required=True, type=str)
    # parser.add_argument('--')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    #print(args)
    
    
    #if no taxon provided: parse for species ids
    #if args.taxons != "None" and args.accsofinterest != "None": 
    if False:
        print(f"\nSearching for taxon: {args.taxons}")
        print(f"Interested in accessions: {args.accsofinterest}\n")
        
        with open(args.taxons, 'r') as file:
            taxon_ids = file.readlines()
        taxon_ids = [line.strip() for line in taxon_ids]
        
        species_ids = parse_taxon.get_species_ids(taxon_ids, args.names, args.nodes)
        
        with open(f"{args.outdir}/species.csv","wt") as file:
            for thestring in species_ids:
                print(thestring, file=file)
                
        #print(species_ids)
        in_genbank = make_genbank_refseq_file.genbank_table(species_ids, 'taxid', args.gen) 
        in_refseq = make_genbank_refseq_file.refseq_table(species_ids, 'taxid', args.ref) 
        
        if in_genbank.empty and in_refseq.empty : raise Exception('No accessions found!')
        
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, args.accsofinterest)
        
    elif args.accortaxon == "accession":
        print("\nNot searching taxonomy")
        print(f"Interested in accessions: {args.filename}\n")
        #read in accessions
        #accession_ids = open(args.accsofinterest).readlines()
        with open(args.filename, 'r') as file:
            accession_ids = file.readlines()
        accession_ids = [line.strip() for line in accession_ids]
        in_genbank = make_genbank_refseq_file.genbank_table(accession_ids, 'assembly_accession', args.gen)
        in_refseq = make_genbank_refseq_file.refseq_table(accession_ids, 'assembly_accession', args.ref)
        
        if in_genbank.empty and in_refseq.empty : raise Exception('No accessions found!')
        
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, args.filename)
        
    elif args.accortaxon == "taxonomy": 
        
        with open(args.filename, 'r') as file:
            taxon_ids = file.readlines()
        taxon_ids = [line.strip() for line in taxon_ids]
        
        print(f"\nSearching for taxon: {args.filename}")
        print(f"Taxons {args.filename} are of interest\n")
        #rank_name = 'genus'  # Example rank name to search for
        species_ids = parse_taxon.get_species_ids(taxon_ids, args.names, args.nodes)
        
        with open(f"{args.outdir}/species.csv","wt") as file:
            for thestring in species_ids:
                print(thestring, file=file)
            
        in_genbank = make_genbank_refseq_file.genbank_table(species_ids, 'taxid', args.gen) 
        in_refseq = make_genbank_refseq_file.refseq_table(species_ids, 'taxid', args.ref) 
        
        if in_genbank.empty and in_refseq.empty : raise Exception('No accessions found!')
        
        gen_ref = make_genbank_refseq_file.join_tables(in_genbank, in_refseq)
        joined = make_genbank_refseq_file.join_experiment_tables(gen_ref, 'None') #just makes interest a copy of genbank
    
    else: raise Exception("Incorrect input!")
        
    save = True
    if save:
        joined.to_csv(f"{args.outdir}/{args.outfilename}.csv")
        
        #GCA_018603945.1 GCA_018603945.1 ASM1860394v1    28037   Streptococcus mitis     strain=14-4881  latest  Contig  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/018/603/945/GCA_018603945.1_ASM1860394v1
        only_of_interest = joined[joined.interest_assembly_accession.notna()]
        only_of_interest.to_csv(f"{args.outdir}/of_interest.csv")
        only_of_interest_filtered = only_of_interest[['interest_assembly_accession', 'interest_assembly_accession', 'biosample', 'taxid', 'organism_name', 'biosample', 'interest_assembly_accession_vers', 'genbank_ftp_path']]
        only_of_interest_filtered.to_csv(f"{args.outdir}/for_download.tsv", sep='\t', header=False, index=False)
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