snakemake --profile config/  \
    --config \
        outname=acc_test\
        accortaxon=accession \
        filename=testing-files/accessions.txt \
        only_download_complete_genomes=f \
        only_download_latest=f \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'

snakemake --profile config/  \
    --config \
        outname=taxonomy_test \
        accortaxon=taxonomy \
        filename=workflow/testing-files/taxonomy.txt \
        only_download_complete_genomes=f \
        only_download_latest=t \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'
