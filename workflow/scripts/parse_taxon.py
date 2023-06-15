import pandas as pd
import numpy as np
import argparse
import sys
import time

# https://github.com/wrf/taxonomy_database/blob/master/parse_ncbi_taxonomy.py
def names_to_nodes(namesfile, metagenomes_only=False):
    '''read names.dmp and return a dict where name is key and value is the node number'''
    name_to_node = {}
    node_to_name = {}
    sys.stderr.write("# reading species names from {}  {}\n".format(namesfile, time.asctime() ) )
    i = 0
    for line in open(namesfile,'r'):
        line = line.strip()
        if line:
            lsplits = [s.strip() for s in line.split("|")]
            #print(lsplits)
            nameclass = lsplits[3]
            if nameclass=="scientific name":
                node = lsplits[0]
                species = lsplits[1]
                # if in metagenome mode, skip species names that do not have "metagenome"
                if metagenomes_only and species.find("metagenome") == -1:
                    continue
                name_to_node[species] = node
                node_to_name[node] = species
                i+=1
        #if (i == 15) : break
    sys.stderr.write("# counted {} scientific names from {}  {}\n".format( len(name_to_node), namesfile, time.asctime() ) )
    return name_to_node, node_to_name

def nodes_to_parents(nodesfilelist):
    '''read nodes.dmp and return two dicts where keys are node numbers'''
    node_to_rank = {}
    node_to_parent = {}
    i = 0
    for nodesfile in nodesfilelist:
        sys.stderr.write("# reading nodes from {}  {}\n".format(nodesfile, time.asctime() ) )
        for line in open(nodesfile,'r'):
            line = line.strip()
            if line:
                lsplits = [s.strip() for s in line.split("|")]
                #print(lsplits)
                node = lsplits[0]
                parent = lsplits[1]
                rank = lsplits[2]
                node_to_rank[node] = rank
                node_to_parent[node] = parent
                i+=1
                #if (i == 15) : break
    sys.stderr.write("# counted {} nodes from {}  {}\n".format( len(node_to_rank), nodesfile, time.asctime() ) )
    return node_to_rank, node_to_parent


def get_parent_tree(nodenumber, noderanks, nodeparents):
    '''given the node number, and the two dictionaries, traverse the tree until you end with kingdom and return a list of the numbers of the kingdom, phylum and class'''
    
    parent = "0"
    ranks = {
        "superkingdom": None,
        "kingdom": None,
        "subkingdom": None,
        "superphylum": None,
        "phylum": None,
        "subphylum": None,
        "infraphylum": None,
        "superclass": None,
        "pclass": None,
        "subclass": None,
        "infraclass": None,
        "cohort": None,
        "superorder": None,
        "order": None,
        "parvorder": None,
        "suborder": None,
        "infraorder": None,
        "section": None,
        "subsection": None,
        "superfamily": None,
        "family": None,
        "subfamily": None,
        "supertribe": None,
        "tribe": None,
        "genus": None,
        "subgenus": None,
        "species_group": None,
        "species_subgroup": None,
        "species": None,
        "subspecies": None,
        "varietas": None,
        "forma": None,
        "forma_specialis": None,
        "clade": None,
        "biotype": None,
        "isolate": None,
        "morph": None,
        "pathogroup": None,
        "genotype": None,
        "no_rank": None
    }
    
    while nodenumber != "1":
        try:
            rank = noderanks[nodenumber]
            if rank in ranks:
                ranks[rank] = nodenumber
            if nodenumber == "2" or nodenumber == "2157": # for bacteria and archaea
                ranks["kingdom"] = nodenumber
        except KeyError:
            sys.stderr.write("WARNING: NODE {} MISSING, CHECK delnodes.dmp\n".format(nodenumber))
            return ["Deleted", "Deleted", "Deleted", "Deleted", "Deleted", "Deleted", "Deleted", "Deleted"]
        
        parent = nodeparents[nodenumber]
        nodenumber = parent
    
    return ranks

def get_species(parentnumber, noderanks, nodeparents):
    #finds species and under
    species = []
    for node in noderanks: 
        #go through ranks, if rank is species or subspecies, see if parent is in traceback
        #if noderanks[node] == "species" or noderanks[node] == "subspecies":
        if parentnumber != node: 
            finalnode = get_parent_tree(node, noderanks, nodeparents)
            finalnode=list(finalnode.values())
            if parentnumber in finalnode:
                species.append(node)
    #if noderanks[parentnumber] == "species" or noderanks[parentnumber] == "subspecies": species.append(parentnumber)
    return species

###############Taxonomy######################
def get_species_ids(taxnames):
    '''
    namesfile = "data/preset/names.dmp"
    nodesfile = ["data/preset/nodes.dmp"]
    name_to_node, node_to_name = names_to_nodes(namesfile)
    node_to_rank, node_to_parent = nodes_to_parents(nodesfile)
    finalnodes = get_parent_tree(name_to_node[name], node_to_rank, node_to_parent)
    species_ids = get_species(name_to_node[name], node_to_rank, node_to_parent)
    return species_ids
    '''
    species_ids = []
    namesfile = "data/preset/names.dmp"
    nodesfile = ["data/preset/nodes.dmp"]
    name_to_node, node_to_name = names_to_nodes(namesfile)
    node_to_rank, node_to_parent = nodes_to_parents(nodesfile)
    
    for name in taxnames:
        
        rankdict = get_parent_tree(name, node_to_rank, node_to_parent)
        
        # Iterate through the ranks and print non-None values
        
        print("\nTraceback:\n______________\n")
        for rank, value in rankdict.items():
            if value is not None:
                print(f"{rank}: {value}")
                
        print(f"\nFinding taxon IDs within {name}...\n")
            
        finalnodes = list(rankdict.values())
        species = get_species(name, node_to_rank, node_to_parent)
        print("Number of taxon IDs to search: ", len(species), "\n")
        species_ids = species_ids + species
        
    return species_ids

