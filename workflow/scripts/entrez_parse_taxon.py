from Bio import Entrez
from xml.etree.ElementTree import fromstring

def find_species_taxon_ids(taxon_id, rank_name):
    """
    Get descendants of a given taxon ID and rank name in the NCBI Taxonomy database using Entrez.

    Args:
        taxon_id (str): Taxon ID to get descendants for.
        rank_name (str): Rank name to filter the descendants.

    Returns:
        list: List of taxon IDs of the descendants of the given taxon ID with the specified rank name.
    """
    descendants = []
    Entrez.email = 'your_email@example.com'  # Replace with your email address
    handle = Entrez.efetch(db='taxonomy', id=taxon_id, retmode='xml')
    record = Entrez.read(handle)
    handle.close()
    lineage_ex = record[0]['LineageEx']
    for child in lineage_ex:
        if child['Rank'] == rank_name:
            descendants.append(child['TaxId'])
    return descendants

'''
# Example usage
taxon_id = '1304'  # Example taxon ID of a genus to get descendants for
descendants_taxon_ids = get_descendants(taxon_id)
print(descendants_taxon_ids)
'''
