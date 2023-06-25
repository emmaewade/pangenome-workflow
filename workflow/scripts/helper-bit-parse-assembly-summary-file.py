#!/usr/bin/env python

import sys
import argparse
import os

parser = argparse.ArgumentParser(description='This script is for parsing NCBI\'s assembly summary file down\
                                              to the provided accessions. It is used by the `bit-dl-ncbi-assemblies`\
                                              script. For version info, run `bit-version`.')

required = parser.add_argument_group('required arguments')

required.add_argument("-g", "-genbank_summary", help="NCBI's genbank summary file", action="store", dest="genbank", required=True)
required.add_argument("-r", "-refseq_summary", help="NCBI's refseq summary file", action="store", dest="refseq", required=True)
required.add_argument("-w", "--wanted", help="Single-column file with wanted accessions or taxonomy IDs", action="store", dest="wanted", required=True)
required.add_argument("-t", "--accession_or_taxonomy", help="Search for accessions or taxonomy", action="store", dest="a_or_t", required=True)
parser.add_argument("-o", "--output_file", help='Wanted summary info only (default: "Wanted.tsv")', action="store", dest="output_file", default="wanted.tsv")
parser.add_argument("-f", "--filter_complete", help='t = only complete genomes f = keep complete genomes, scaffolds, chromosomes, and contigs', action="store", dest="complete", default="t")
parser.add_argument("-v", "--filter_latest", help='t = only latest version f = all versions', action="store", dest="latest", default="t")


if len(sys.argv)==1:
  parser.print_help(sys.stderr)
  sys.exit(0)

args = parser.parse_args()

wanted_dict = {}

with open(args.wanted, "r") as wanted_accs:
  
    for line in wanted_accs:
        root_acc = line.strip().split(".")[0]
        wanted_dict[str(root_acc)] = line.strip()

out_file = open(args.output_file, "w")


####If given list of accessions, search genbank and refseq######
if args.a_or_t == "accession":
        
    with open(args.genbank) as assemblies:
        
        for line in assemblies:
            
            line = line.split("\t")
            
            if line[0].startswith("#"): continue
        
            #if in accession list, assembly_level is Complete Genome, and version is latest
            if line[0].split(".")[0] in wanted_dict:
                
                if line[11] != "Complete Genome" and args.complete == "t": continue 
                
                if line[10] != "latest" and args.latest == "t" : continue
                
                dl_acc = str(line[0])
    
                if not dl_acc:
                    dl_acc = "NA"
    
                ass_name = str(line[15])
                if not ass_name:
                    ass_name = "NA"
    
                taxid = str(line[5])
                if not taxid:
                    taxid = "NA"
    
                org_name = str(line[7])
                if not org_name:
                    org_name = "NA"
    
                infra_name = str(line[8])
                if not infra_name:
                    infra_name = "NA"
    
                version_status = str(line[10])
                if not version_status:
                    version_status = "NA"
    
                ass_level = str(line[11])
                if not ass_level:
                    ass_level = "NA"
    
                ftp_path = str(line[19])
                if not ftp_path:
                    ftp_path = "NA"
    
                out_file.write(str(wanted_dict[str(line[0].split(".")[0])]) + "\t" + str(dl_acc) + "\t"  + str(ass_name) + "\t" + str(taxid) + "\t" + str(org_name) + "\t" + str(infra_name) + "\t" + str(version_status) + "\t" + str(ass_level) + "\t" + str(ftp_path) + "\n")

    with open(args.refseq) as assemblies:
        
        for line in assemblies:
            
            line = line.split("\t")
            
            if line[0].startswith("#"): continue
        
            #if in accession list, assembly_level is Complete Genome, and version is latest
            if line[0].split(".")[0] in wanted_dict:
                
                if line[11] != "Complete Genome" and args.complete == "t": continue 
                
                if line[10] != "latest" and args.latest == "t" : continue
                
                dl_acc = str(line[0])
    
                if not dl_acc:
                    dl_acc = "NA"
    
                ass_name = str(line[15])
                if not ass_name:
                    ass_name = "NA"
    
                taxid = str(line[5])
                if not taxid:
                    taxid = "NA"
    
                org_name = str(line[7])
                if not org_name:
                    org_name = "NA"
    
                infra_name = str(line[8])
                if not infra_name:
                    infra_name = "NA"
    
                version_status = str(line[10])
                if not version_status:
                    version_status = "NA"
    
                ass_level = str(line[11])
                if not ass_level:
                    ass_level = "NA"
    
                ftp_path = str(line[19])
                if not ftp_path:
                    ftp_path = "NA"
    
                out_file.write(str(wanted_dict[str(line[0].split(".")[0])]) + "\t" + str(dl_acc) + "\t"  + str(ass_name) + "\t" + str(taxid) + "\t" + str(org_name) + "\t" + str(infra_name) + "\t" + str(version_status) + "\t" + str(ass_level) + "\t" + str(ftp_path) + "\n")


elif args.a_or_t == "taxonomy":
    
    with open(args.genbank) as assemblies:
        
        for line in assemblies:
            
            line = line.split("\t")
            
            if line[0].startswith("#"): continue
        
            if line[5] in wanted_dict:
                
                if line[11] != "Complete Genome" and args.complete == "t": continue 
                
                if line[10] != "latest" and args.latest == "t" : continue
                
                dl_acc = str(line[0])
    
                if not dl_acc:
                    dl_acc = "NA"
    
                ass_name = str(line[15])
                if not ass_name:
                    ass_name = "NA"
    
                taxid = str(line[5])
                if not taxid:
                    taxid = "NA"
    
                org_name = str(line[7])
                if not org_name:
                    org_name = "NA"
    
                infra_name = str(line[8])
                if not infra_name:
                    infra_name = "NA"
    
                version_status = str(line[10])
                if not version_status:
                    version_status = "NA"
    
                ass_level = str(line[11])
                if not ass_level:
                    ass_level = "NA"
    
                ftp_path = str(line[19])
                if not ftp_path:
                    ftp_path = "NA"
    
                out_file.write(str(line[0].split(".")[0]) + "\t" + str(dl_acc) + "\t"  + str(ass_name) + "\t" + str(taxid) + "\t" + str(org_name) + "\t" + str(infra_name) + "\t" + str(version_status) + "\t" + str(ass_level) + "\t" + str(ftp_path) + "\n")
