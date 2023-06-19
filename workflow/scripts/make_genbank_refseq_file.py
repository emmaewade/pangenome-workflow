import pandas as pd
import numpy as np
import argparse
import sys
import time

def genbank_table(ids, searchcol, report_file):
    ################### 1 parse out all the Streptococcus genomes in NCBI #############################################
    ##### 1.a try the assembly reports to get the samples #############################################################
    # Use the genbank list
    #https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt
    #"C:\pg_project\data\assembly_summary_genbank.txt"
    #report_file = "data/assembly_summary_genbank.txt"
    chunksize = 1000000 #chunksize = args.chunksize
    nrows = None #nrows = args.nrows
    #species = "Streptococcus " #species = args.species 
    in_genbank = pd.DataFrame()
    
    #read in file by chunks
    for chunk in pd.read_csv(report_file, header=0, index_col=False, sep="\t", iterator=True, skiprows=[0],chunksize=chunksize, nrows = nrows, dtype='unicode'):
        #name columns
        #chunk.columns = ['assembly_accession', 'bioproject','biosample','wgs_master','refseq_category','taxid', 'species_taxid','organism_name','infraspecific_name','isolate','version_status','assembly_level','release_type','genome_rep','seq_rel_date','asm_name', 'asm_submitter','gbrs_paired_asm','paired_asm_comp','ftp_path','excluded_from_refseq','relation_to_type_material','asm_not_live_date']
        #bioproject      biosample       wgs_master      refseq_category taxid   species_taxid   organism_name   infraspecific_name      isolate version_status  assembly_level  release_type    genome_rep      seq_rel_date    asm_name        asm_submitter   gbrs_paired_asm paired_asm_comp ftp_path        excluded_from_refseq    relation_to_type_material       asm_not_live_date       assembly_type   group   genome_size     genome_size_ungapped    gc_percent      replicon_count  scaffold_count  contig_count    annotation_provider     annotation_name annotation_date total_gene_count        protein_coding_gene_count       non_coding_gene_count   pubmed_id
        #drop unneeded columns
        chunk.drop(['infraspecific_name','isolate','version_status','refseq_category','wgs_master','assembly_level','release_type','genome_rep','seq_rel_date','asm_name', 'asm_submitter','gbrs_paired_asm','paired_asm_comp','relation_to_type_material','asm_not_live_date'], axis = 1, inplace = True)
        chunk = chunk.rename(columns={'#assembly_accession': 'assembly_accession'})
        #chunk = chunk[chunk['organism_name'].str.startswith(species)] # %in% taxon_ids
        chunk = chunk[chunk[searchcol].isin(ids)]
        #add chunk to dataframe
        if in_genbank is None:
            in_genbank = chunk
        else:
            in_genbank = pd.concat([in_genbank,chunk])
            
    if in_genbank.empty:
        print("\nNo genbank accessions found\n")
        in_genbank = pd.DataFrame(columns=['assembly_accession', 'bioproject','biosample', 'taxid', 'species_taxid','organism_name', 'ftp_path','excluded_from_refseq'])
    
    else:
        print("---------------\nFound in genbank...\n---------------")
        print(in_genbank)
            
    return in_genbank
    
def refseq_table(ids, searchcol, report_file): 
    ##### 1.b Verify all the samples in the Streptococcus refseq are also found in the genbank ########################
    #https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt
    #Parse 'Streptococcus ' at begining of species name, A space is used to make sure we get the right genus as other genuse exist ..... 
    #report_file = "data/preset/assembly_summary_refseq.txt" #<-- turn into argument
    chunksize = 1000000 #chunksize = args.chunksize
    nrows = None #nrows = args.nrows
    species = "Streptococcus " #species = args.species
    in_refseq = pd.DataFrame()
    for chunk in pd.read_csv(report_file, header=0, index_col=False, sep="\t", iterator=True, skiprows=[0],chunksize=chunksize, nrows = nrows, dtype='unicode'):
        #chunk.columns = ['assembly_accession', 'bioproject','biosample','wgs_master','refseq_category','taxid', 'species_taxid','organism_name','infraspecific_name','isolate','version_status','assembly_level','release_type','genome_rep','seq_rel_date','asm_name', 'submitter','gbrs_paired_asm','paired_asm_comp','ftp_path','excluded_from_refseq','relation_to_type_material','asm_not_live_date']
        chunk.drop(['infraspecific_name','isolate','version_status','refseq_category','wgs_master','assembly_level','release_type','genome_rep','seq_rel_date','asm_name', 'asm_submitter','gbrs_paired_asm','paired_asm_comp','relation_to_type_material','asm_not_live_date'], axis = 1, inplace = True)
        #if args.chrs is not None: chunk = chunk[chunk['Chr'].isin(args.chrs)]
        #chunk = chunk[chunk['organism_name'].str.startswith(species)]
        chunk = chunk.rename(columns={'#assembly_accession': 'assembly_accession'})
        chunk = chunk[chunk[searchcol].isin(ids)]
        if in_refseq is None:
            in_refseq = chunk
        else:
            in_refseq = pd.concat([in_refseq,chunk])
            
    if in_refseq.empty:
        print("\nNo refseq accessions found\n")
        in_refseq = pd.DataFrame(columns=['assembly_accession', 'bioproject','biosample', 'taxid', 'species_taxid','organism_name', 'ftp_path','excluded_from_refseq'])
    else:
        print("---------------\nFound in refseq...\n---------------")
        print(in_refseq)
        
    return in_refseq


def join_tables(in_genbank, in_refseq):
    ###########################################
    joined = pd.merge(in_genbank, in_refseq[['assembly_accession', 'biosample', 'ftp_path']], on=['biosample'], how = "outer")
    joined.rename(columns = {'assembly_accession_x':'genbank_assembly_accession', 'assembly_accession_y':'refseq_assembly_accession', 'ftp_path_x':'genbank_ftp_path', 'ftp_path_y':'refseq_ftp_path' }, inplace = True)
    return joined

def join_experiment_tables(joined, filename):
    
    if filename == 'None': 
        
        try: joined[['genbank_assembly_accession_base', 'genbank_assembly_accession_vers']] = joined['genbank_assembly_accession'].str.split('.', n = 1, expand=True)
        except:  
            joined['genbank_assembly_accession_base'] = '' 
            joined['genbank_assembly_accession_vers'] = ''
        
        try: joined[['refseq_assembly_accession_base', 'refseq_assembly_accession_vers']] = joined['refseq_assembly_accession'].str.split('.', n = 1, expand=True)
        except: 
            joined['refseq_assembly_accession_base'] = '' 
            joined['refseq_assembly_accession_vers'] = ''
            
        joined[['interest_assembly_accession', 'interest_assembly_accession_base', 'interest_assembly_accession_vers']] = joined[['genbank_assembly_accession', 'genbank_assembly_accession_base', 'genbank_assembly_accession_vers']]
        return joined
        
    else: 
        
        int_acc = pd.read_csv(filename, header=None, index_col=False, sep="/n", dtype='unicode')
        int_acc.columns = ['interest_assembly_accession']
        int_acc['interest_assembly_accession'] = int_acc['interest_assembly_accession'].astype(str)
        
        try: joined[['genbank_assembly_accession_base', 'genbank_assembly_accession_vers']] = joined['genbank_assembly_accession'].str.split('.', n = 1, expand=True)
        except:  
            joined['genbank_assembly_accession_base'] = ''
            joined['genbank_assembly_accession_vers'] = ''
        
        try: joined[['refseq_assembly_accession_base', 'refseq_assembly_accession_vers']] = joined['refseq_assembly_accession'].str.split('.', n = 1, expand=True)
        except: 
            joined['refseq_assembly_accession_base'] = ''
            joined['refseq_assembly_accession_vers'] = ''
        
        int_acc[['interest_assembly_accession_base', 'interest_assembly_accession_vers']] = int_acc['interest_assembly_accession'].str.split('.', n = 1, expand=True)
        
        joined['refseq_assembly_accession_base'] = joined['refseq_assembly_accession_base'].astype(str)
        joined['genbank_assembly_accession_base'] = joined['genbank_assembly_accession_base'].astype(str)
        joined_ref = pd.merge(joined, int_acc, left_on=['refseq_assembly_accession_base'], right_on = ['interest_assembly_accession_base'], how = 'outer')
        #joined_ref.to_csv("joined_refseq.csv")
        joined_gen_ref = pd.merge(joined_ref, int_acc, left_on=['genbank_assembly_accession_base'], right_on = ['interest_assembly_accession_base'], how = 'outer')
        
        joined_all = joined.copy()
        joined_all['interest_assembly_accession_base'] = joined_gen_ref.fillna("").apply(lambda x: str(x['interest_assembly_accession_base_x']) + str(x['interest_assembly_accession_base_y']) if x['interest_assembly_accession_base_x'] != x['interest_assembly_accession_base_y'] else x['interest_assembly_accession_base_x'], axis=1)
        joined_all['interest_assembly_accession_vers'] = joined_gen_ref.fillna("").apply(lambda x: str(x['interest_assembly_accession_vers_x']) + str(x['interest_assembly_accession_vers_y']) if x['interest_assembly_accession_vers_x'] != x['interest_assembly_accession_vers_y'] else x['interest_assembly_accession_base_x'], axis=1)
        joined_all['interest_assembly_accession'] = joined_gen_ref.fillna("").apply(lambda x: str(x['interest_assembly_accession_x']) + str(x['interest_assembly_accession_y']) if x['interest_assembly_accession_x'] != x['interest_assembly_accession_y'] else x['interest_assembly_accession_base_x'], axis=1)
    
        return joined_all